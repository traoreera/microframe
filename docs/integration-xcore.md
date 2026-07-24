# Intégration XCore

Commence par `guide.md` si tu veux voir le flux de base, puis reviens ici pour brancher MicroFrame sur FastAPI et XCore.

XCore est un framework de plugins pour FastAPI. MicroFrame peut s'y intégrer pour utiliser les plugins comme backends pour les tags `<remote>` et `<action>`.

## Installation

```bash
pip install microframe[xcore]
```

## Création du moteur

```python
from fastapi import FastAPI
from xcore import Xcore
from microframe.engine.integration.xcore import (
    create_xcore_engine,
    register_action_routes,
    register_engine_service,
    mount_template_static,
)

app = FastAPI()
xcore = Xcore(app)

engine = create_xcore_engine(
    xcore_instance=xcore,
    directory="templates",
    enable_ui=True,
    enable_minify=True,
    enable_cache=True,
    cache_ttl=300,
    static_prefix="/static",
)
```

## Routes d'action

```python
register_action_routes(app, prefix="/_/a")
```

Enregistre `POST /_/a/<token>` qui :
1. Reçoit les données du formulaire
2. Valide le token CSRF
3. Appelle le plugin xcore correspondant
4. Redirige ou retourne du HTML

## Service de template

```python
register_engine_service(xcore, engine, service_name="template_engine")
```

Permet aux plugins xcore d'accéder au moteur :

```python
class MyPlugin(Plugin):
    async def handle(self, request):
        engine = await self.get_service("template_engine")
        html = await engine.render("page.html", {"key": "value"})
        return {"html": html}
```

## Fichiers statiques

```python
mount_template_static(app, template_dir="templates", url_prefix="/static")
```

Sert automatiquement `templates/static/` si le dossier existe.

## Cache

```python
class XCoreCacheBackend(CacheBackend):
    """Bridge entre microframe et le cache xcore."""
```

Utilisé automatiquement par `create_xcore_engine` si xcore dispose d'un service de cache.

## Helper static

```python
class XCoreStatic:
    """Builds static URLs with mount prefix and asset versioning."""

engine.add_global("static", XCoreStatic(mount_prefix="/static"))
```

```html
<link rel="stylesheet" href="{{ static('app.css') }}">
```
