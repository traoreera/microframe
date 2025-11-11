"""
Documentation UI generators
"""
from typing import Any
from starlette.responses import HTMLResponse

from ..core.config import AppConfig


class SwaggerUI:
    """Swagger UI generator"""
    
    def __init__(self, title:str):
        self.title = title

    
    def __call__(self,) -> HTMLResponse:
        
        return HTMLResponse(
            content= f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <title>{self.title} - Swagger</title>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/5.10.5/swagger-ui.min.css" />
        </head>
        <body>
            <div id="swagger-ui"></div>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/5.10.5/swagger-ui-bundle.min.js"></script>
            <script>
                SwaggerUIBundle({{
                    url: '/openapi.json',
                    dom_id: '#swagger-ui',
                    deepLinking: true,
                    presets: [SwaggerUIBundle.presets.apis],
                    layout: 'BaseLayout'
                }});
            </script>
        </body>
        </html>
        """
        )

class ReDocUI:
    """ReDoc UI generator"""
    
    def __init__(self, title):
        
        self.title = title
    
    def __call__(self)->HTMLResponse:

        return HTMLResponse(
            content=f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <title>{self.title} - ReDoc</title>
        </head>
        <body>
            <redoc spec-url="/openapi.json"></redoc>
            <script src="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"></script>
        </body>
        </html"""

        )