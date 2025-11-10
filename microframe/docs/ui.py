"""
Documentation UI generators
"""
from starlette.responses import HTMLResponse

from ..core.config import AppConfig


class SwaggerUI:
    """Swagger UI generator"""
    
    def __init__(self, config: AppConfig):
        self.config = config
    
    def render(self) -> HTMLResponse:
        """Render Swagger UI HTML"""
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{self.config.title} - API Documentation</title>
            <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/5.10.5/swagger-ui.min.css" />
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                }}
            </style>
        </head>
        <body>
            <div id="swagger-ui"></div>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/5.10.5/swagger-ui-bundle.min.js" crossorigin></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/5.10.5/swagger-ui-standalone-preset.min.js" crossorigin></script>
            <script>
                window.onload = function() {{
                    const ui = SwaggerUIBundle({{
                        url: '{self.config.openapi_url}',
                        dom_id: '#swagger-ui',
                        deepLinking: true,
                        presets: [
                            SwaggerUIBundle.presets.apis,
                            SwaggerUIStandalonePreset
                        ],
                        layout: "StandaloneLayout"
                    }});
                    window.ui = ui;
                }};
            </script>
        </body>
        </html>
        """
        return HTMLResponse(html)


class ReDocUI:
    """ReDoc UI generator"""
    
    def __init__(self, config: AppConfig):
        self.config = config
    
    def render(self) -> HTMLResponse:
        """Render ReDoc UI HTML"""
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{self.config.title} - API Documentation</title>
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                }}
            </style>
        </head>
        <body>
            <redoc spec-url='{self.config.openapi_url}'></redoc>
            <script src="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"></script>
        </body>
        </html>
        """
        return HTMLResponse(html)
