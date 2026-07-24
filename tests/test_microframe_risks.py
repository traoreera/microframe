import asyncio

from microframe import TemplateEngine, UIComponent, ui_register
from microframe.engine.ui import ComponentRegistry, render_microui


def test_ui_components_do_not_share_state_between_renders():
    ComponentRegistry.clear()

    @ui_register
    class Counter(UIComponent):
        def render(self):
            calls = getattr(self, "_calls", 0) + 1
            self._calls = calls
            return "{}:{}:{}".format(self.props.get("label", ""), calls, self.children or "")

    try:
        first = str(render_microui("counter", label="A"))
        second = str(render_microui("counter", label="B"))

        assert first == "A:1:"
        assert second == "B:1:"
    finally:
        ComponentRegistry.clear()


def test_csrf_token_is_stable_per_engine(tmp_path):
    engine = TemplateEngine(directory=str(tmp_path))
    token = engine.env.globals["csrf_token"]()

    assert token == engine.env.globals["csrf_token"]()
    assert token != TemplateEngine(directory=str(tmp_path)).env.globals["csrf_token"]()
    assert len(token) >= 40


def test_action_extension_escapes_html_attributes(tmp_path):
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()

    template_path = templates_dir / "page.html"
    template_path.write_text("""
{% action "save" redirect="\"><img src=x onerror=1>" hx_target="panel\"><svg/onload=1>" %}
  <button>Save</button>
{% endaction %}
""".strip())

    engine = TemplateEngine(
        directory=str(templates_dir),
        action_resolver=lambda name, kwargs: "\"/><script>alert(1)</script>",
    )
    html = asyncio.run(engine.render("page.html", {}))

    assert "<script>alert(1)</script>" not in html
    assert "<img src=x onerror=1>" not in html
    assert "<svg/onload=1>" not in html
    assert "<button>Save</button>" in html
