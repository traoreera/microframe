from app.app import router
from starlette.middleware.cors import CORSMiddleware

from microframe import AppConfig, Application

app = Application(
    AppConfig(
        title="MicroFrame",
        version="2.0.0",
        description="A modern ASGI microframe",
        debug=True,
    )
)


app = Application(configuration=AppConfig("AuthX", "1.0.0"))
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Votre frontend
    allow_credentials=True,  # ⚠️ IMPORTANT pour les cookies
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
