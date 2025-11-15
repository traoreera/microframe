from starlette.requests import Request

from microframe import Depends, Router
from microframe.ui import ComponentRegistry, TemplateEngine, get_engine

from .custom_templates.compoments import UI

template = TemplateEngine(cache=True, debug=True).instance()

# your custon extension compoment with python
ComponentRegistry.register("button", UI.button)
ComponentRegistry.register("badge", UI.badge)


router = Router(
    prefix="/demo_ui",
    tags=["Demo UI"],
)


@router.get("/")
async def demo_ui(request: Request):

    ip = request.client.host
    print(ip)
    return await template.render("index.html", {"ip_addr": f"{ip}"})
