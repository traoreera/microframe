"""`<ui.x>` components (attrs pass-through + named slots) — engine.components.ui_kit.

Covers the real bugs found while building this: Jinja2 hoists free-variable
resolution to the top of the compiled function, so a runtime-only
`context.vars` mutation (no static `Assign` node) is invisible to later
`{{ name }}` reads in the SAME template — this bit both defaults (silently
never applied) and `attrs` (always empty) until `UIVarsExtension` was
rewritten to emit real `Assign` nodes instead of an opaque method call.
"""

import jinja2
import pytest

from microframe.engine.components.extension import ComponentExtensions
from microframe.engine.components.ui_kit import (
    UIComponentExtension,
    UIComponentPreprocessor,
    UIComponentRegistry,
    UIVarsExtension,
)


@pytest.fixture
def env():
    e = jinja2.Environment(enable_async=True, autoescape=True)
    e.add_extension(UIVarsExtension)
    e.add_extension(UIComponentExtension)
    e.add_extension(UIComponentPreprocessor)
    return e


async def _render(env, source, **ctx):
    return await env.from_string(source).render_async(**ctx)


@pytest.mark.asyncio
async def test_attrs_passthrough_for_undeclared_props(env):
    UIComponentRegistry.register("badge", '{% uivars text="" color="ink" %}<span {{ attrs }}>{{ text }}</span>')
    out = await _render(env, '<ui.badge text="Hi" id="b1" />')
    assert out == '<span id="b1">Hi</span>'


@pytest.mark.asyncio
async def test_declared_prop_defaults_apply_when_not_passed(env):
    UIComponentRegistry.register(
        "badge2", '{% uivars text="" color="ink" %}<span class="badge-{{ color }}">{{ text }}</span>'
    )
    out = await _render(env, '<ui.badge2 id="b2" />')
    assert out == '<span class="badge-ink"></span>'


@pytest.mark.asyncio
async def test_declared_prop_overrides_default_when_passed(env):
    UIComponentRegistry.register("badge3", '{% uivars color="ink" %}<span class="badge-{{ color }}"></span>')
    out = await _render(env, '<ui.badge3 color="green" />')
    assert out == '<span class="badge-green"></span>'


@pytest.mark.asyncio
async def test_named_slot_becomes_a_template_variable_not_an_attr(env):
    UIComponentRegistry.register(
        "card",
        '{% uivars title="" %}<div {{ attrs }}>'
        '{% if header %}<div class="head">{{ header }}</div>{% endif %}'
        "{{ slot }}</div>",
    )
    out = await _render(
        env,
        '<ui.card title="X" data-testid="c1">'
        '<ui-slot name="header">H</ui-slot>'
        "Body"
        "</ui.card>",
    )
    assert out == '<div data-testid="c1"><div class="head">H</div>Body</div>'


@pytest.mark.asyncio
async def test_hyphenated_and_alpine_attrs_pass_through(env):
    UIComponentRegistry.register("btn", "{% uivars %}<button {{ attrs }}>{{ slot }}</button>")
    out = await _render(env, '<ui.btn data-testid="save" aria-label="Save" x-data="{}">Go</ui.btn>')
    assert 'data-testid="save"' in out
    assert 'aria-label="Save"' in out
    assert 'x-data="{}"' in out


@pytest.mark.asyncio
async def test_attrs_value_is_html_escaped(env):
    UIComponentRegistry.register("badge4", "{% uivars %}<span {{ attrs }}></span>")
    out = await _render(env, '<ui.badge4 title="a&quot;b" />')
    assert "&amp;quot;" in out or "&#34;" in out or "&quot;" in out
    assert '"a"' not in out  # the raw quote must never break out of the attribute


@pytest.mark.asyncio
async def test_prop_passed_as_jinja_expression(env):
    UIComponentRegistry.register("badge5", "{% uivars text=\"\" %}<span>{{ text }}</span>")
    out = await _render(env, '<ui.badge5 text="{{ dangerous }}" />', dangerous="<script>x</script>")
    assert out == "<span>&lt;script&gt;x&lt;/script&gt;</span>"


def test_component_extensions_expression_attr_regression():
    """The plain (pre-existing) <component.x> syntax had the same bug —
    `title="{{ page.title }}"` compiled to the syntactically invalid
    `title={{ page.title }}` (`{{ }}` is print syntax, illegal inside a
    `{% %}` tag). Fixed alongside ui_kit since it's the same root cause."""
    env = jinja2.Environment()
    ext = ComponentExtensions(env)
    out = ext._convert('<component.card title="{{ page.title }}">body</component.card>')
    assert out == '{% component "card" title=page.title %}body{% endcomponent %}'


def test_ui_component_preprocessor_self_closing_expression_attr():
    out = UIComponentPreprocessor._convert('<ui.badge text="{{ page.title }}" />')
    assert out == '{% uicomponent "badge" text=page.title %}{% enduicomponent %}'
