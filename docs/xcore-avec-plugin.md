# XCore + Plugin : guide complet

Guide pas à pas pour créer une application FastAPI avec XCore, des plugins, et MicroFrame comme moteur de rendu avec les tags `<remote>` et `<action>`.

## Installation

xcore n'est pas publié sur PyPI : c'est un projet séparé, installé en local (sibling repo ou éditable).

```bash
pip install -e ../xcore   # ou le chemin vers ton clone de xcore
pip install microframe fastapi
```

Il n'existe pas d'extra `microframe[xcore]` — MicroFrame ne dépend jamais de xcore ; c'est xcore qui charge MicroFrame comme extension (import paresseux des deux côtés).

## Structure du projet

Un plugin xcore n'est pas un simple fichier `.py` : c'est un dossier avec un manifeste `plugin.yaml` déclarant ses permissions et son point d'entrée, dont le module doit exposer une classe littéralement nommée `Plugin` (xcore vérifie `hasattr(module, "Plugin")` au chargement — `MonPlugin` ou tout autre nom ne serait jamais trouvé).

```
mon-app/
├── app.py                          # Point d'entrée FastAPI + XCore
├── xcore.yaml                       # Config XCore (déclare l'extension template_engine)
├── templates/
│   ├── base.html                    # Layout partagé par tous les plugins
│   └── components/
│       └── card.html                # Composant HTML commun
└── plugins/
    └── mon_plugin/
        ├── plugin.yaml               # Manifeste : version, permissions, entry_point
        ├── src/
        │   └── main.py               # class Plugin(TrustedBase) — obligatoire
        └── templates/
            └── index.html            # {% extends "base.html" %}, namespacé "mon_plugin/…"
```

## 1. Déclarer MicroFrame comme extension XCore

MicroFrame s'enregistre via le système d'extensions de xcore (`services.extensions` dans `xcore.yaml`), pas comme un plugin — c'est un service, avec un cycle de vie `init/shutdown/health_check/status`.

```yaml
# xcore.yaml
plugins:
  directory: "./plugins"

services:
  extensions:
    template_engine:
      module: microframe.engine.integration.xcore:TemplateEngineExtension
      config:
        directory: templates
        namespaces:
          mon_plugin: plugins/mon_plugin/templates
        enable_ui: false
        enable_minify: true
        enable_cache: true
        cache_ttl: 300
```

## 2. Créer un plugin XCore

Manifeste d'abord — xcore refuse tout appel par défaut (fail-closed), donc sans `permissions:` déclarées, `xcore.plugins.call(...)` renverra silencieusement `{"status": "error", "code": "permission_denied"}` plutôt qu'une exception bruyante :

```yaml
# plugins/mon_plugin/plugin.yaml
name: "mon_plugin"
version: "1.0.0"
mode: "trusted"
entry_point: "src/main.py"
permissions:
  - resource: "*"
    actions: ["execute"]
    effect: allow
```

Un plugin xcore hérite de `TrustedBase`, expose `handle(action, payload)` (pas `handle(request)`), et la classe doit s'appeler `Plugin` — c'est ce nom exact que le loader va chercher dans le module :

```python
# plugins/mon_plugin/src/main.py
from xcore.kernel.api.contract import TrustedBase


class Plugin(TrustedBase):
    """Plugin exemple avec des actions utilisables depuis les templates."""

    async def handle(self, action: str, payload: dict) -> dict:
        """Point d'entrée : dispatch manuel vers les actions ci-dessous."""
        method = getattr(self, action, None)
        if method is None:
            return {"html": "<p>Action inconnue</p>"}
        return await method(payload)

    async def list_articles(self, payload: dict) -> dict:
        articles = [
            {"id": 1, "title": "Premier article", "content": "Lorem ipsum..."},
            {"id": 2, "title": "Second article", "content": "Dolor sit amet..."},
        ]
        return {
            "html": "".join(
                f"<article><h3>{a['title']}</h3><p>{a['content']}</p></article>"
                for a in articles
            )
        }

    async def contact_form(self, payload: dict) -> dict:
        """Traite un formulaire de contact (appelée par <action>)."""
        name = payload.get("name", "")
        email = payload.get("email", "")
        message = payload.get("message", "")

        # Traitement (email, base de données, etc.)
        print(f"Contact reçu : {name} <{email}> : {message}")

        return {"html": f"<p>Merci {name}, votre message a été envoyé.</p>"}

    async def counter(self, payload: dict) -> dict:
        count = payload.get("count", "0")
        return {
            "html": f"""
            <div id="counter" class="text-2xl font-bold">{count}</div>
            <button hx-post="/_/a/increment" hx-target="#counter"
                    class="btn btn-primary">
                +1
            </button>
            """
        }

    async def increment(self, payload: dict) -> dict:
        current = int(payload.get("count", "0"))
        return {"html": str(current + 1)}
```

## 3. Configurer l'application FastAPI

Les extensions xcore sont initialisées **avant** que le supervisor de plugins existe — donc le câblage des tags `<remote>`/`<action>` et du cache se fait après `await xcore.boot(app)`, via `bind_engine()`.

```python
# app.py
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from xcore import Xcore

from microframe.engine.integration.xcore import (
    bind_engine,
    register_action_routes,
    mount_template_static,
)

xcore = Xcore(config_path="xcore.yaml")  # déclare l'extension template_engine
action_map: dict = {}
engine = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global engine

    await xcore.boot(app)          # démarre services, registry, plugin supervisor

    engine = xcore.services.get("ext.template_engine").engine
    action_map.update(bind_engine(xcore, engine, static_prefix="/static"))
    register_action_routes(app, xcore, engine, action_map, prefix="/_/a")
    mount_template_static(app, template_dir="templates", url_prefix="/static")

    yield
    await xcore.shutdown()


app = FastAPI(lifespan=lifespan)
xcore.setup(app)  # middlewares (dont TenantMiddleware) — DOIT être appelé ici,
                  # après FastAPI(lifespan=...) mais avant que l'app ne serve
                  # une requête. À l'intérieur de lifespan(), c'est trop tard :
                  # Starlette a déjà démarré et refuse d'ajouter un middleware.


@app.get("/", response_class=HTMLResponse)
@app.get("/{path:path}", response_class=HTMLResponse)
async def render_page(request: Request, path: str = "index"):
    template_name = f"{path}.html" if not path.endswith(".html") else path

    ctx = {
        "request": request,
        "current_path": request.url.path,
    }

    html = await engine.render(template_name, ctx)
    return HTMLResponse(html)
```

Les plugins eux-mêmes (ex: `mon_plugin`) sont chargés par xcore selon son propre mécanisme de découverte (répertoire `plugins/` de `xcore.yaml`, un sous-dossier par plugin avec son `plugin.yaml`) — voir la doc xcore pour le détail, ça ne change pas avec cette intégration.

## 4. Templates avec remote et action

### Layout de base

```html
<!DOCTYPE html>
<html lang="fr" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{ title|default("Mon App") }}</title>
  <link rel="stylesheet" href="{{ static('app.css') }}">
  <script src="https://unpkg.com/htmx.org@2"></script>
</head>
<body>
  <header>
    <nav>
      <a href="/">Accueil</a>
      <a href="/about">À propos</a>
      <a href="/contact">Contact</a>
      <a href="/counter">Compteur</a>
    </nav>
  </header>

  <main>
    {{ content|default("") }}
  </main>

  {% block content %}{% endblock %}
</body>
</html>
```

### Page d'accueil avec remote

```html
<!-- templates/index.html -->
{% extends "base.html" %}

{% block content %}
<h1>Bienvenue</h1>

<section id="articles">
  <h2>Derniers articles</h2>
  <remote name="mon_plugin.list_articles">
    <p>Chargement des articles…</p>
  </remote>
</section>

<section id="counter-demo">
  <h2>Compteur HTMX</h2>
  <remote name="mon_plugin.counter" count="0">
    <p>Chargement du compteur…</p>
  </remote>
</section>
{% endblock %}
```

### Page de contact avec action

```html
<!-- templates/contact.html -->
{% extends "base.html" %}

{% block content %}
<h1>Contact</h1>

<action name="mon_plugin.contact_form" redirect="/merci">
  <div class="form-group">
    <label for="name">Nom</label>
    <input type="text" name="name" id="name" required>
  </div>

  <div class="form-group">
    <label for="email">Email</label>
    <input type="email" name="email" id="email" required>
  </div>

  <div class="form-group">
    <label for="message">Message</label>
    <textarea name="message" id="message" rows="5" required></textarea>
  </div>

  <button type="submit" class="btn btn-primary">Envoyer</button>
</action>
{% endblock %}
```

### Page de remerciement

```html
<!-- templates/merci.html -->
{% extends "base.html" %}

{% block content %}
<h1>Merci !</h1>
<p>Votre message a bien été envoyé. Nous vous répondrons dans les plus brefs délais.</p>
<a href="/" class="btn">Retour à l'accueil</a>
{% endblock %}
```

### Compteur avec HTMX (action self-closing + remote)

```html
<!-- templates/counter.html -->
{% extends "base.html" %}

{% block content %}
<h1>Compteur interactif</h1>

<div class="counter-demo">
  <remote name="mon_plugin.counter" count="0">
    <p>Chargement…</p>
  </remote>
</div>

<!-- action self-closing : incrémente sans formulaire -->
<action name="mon_plugin.increment"
       hx_post="true"
       hx_target="#counter"
       hx_swap="outerHTML">
  <button class="btn btn-primary">+1</button>
</action>
{% endblock %}
```

## 5. Lancer l'application

```bash
uvicorn app:app --reload --port 8000
```

Ouvrir http://localhost:8000.

## 6. Plugin qui utilise le moteur de templates

Un plugin accède au moteur MicroFrame via `get_service()` (synchrone) en ciblant l'extension par son nom xcore (`ext.<nom>`). Là encore, la classe doit s'appeler `Plugin` (`plugins/article_plugin/plugin.yaml` + `entry_point: src/main.py`, avec les mêmes `permissions:` que plus haut) :

```python
# plugins/article_plugin/src/main.py
from xcore.kernel.api.contract import TrustedBase


class Plugin(TrustedBase):
    async def handle(self, action: str, payload: dict) -> dict:
        method = getattr(self, action, None)
        return await method(payload) if method else {"html": ""}

    async def list(self, payload: dict) -> dict:
        engine = self.get_service("ext.template_engine").engine

        articles = [
            {"title": "Article 1", "content": "Contenu..."},
            {"title": "Article 2", "content": "Contenu..."},
        ]

        # "article_plugin/…" : résolu via le namespace déclaré dans xcore.yaml
        # pour ce plugin (voir §1) — évite toute collision avec un composant
        # "components/article_list.html" d'un autre plugin.
        html = await engine.render("article_plugin/components/article_list.html", {"articles": articles})
        return {"html": html}

    async def detail(self, payload: dict) -> dict:
        engine = self.get_service("ext.template_engine").engine
        article_id = payload.get("id")

        html = await engine.render("article_plugin/components/article_detail.html", {
            "article": {"id": article_id, "title": "Article", "content": "..."}
        })
        return {"html": html}
```

## 7. API de l'intégration

### `TemplateEngineExtension`

Classe `BaseService` xcore, déclarée dans `xcore.yaml` sous `services.extensions.<nom>.module`. `config:` est passé tel quel aux kwargs de `TemplateEngine` (`directory`, `debug`, `enable_minify`, `enable_cache`, `enable_ui`, `cache_ttl`, `mfe_timeout`).

Accessible via :
```python
xcore.services.get("ext.template_engine").engine   # depuis le code applicatif
self.get_service("ext.template_engine").engine      # depuis un plugin TrustedBase
```

### `bind_engine(xcore_instance, engine, static_prefix="/static")`

À appeler **après** `await xcore.boot(app)` (services et plugin supervisor doivent exister). Fait automatiquement :

| Élément | Description |
|---|---|
| Cache | Bridge vers `xcore.services.get("cache")` si le service cache est configuré |
| `_remote_caller` | Injecté dans `engine.env.globals`, résout `xcore.plugins.call(plugin, action, kwargs)` à chaque render |
| `_action_resolver` | Génère des URLs opaques `/_/a/<token>`, stockées dans la map retournée |
| `static()` | Helper `XCoreStatic` avec préfixe et versionnement d'assets |

Retourne la map de tokens `{token: (plugin, action)}`, à passer à `register_action_routes`.

### `register_action_routes(app, xcore_instance, engine, action_map, prefix="/_/a")`

Enregistre `POST /_/a/<token>` sur l'application FastAPI.

Ce que fait la route :

1. Résout `(plugin, action)` depuis `action_map[token]`
2. Reçoit les données du formulaire
3. Valide le CSRF contre `engine.csrf_token`
4. Lit `request.state.tenant_id` (posé par le `TenantMiddleware` de xcore via `xcore.setup(app)`)
5. Appelle `xcore.plugins.call(plugin, action, form_data, tenant_id=tenant_id)`
6. Si `redirect` est présent, redirige (303) — sinon retourne le HTML

### `mount_template_static(app, template_dir, url_prefix="/static")`

Monte le dossier `templates/static/` sur l'application FastAPI, s'il existe.

## 8. Résumé du flux

```
Template avec <remote>
        │
        ▼
MicroFrame rend le template
        │
        ▼
Tag <remote> → appelle _remote_caller (injecté par bind_engine)
        │
        ▼
xcore.plugins.call("plugin", "action", kwargs)
        │
        ▼
TrustedBase.handle(action, payload) → retourne {"html": "..."}
        │
        ▼
HTML inséré dans le template


Template avec <action>
        │
        ▼
MicroFrame génère un <form> avec URL opaque /_/a/<token> (via _action_resolver)
        │
        ▼
Soumission du formulaire → POST /_/a/<token>
        │
        ▼
register_action_routes vérifie le CSRF (engine.csrf_token) et lit le tenant
        │
        ▼
xcore.plugins.call("plugin", "action", form_data, tenant_id=...)
        │
        ▼
TrustedBase.handle(action, payload) → {"html": "..."} ou redirect
```
