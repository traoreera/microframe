from microframe import Application, AppConfig, Router
from examples.template_testing import router


app = Application(
    configuration=AppConfig(
        title="My API",
        version="1.0.0",
        description="A sample API",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )
)


app.include_router(router,tags=["Template Testing"])