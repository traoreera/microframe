# Intégration XCore

XCore est un framework de plugins pour FastAPI. MicroFrame s'y intègre comme une véritable **extension xcore** (`BaseService`), pas comme un plugin — c'est un service de rendu, pas une unité métier.

→ **Guide complet avec plugin pas à pas** : [xcore-avec-plugin](xcore-avec-plugin.md)

## Installation

xcore n'est pas publié sur PyPI — c'est un projet séparé, à installer en local (ex. sibling repo) :

```bash
pip install -e ../xcore
pip install microframe fastapi
```

## Déclaration de l'extension

```yaml
# xcore.yaml
services:
  extensions:
    template_engine:
      module: microframe.engine.integration.xcore:TemplateEngineExtension
      config:
        directory: templates          # base.html et layouts partagés
        namespaces:                   # un dossier de templates par plugin
          blog: plugins/blog/templates
          crm: plugins/crm/templates
        enable_ui: true
        enable_minify: true
        enable_cache: true
        cache_ttl: 300
```

## Plusieurs plugins, un seul `base.html`

`directory` est le chemin de recherche partagé (layouts communs, `base.html`). `namespaces` associe un préfixe à un dossier de templates par plugin : `blog/index.html` charge `plugins/blog/templates/index.html`, `crm/index.html` charge `plugins/crm/templates/index.html` — sans collision même si les deux plugins ont chacun un `index.html`. Chaque template de plugin peut faire `{% extends "base.html" %}` normalement, résolu depuis le dossier partagé.

Sans `namespaces` (juste une liste de dossiers dans `directory`), les dossiers sont fusionnés en un seul chemin de recherche plat : ça marche tant que les noms de fichiers ne se répètent pas entre plugins, mais le premier trouvé gagne silencieusement en cas de collision — préférer `namespaces` dès qu'il y a plus d'un plugin.

### Composants : partagés, mais pas namespacés

`ComponentRegistry` (les fichiers de `components/`, utilisables via `{% component "name" %}` ou `<component.name>`) est un registre **global au process**, à plat, indépendant du `namespaces` ci-dessus — un composant `card.html` défini dans `plugins/blog/templates/components/` et un autre dans `plugins/crm/templates/components/` collisionnent sur le même nom `card`. `ComponentRegistry.register()` logge un warning quand ça arrive (contenu différent sous le même nom) au lieu d'écraser silencieusement, mais la résolution reste la responsabilité de l'auteur du plugin : nommer les fichiers de composants spécifiques à un plugin de façon unique (ex. `blog_card.html`, `crm_card.html`). Les composants vraiment communs (boutons, layout…) doivent vivre dans le dossier `components/` du `directory` partagé, où ils sont réutilisables par tous les plugins sans risque de collision.

## Câblage de l'application

Les extensions xcore sont initialisées **avant** que le plugin supervisor existe (ordre du boot : services → registry → plugins), donc les tags `<remote>`/`<action>` et le pont vers le cache xcore sont câblés séparément, **après** `await xcore.boot(app)`.

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from xcore import Xcore

from microframe.engine.integration.xcore import (
    bind_engine,
    register_action_routes,
    mount_template_static,
)

xcore = Xcore(config_path="xcore.yaml")
action_map: dict = {}
engine = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global engine
    await xcore.boot(app)

    engine = xcore.services.get("ext.template_engine").engine
    action_map.update(bind_engine(xcore, engine, static_prefix="/static"))
    register_action_routes(app, xcore, engine, action_map, prefix="/_/a")
    mount_template_static(app, template_dir="templates", url_prefix="/static")

    yield
    await xcore.shutdown()

app = FastAPI(lifespan=lifespan)
xcore.setup(app)  # middlewares (TenantMiddleware…) — must run before the app
                  # starts serving, NOT inside lifespan() (Starlette raises
                  # "Cannot add middleware after an application has started"
                  # otherwise: by the time lifespan() runs, it's too late)
```

## Permissions des plugins (fail-closed)

xcore refuse tout appel de plugin par défaut (`resource=<action>, action="execute"` évalué contre le `permissions:` du manifeste — aucune règle = deny). Un `plugin.yaml` avec `permissions: []` bloque silencieusement **tous** ses appels (`{"status": "error", "code": "permission_denied", ...}`, jamais une exception qui remonterait bruyamment). Pour un plugin qui expose juste des actions de rendu appelées depuis l'app elle-même, autoriser explicitement :

```yaml
# plugins/mon_plugin/plugin.yaml
permissions:
  - resource: "*"
    actions: ["execute"]
    effect: allow
```

## Routes d'action

`register_action_routes(app, xcore, engine, action_map, prefix="/_/a")` enregistre `POST /_/a/<token>` qui :
1. Résout `(plugin, action)` depuis la map de tokens générée par `bind_engine`
2. Reçoit les données du formulaire
3. Valide le token CSRF contre `engine.csrf_token`
4. Appelle `xcore.plugins.call(plugin, action, form_data, tenant_id=request.state.tenant_id)`
5. Redirige ou retourne du HTML

## Accès depuis un plugin

```python
from xcore.kernel.api.contract import TrustedBase

class MyPlugin(TrustedBase):
    async def handle(self, action: str, payload: dict) -> dict:
        engine = self.get_service("ext.template_engine").engine  # synchrone
        html = await engine.render("page.html", payload)
        return {"html": html}
```

## Fichiers statiques

```python
mount_template_static(app, template_dir="templates", url_prefix="/static")
```

Sert automatiquement `templates/static/` si le dossier existe.

## Cache

`XCoreCacheBackend` fait le pont entre le cache microframe et le `CacheService` de xcore. Câblé automatiquement par `bind_engine()` si `xcore.services.has("cache")`.

Le `CacheService` de xcore est async par nature (`await cache.get(key)`). `XCoreCacheBackend` ne fait aucune gymnastique `asyncio.run()` pour se faire passer pour un backend synchrone — ses méthodes renvoient directement les coroutines de `CacheService`. `TemplateEngine.render()` les attend lui-même via un petit helper (`_maybe_await`, dans `renderer.py`) qui `await` le résultat si c'est awaitable, et le laisse passer tel quel sinon (cas du `CacheManager` intégré, purement sync). C'est ce qui permet à n'importe quel `CacheBackend` d'être sync ou async sans que `TemplateEngine` ait besoin de le savoir à l'avance.

## Helper static

`XCoreStatic` construit des URLs avec préfixe de montage et versionnement d'assets.

```html
<link rel="stylesheet" href="{{ static('app.css') }}">
```
