"""`<ui.name>` components — a second, richer component system alongside
`ComponentRegistry`/`<component.name>` (registry.py, extension.py).

Built for porting design-system component libraries (e.g. cotton-based UI
kits) whose components rely on two things plain `{% component %}` doesn't
support:

  - **Automatic attrs pass-through**: any prop passed to a `<ui.x>` call that
    the component didn't declare via `{% uivars %}` is collected into an
    `attrs` variable (an HTML attribute string) instead of being silently
    dropped, so `<ui.button id="save-btn" data-testid="x">` just works
    without the component template listing every possible caller attribute.
  - **Named slots**: `<ui-slot name="header">...</ui-slot>` inside a
    `<ui.card>` call renders that markup into a `header` variable inside
    card's own template — same idea as the default `{{ slot }}`, just named.
    This is done entirely by the HTML-sugar preprocessor (turning each
    `<ui-slot>` into a Jinja2 native `{% set %}` capture passed as a keyword
    prop) rather than any custom runtime plumbing — `{% set x %}...{% endset
    %}` is a well-tested, core Jinja2 feature, so a named slot is, by the
    time the runtime ever sees it, indistinguishable from any other keyword
    prop. This sidesteps the much more fragile alternative (a side-channel
    written into `Context.vars` from inside a nested `{% call %}` block,
    whose visibility back out depends on Jinja2's for/call scoping rules —
    not something to build a feature's correctness on).

Deliberately a SEPARATE registry/tag/preprocessor from `ComponentRegistry`/
`ComponentExtension`, not a superset bolted onto it: plain `{% component %}`
components have simpler (single anonymous slot, explicit kwargs only)
semantics that plenty of callers rely on and shouldn't have to opt out of.
"""

import logging
import re
from pathlib import Path
from typing import Optional

from jinja2 import nodes
from jinja2.ext import Extension
from markupsafe import Markup, escape

logger = logging.getLogger(__name__)


class UIComponentRegistry:
    """Global registry for `<ui.name>` components — same flat, process-wide
    shape as `ComponentRegistry` (see its docstring for the collision
    caveat and the recommended naming-prefix workaround)."""

    _components: dict = {}

    @classmethod
    def register(cls, name: str, template: str):
        existing = cls._components.get(name)
        if existing is not None and existing != template:
            logger.warning(
                "UI component '%s' re-registered with different content — "
                "the previous definition is now shadowed.",
                name,
            )
        cls._components[name] = template

    @classmethod
    def get(cls, name: str):
        return cls._components.get(name)

    @classmethod
    def all(cls) -> dict:
        return dict(cls._components)


def auto_register_ui_components(folder: str):
    """Auto-register all `*.html` files in `folder` as `<ui.x>` components,
    named by filename stem — mirrors `auto_register_components`."""
    path = Path(folder)
    if not path.exists():
        return
    for file in path.glob("*.html"):
        UIComponentRegistry.register(file.stem, file.read_text())


# Props every component receives that are never part of `attrs` — the
# default slot and any named slots the caller passed are content, not HTML
# attributes on the root element.
_RESERVED_PROPS = {"slot", "children"}


def _as_bare_expr(value: str) -> str:
    """`"{{ page.title }}"` -> `page.title` — see call sites for why."""
    v = value.strip()
    return v[2:-2].strip() if v.startswith("{{") and v.endswith("}}") else v


def _build_attrs(extra: dict) -> Markup:
    parts = []
    for key, value in extra.items():
        if value is False or value is None or value == "":
            continue
        if value is True:
            parts.append(key)
        else:
            parts.append(f'{key}="{escape(value)}"')
    return Markup(" ".join(parts))


class UIVarsExtension(Extension):
    """`{% uivars key=default ... %}` — must be the first statement in a
    `<ui.x>` component template. Declares this component's known prop names
    (with defaults); every OTHER prop the caller passed (that isn't a
    reserved slot name) is collected into `attrs` instead of being ignored.

    Not a block tag: it has no body, just a side effect on the current
    render's context — the same pattern as Jinja2's built-in `{% do %}`
    extension (evaluate an expression, print nothing).
    """

    tags = {"uivars"}

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        declared = []  # [(name, default_expr_node), ...]
        while parser.stream.current.type != "block_end":
            key = parser.parse_assign_target()
            parser.stream.expect("assign")
            value = parser.parse_expression()
            declared.append((key.name, value))

        stmts = []

        # `attrs` FIRST, from whatever the caller actually passed in — this
        # must be a real `Assign` node (not an opaque method call whose side
        # effect only mutates `context.vars`): Jinja2 hoists every free
        # variable used later in the template to a local at the top of the
        # compiled function (`l_0_attrs = resolve('attrs')`, run BEFORE this
        # tag's own code executes), and later `{{ attrs }}` reads reuse that
        # already-hoisted local — mutating `context.vars` afterwards doesn't
        # touch it. A proper `Assign` node is what `{% set %}` itself compiles
        # to, and *that* correctly updates the same local Jinja2 already
        # hoisted, because the compiler's static pass sees `attrs` as locally
        # assigned and knows to route later reads through the assignment.
        names_list = nodes.List([nodes.Const(n) for n, _ in declared])
        attrs_call = self.call_method("_compute_attrs", [nodes.ContextReference(), names_list])
        stmts.append(nodes.Assign(nodes.Name("attrs", "store"), attrs_call).set_lineno(lineno))

        # Then each declared prop: keep the caller's value if they passed
        # one, else fall back to its `{% uivars %}` default — same
        # `{% set x = x if x is defined else default %}` shape, for the same
        # hoisting reason.
        for name, default_expr in declared:
            is_defined = nodes.Test(nodes.Name(name, "load"), "defined", [], [], None, None)
            value = nodes.CondExpr(is_defined, nodes.Name(name, "load"), default_expr)
            stmts.append(nodes.Assign(nodes.Name(name, "store"), value).set_lineno(lineno))

        return stmts

    def _compute_attrs(self, context, declared_names) -> Markup:
        provided = context.get_all()
        # __slot_names (injected by UIComponentPreprocessor for each
        # <ui-slot name="x"> the caller passed) marks x as slot CONTENT, not
        # an HTML attribute — without this, a named slot value (arbitrary
        # markup) would get dumped straight into `attrs` right alongside real
        # attributes, since by this point it's just another keyword prop.
        excluded = set(declared_names) | set(provided.get("__slot_names", ()))
        extra = {
            k: v
            for k, v in provided.items()
            if k not in excluded
            and k not in _RESERVED_PROPS
            and k not in context.globals_keys  # env-wide globals (static, csrf_token, range, dict...)
            and not k.startswith("_")
        }
        # __raw_attrs (hyphenated/Alpine.js names — data-foo, aria-*, x-data,
        # :class, @click — that can't be Jinja2 keyword-argument names at
        # all, see UIComponentPreprocessor._parse_props) merge unconditionally.
        extra.update(provided.get("__raw_attrs", {}))
        return _build_attrs(extra)


class UIComponentExtension(Extension):
    """Handles `{% uicomponent "name" key=value %}...{% enduicomponent %}` —
    the compiled form of `<ui.name>`, produced by `UIComponentPreprocessor`.
    """

    tags = {"uicomponent"}

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        component_name = parser.parse_expression()

        props = []
        while parser.stream.current.type != "block_end":
            key = parser.parse_assign_target()
            parser.stream.expect("assign")
            value = parser.parse_expression()
            props.append(nodes.Keyword(key.name, value))

        body = parser.parse_statements(("name:enduicomponent",), drop_needle=True)

        return nodes.CallBlock(
            self.call_method("_render_async", [component_name], props), [], [], body
        ).set_lineno(lineno)

    async def _render_async(self, name: str, caller, **props):
        template = UIComponentRegistry.get(name)
        if not template:
            return f"<!-- UI component '{name}' not found -->"
        try:
            slot_content = await caller()
            slot = Markup(slot_content) if slot_content else Markup("")
            props["slot"] = slot
            props["children"] = slot

            tpl = self.environment.from_string(template)
            return await tpl.render_async(**props)
        except Exception as e:
            import traceback

            traceback.print_exc()
            return f"<!-- Error rendering ui component '{name}': {e} -->"


class UIComponentPreprocessor(Extension):
    """Preprocessor: converts `<ui.x prop="v">...</ui.x>` (and self-closing
    `<ui.x .../>`) into `{% uicomponent %}` tags, and `<ui-slot name="x">
    ...</ui-slot>` blocks found inside them into `{% set %}`-captured
    keyword props — see module docstring for why named slots are flattened
    into ordinary props at the text level rather than handled at runtime.
    """

    def preprocess(self, source, name, filename=None):
        return self._convert(source)

    @staticmethod
    def _parse_props(props_str: str) -> str:
        """Parses `key="value"` pairs from a `<ui.x ...>` tag's attribute
        text into `{% uicomponent %}` keyword arguments.

        HTML/Alpine.js attribute names aren't all valid Jinja2 identifiers —
        `data-foo`, `aria-label`, and Alpine's `x-data`/`:class`/`@click`
        contain hyphens/colons/at-signs that `{% uicomponent %}`'s own tag
        grammar can't accept as a keyword name (Jinja2 keyword args require
        a real identifier). Those go into a `__raw_attrs={...}` dict literal
        instead, merged straight into `attrs` unconditionally by
        `UIVarsExtension._compute_attrs` — a component could never validly
        declare e.g. `data-foo` via `{% uivars %}` anyway, so there's no
        "declared vs extra" question for these, unlike plain-identifier props.
        """
        props = []
        raw_attrs: dict[str, str] = {}
        for match in re.findall(
            r'([\w@:.-]+)=(?:"([^"]*)"|\'([^\']*)\'|(\d+\.?\d*)|(\w+))', props_str
        ):
            key = match[0]
            if match[1]:
                value, is_expr = match[1], "{{" in match[1]
            elif match[2]:
                value, is_expr = match[2], "{{" in match[2]
            elif match[3]:
                props.append(f"{key}={match[3]}") if key.isidentifier() else raw_attrs.__setitem__(key, match[3])
                continue
            else:
                lower = match[4].lower()
                literal = lower if lower in ("true", "false", "none", "null") else match[4]
                if key.isidentifier():
                    props.append(f"{key}={literal}")
                else:
                    raw_attrs[key] = match[4]
                continue

            if key.isidentifier():
                # `title="{{ page.title }}"` -> bare expression `title=page.title`:
                # `{{ }}` is Jinja2 PRINT syntax, invalid inside a `{% %}` tag.
                props.append(f'{key}="{value}"' if not is_expr else f"{key}={_as_bare_expr(value)}")
            else:
                # Un attribut hyphéné/Alpine avec une expression ({{ }}) n'est
                # pas exprimable dans un dict littéral statique — cas rare,
                # non géré (le composant devra passer la valeur autrement).
                if not is_expr:
                    raw_attrs[key] = value

        if raw_attrs:
            literal = "{" + ", ".join(f'"{k}": "{v}"' for k, v in raw_attrs.items()) + "}"
            props.append(f"__raw_attrs={literal}")

        return (" " + " ".join(props)) if props else ""

    _SLOT_RE = re.compile(r'<ui-slot\s+name="(\w+)"\s*>(.*?)</ui-slot>', re.DOTALL)

    @classmethod
    def _extract_named_slots(cls, inner: str) -> tuple[str, str, str]:
        """Pulls every `<ui-slot name="x">...</ui-slot>` out of `inner`.

        Returns `(setup, extra_props, remaining)`: `setup` is the
        `{% set %}` capture block(s) to emit before the component tag;
        `extra_props` is the `name=var` keyword list to append to the
        `{% uicomponent %}` call, PLUS a synthetic `__slot_names=[...]`
        marker so `UIVarsExtension._compute_attrs` can tell a named slot's
        value apart from a genuine HTML attribute (see its docstring —
        without this, `header=<big blob of markup>` would land in `attrs`
        indistinguishably from `id="x"`); `remaining` is `inner` with those
        slot blocks removed — the leftover markup becomes the default
        `{{ slot }}`.
        """
        setup_blocks = []
        extra_props = []
        slot_names = []
        for match in cls._SLOT_RE.finditer(inner):
            slot_name, slot_body = match.group(1), match.group(2)
            var = f"_uislot_{slot_name}"
            setup_blocks.append(f"{{% set {var} %}}{slot_body}{{% endset %}}")
            extra_props.append(f"{slot_name}={var}")
            slot_names.append(slot_name)
        if slot_names:
            names_literal = "[" + ", ".join(f'"{n}"' for n in slot_names) + "]"
            extra_props.append(f"__slot_names={names_literal}")
        remaining = cls._SLOT_RE.sub("", inner)
        return "".join(setup_blocks), " ".join(extra_props), remaining

    @classmethod
    def _convert(cls, source: str) -> str:
        # Self-closing : <ui.name attr="v" />
        source = re.sub(
            r"<ui\.(\w+)([^/]*)/>",
            lambda m: f'{{% uicomponent "{m.group(1)}"{cls._parse_props(m.group(2))} %}}{{% enduicomponent %}}',
            source,
        )

        # Blocs : <ui.name attr="v">...</ui.name> — innermost-first, comme
        # ComponentExtensions, pour supporter la composition <ui.x><ui.y/></ui.x>.
        pattern = re.compile(r"<ui\.(\w+)([^>]*)>((?:(?!<ui\.).)*?)</ui\.\1>", re.DOTALL)

        def replace(m: "re.Match") -> str:
            name, props_str, inner = m.group(1), m.group(2), m.group(3)
            setup, extra_props, remaining = cls._extract_named_slots(inner)
            props = cls._parse_props(props_str)
            if extra_props:
                props = f"{props} {extra_props}" if props else f" {extra_props}"
            return f'{setup}{{% uicomponent "{name}"{props} %}}{remaining}{{% enduicomponent %}}'

        prev = None
        while prev != source:
            prev = source
            source = re.sub(pattern, replace, source)

        return source
