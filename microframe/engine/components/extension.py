import re

from jinja2 import nodes
from jinja2.ext import Extension
from markupsafe import Markup, escape

from .registry import ComponentRegistry


def _build_raw_attrs(raw_attrs: dict) -> Markup:
    """Chaîne d'attributs HTML à partir des attrs « bruts » (noms non
    identifiants — htmx `hx-*`, Alpine `x-data`/`@click`/`:class`, `data-*`).
    Valeurs échappées : elles retombent direct dans un markup généré, hors
    du filet d'autoescape du template hôte."""
    return Markup(" ".join(f'{k}="{escape(v)}"' for k, v in raw_attrs.items()))


class ComponentExtension(Extension):
    """Handles {% component "name" key=value %} ... {% endcomponent %} tags."""

    tags = {"component"}

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        component_name = parser.parse_expression()

        props = []
        while parser.stream.current.type != "block_end":
            key = parser.parse_assign_target()
            parser.stream.expect("assign")
            value = parser.parse_expression()
            props.append(nodes.Keyword(key.name, value))

        body = parser.parse_statements(("name:endcomponent",), drop_needle=True)

        return nodes.CallBlock(
            self.call_method("_render_async", [component_name], props), [], [], body
        ).set_lineno(lineno)

    async def _render_async(self, component_name: str, caller, **props):
        template = ComponentRegistry.get(component_name)
        if not template:
            return f"<!-- Component '{component_name}' not found -->"
        try:
            slot_content = await caller()
            slot = Markup(slot_content) if slot_content else Markup("")
            props["slot"] = slot
            props["children"] = slot

            # htmx/Alpine/`data-*` : les noms d'attributs non identifiants
            # (hx-get, x-data, @click…) ne peuvent pas être des kwargs Jinja2 —
            # le préprocesseur les regroupe dans `__raw_attrs` ; on les traduit
            # ici en la variable `attrs` que le template composant peut écrire.
            raw_attrs = props.pop("__raw_attrs", None) or {}
            if raw_attrs:
                props["attrs"] = _build_raw_attrs(raw_attrs)

            if hasattr(template, "render") and callable(template.render):
                template.props = props
                template.children = slot
                return template.render()

            tpl = self.environment.from_string(template)
            return await tpl.render_async(**props)
        except Exception as e:
            import traceback

            traceback.print_exc()
            return f"<!-- Error rendering component '{component_name}': {e} -->"


class ComponentExtensions(Extension):
    """Preprocessor: converts <component.X prop="v"> syntax to {% component %} tags."""

    def preprocess(self, source, name, filename=None):
        return self._convert(source)

    def _convert(self, source: str) -> str:
        def as_bare_expr(value: str) -> str:
            # A prop written as `title="{{ page.title }}"` must become the
            # BARE expression `title=page.title` inside `{% component %}` —
            # `{{ }}` is Jinja2's PRINT syntax, invalid inside a `{% %}`
            # statement tag (`title={{ page.title }}` is a syntax error).
            v = value.strip()
            return v[2:-2].strip() if v.startswith("{{") and v.endswith("}}") else v

        def parse_props(props_str: str) -> str:
            props = []
            raw_attrs: dict = {}
            for match in re.findall(
                r'([\w@:.-]+)=(?:"([^"]*)"|\'([^\']*)\'|(\d+\.?\d*)|(\w+))', props_str
            ):
                key = match[0]
                if match[1]:
                    value, is_expr = match[1], "{{" in match[1]
                elif match[2]:
                    value, is_expr = match[2], "{{" in match[2]
                elif match[3]:
                    if key.isidentifier():
                        props.append(f"{key}={match[3]}")
                    else:
                        raw_attrs[key] = match[3]
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
                    # `title="{{ page.title }}"` -> expression BARE
                    # `title=page.title` : `{{ }}` est de la syntaxe PRINT Jinja2,
                    # invalide dans un mot-clé de tag (erreur de syntaxe).
                    props.append(f'{key}="{value}"' if not is_expr else f"{key}={as_bare_expr(value)}")
                elif not is_expr:
                    # htmx/Alpine/`data-*` : nom non identifiable (hx-get,
                    # x-data, @click, :class) — impossible en keyword arg, on
                    # les regroupe pour `_render_async` (variable `attrs`).
                    raw_attrs[key] = value

            if raw_attrs:
                literal = "{" + ", ".join(f'"{k}": "{v}"' for k, v in raw_attrs.items()) + "}"
                props.append(f"__raw_attrs={literal}")
            return (" " + " ".join(props)) if props else ""

        # Self-closing. `[^<>]*` (pas `[^/]*`) : un `<component.a>...<component.b/>`
        # ne doit pas faire partir la regex du premier tag pour la fermer sur le
        # second — un `/>` de composant imbriqué avalerait les props de l'enfant.
        source = re.sub(
            r"<component\.(\w+)([^<>]*)/>",
            lambda m: f'{{% component "{m.group(1)}"{parse_props(m.group(2))} %}}{{% endcomponent %}}',
            source,
        )

        # Block components (innermost-first loop)
        pattern = re.compile(
            r"<component\.(\w+)([^>]*)>((?:(?!<component\.).)*?)</component\.\1>", re.DOTALL
        )
        prev = None
        while prev != source:
            prev = source
            source = re.sub(
                pattern,
                lambda m: f'{{% component "{m.group(1)}"{parse_props(m.group(2))} %}}{m.group(3)}{{% endcomponent %}}',
                source,
            )

        return source
