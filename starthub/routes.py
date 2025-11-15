from starlette.requests import Request
from starlette.responses import FileResponse

from microframe import Depends, Router
from microframe.ui import TemplateEngine, get_engine

router = Router(prefix="/starthub", tags=["Starthub"])


@router.get("/")
async def index(request: Request, template: TemplateEngine = Depends(get_engine)):
    return await template.render("pages/starthub.html")


@router.get("/sw.js")
async def sw(request: Request, template: TemplateEngine = Depends(get_engine)):
    import os

    file = os.path.join(os.curdir, "templates", "js", "ws.js")
    if os.path.exists(file):
        return FileResponse(file, 200)
    print("file not found")
    return ""
