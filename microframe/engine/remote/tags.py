from jinja2 import nodes
from jinja2.ext import Extension
from markupsafe import Markup, escape


class RemoteExtension(Extension):
    """Handles {% remote "plugin.action" key=val %}...{% endremote %} tags.

    Calls the registered _remote_caller function at render time.
    If no caller is registered or it returns nothing, renders the body as fallback.
    """

    tags = {"remote"}

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        name = parser.parse_expression()

        props = []
        while parser.stream.current.type != "block_end":
            key = parser.parse_assign_target()
            parser.stream.expect("assign")
            value = parser.parse_expression()
            props.append(nodes.Keyword(key.name, value))

        body = parser.parse_statements(("name:endremote",), drop_needle=True)

        return nodes.CallBlock(
            self.call_method("_render", [name], props), [], [], body
        ).set_lineno(lineno)

    async def _render(self, name: str, caller, **kwargs) -> str:
        caller_func = self.environment.globals.get("_remote_caller")
        if caller_func:
            result = await caller_func(name, kwargs)
            if result is not None:
                return Markup(result)

        body = await caller()
        fallback = body.strip() if body else ""
        return fallback or f"<!-- remote '{name}' not available -->"


class ActionExtension(Extension):
    """Handles {% action "plugin.action" redirect="/" %}...{% endaction %} tags.

    Generates a <form> with opaque action URL, CSRF token, and optional HTMX attrs.
    """

    tags = {"action"}

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        name = parser.parse_expression()

        props = []
        while parser.stream.current.type != "block_end":
            key = parser.parse_assign_target()
            parser.stream.expect("assign")
            value = parser.parse_expression()
            props.append(nodes.Keyword(key.name, value))

        body = parser.parse_statements(("name:endaction",), drop_needle=True)

        return nodes.CallBlock(
            self.call_method("_render_form", [name], props), [], [], body
        ).set_lineno(lineno)

    async def _render_form(self, name: str, caller, **kwargs) -> str:
        resolver = self.environment.globals.get("_action_resolver")
        csrf_fn = self.environment.globals.get("csrf_token")

        url = escape(resolver(name, kwargs) if resolver else "#")
        method = escape(kwargs.get("method", "POST").upper())
        redirect = escape(kwargs.get("redirect", ""))
        htmx = self._build_htmx(kwargs)
        token = escape(csrf_fn() if csrf_fn else "")

        if kwargs.get("hx_post") or kwargs.get("hx_get"):
            hx_verb = "hx-get" if kwargs.get("hx_get") else "hx-post"
            htmx += f' {hx_verb}="{url}"'

        body = await caller()
        parts = [f'<form action="{url}" method="{method}"{htmx}>']
        parts.append(f'<input type="hidden" name="csrf_token" value="{token}">')
        if redirect:
            parts.append(f'<input type="hidden" name="redirect" value="{redirect}">')
        parts.append(body)
        parts.append("</form>")
        return Markup("".join(parts))

    @staticmethod
    def _build_htmx(kwargs: dict) -> str:
        mapping = {
            "hx_target": "hx-target",
            "hx_swap": "hx-swap",
            "hx_trigger": "hx-trigger",
            "hx_push_url": "hx-push-url",
            "hx_select": "hx-select",
            "hx_select_oob": "hx-select-oob",
            "hx_confirm": "hx-confirm",
            "hx_on": "hx-on",
        }
        attrs = []
        for py_key, html_key in mapping.items():
            val = kwargs.get(py_key)
            if val:
                attrs.append(f'{html_key}="{escape(val)}"')
        return " " + " ".join(attrs) if attrs else ""
