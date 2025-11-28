from pathlib import Path

import jinja2
from starlette.requests import Request
from starlette.responses import HTMLResponse

from .components import ComponentExtension, auto_register_components


class TemplateEngine:
    _instance = None

    def __init__(self, directory="templates", debug=True, cache: bool = False):
        self.directory = directory
        cache_dir = Path(".jinja_cache")

        if not cache_dir.exists():
            cache_dir.mkdir(parents=True, exist_ok=True)
        auto_register_components(f"{directory}/components")
        if cache:
            self.env = jinja2.Environment(
                loader=jinja2.FileSystemLoader(directory),
                auto_reload=debug,
                enable_async=True,
                bytecode_cache=jinja2.FileSystemBytecodeCache(str(cache_dir)),
                trim_blocks=True,
                lstrip_blocks=True,
                autoescape=True
            )
        else:
            self.env = jinja2.Environment(
                loader=jinja2.FileSystemLoader(directory),
                auto_reload=debug,
                enable_async=True,
                trim_blocks=True,
                lstrip_blocks=True,
                autoescape=True
            )

        self.env.add_extension(ComponentExtension)

        self.env.globals.update(
            {
                "static": lambda path: f"/static/{path}",
                "url": lambda name: f"/{name}",
            }
        )

    async def render(self, template_name, ctx: dict = None, request: Request = None):
        ctx = ctx or {}
        ctx["request"] = request

        is_htmx = request and request.headers.get("HX-Request")

        if is_htmx:
            partial = f"partials/{template_name}"
            if Path(f"templates/{partial}").exists():
                template_name = partial
            print(f"Rendering partial: {partial}")

        try:
            template = self.env.get_template(template_name)
            html = await template.render_async(**ctx)
            return HTMLResponse(html)

        except Exception as ex:
            return HTMLResponse(f"<pre>{ex}</pre>", status_code=500)

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


def get_engine():
    return TemplateEngine.instance()


def render(template_name, ctx: dict = None, request: Request = None):
    return get_engine().render(template_name, ctx, request)


def list_templates():
    return get_engine().env.list_templates()
