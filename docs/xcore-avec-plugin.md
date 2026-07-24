# XCore + Plugin : guide complet

Guide pas à pas pour créer une application FastAPI avec XCore, des plugins, et MicroFrame comme moteur de rendu avec les tags `<remote>` et `<action>`.

## Installation

```bash
pip install microframe[xcore]
```

Installe microframe, fastapi, xcore et httpx.

## Structure du projet

```
mon-app/
├── app.py                 # Point d'entrée FastAPI + XCore
├── templates/
│   ├── index.html          # Page d'accueil
│   ├── base.html           # Layout de base
│   └── components/
│       └── card.html       # Composant HTML
├── plugins/
│   └── mon_plugin.py       # Plugin XCore
└── static/
    └── app.css             # Fichiers statiques
```

## 1. Créer un plugin XCore

Un plugin XCore est une classe qui hérite de `Plugin` et expose des méthodes appelables via `plugin.action`.

```python
# plugins/mon_plugin.py
from xcore import Plugin


class MonPlugin(Plugin):
    """Plugin exemple avec des actions utilisables depuis les templates."""

    async def handle(self, request):
        """Point d'entrée principal (appelé par défaut)."""
        return {"html": "<p>Plugin principal</p>"}

    async def list_articles(self, request):
        """Action : retourne une liste d'articles."""
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

    async def contact_form(self, request):
        """Action : traite un formulaire de contact (appelée par <action>)."""
        data = request.get("data", {})
        name = data.get("name", "")
        email = data.get("email", "")
        message = data.get("message", "")

        # Traitement (email, base de données, etc.)
        print(f"Contact reçu : {name} <{email}> : {message}")

        return {
            "html": f"<p>Merci {name}, votre message a été envoyé.</p>"
        }

    async def counter(self, request):
        """Action : page avec compteur interactif."""
        count = request.get("data", {}).get("count", "0")
        return {
            "html": f"""
            <div id="counter" class="text-2xl font-bold">{count}</div>
            <button hx-post="/_/a/increment" hx-target="#counter"
                    class="btn btn-primary">
                +1
            </button>
            """
        }

    async def increment(self, request):
        """Action : incrémente le compteur."""
        current = int(request.get("data", {}).get("count", "0"))
        return {"html": str(current + 1)}
```

## 2. Configurer l'application FastAPI

```python
# app.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from xcore import Xcore

from microframe.engine.integration.xcore import (
    create_xcore_engine,
    register_action_routes,
    register_engine_service,
    mount_template_static,
)

from plugins.mon_plugin import MonPlugin

app = FastAPI()

# 1. Initialiser XCore
xcore = Xcore(app)

# 2. Enregistrer le plugin
xcore.register(MonPlugin, "mon_plugin")

# 3. Créer le moteur de templates branché sur XCore
engine = create_xcore_engine(
    xcore_instance=xcore,
    directory="templates",
    enable_ui=False,
    enable_minify=True,
    enable_cache=True,
    cache_ttl=300,
    debug=True,
)

# 4. Enregistrer les routes d'action (formulaires <action>)
register_action_routes(app, prefix="/_/a")

# 5. Enregistrer le moteur comme service accessible depuis les plugins
register_engine_service(xcore, engine, service_name="template_engine")

# 6. Monter les fichiers statiques
mount_template_static(app, template_dir="templates", url_prefix="/static")


# 7. Route principale : rend le template avec MicroFrame
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

## 3. Templates avec remote et action

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

## 4. Lancer l'application

```bash
uvicorn app:app --reload --port 8000
```

Ouvrir http://localhost:8000.

## 5. Plugin qui utilise le moteur de templates

Un plugin peut accéder au moteur MicroFrame pour rendre des templates :

```python
# plugins/article_plugin.py
from xcore import Plugin


class ArticlePlugin(Plugin):
    async def list(self, request):
        engine = await self.get_service("template_engine")

        articles = [
            {"title": "Article 1", "content": "Contenu..."},
            {"title": "Article 2", "content": "Contenu..."},
        ]

        html = await engine.render("components/article_list.html", {
            "articles": articles
        })
        return {"html": html}

    async def detail(self, request):
        engine = await self.get_service("template_engine")
        article_id = request.get("data", {}).get("id")

        html = await engine.render("components/article_detail.html", {
            "article": {"id": article_id, "title": "Article", "content": "..."}
        })
        return {"html": html}
```

## 6. Exemple complet avec sessions et base de données

```python
# app.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from xcore import Xcore

from microframe.engine.integration.xcore import (
    create_xcore_engine,
    register_action_routes,
    register_engine_service,
    mount_template_static,
)

from plugins.auth_plugin import AuthPlugin
from plugins.blog_plugin import BlogPlugin
from plugins.cart_plugin import CartPlugin

app = FastAPI()
xcore = Xcore(app)

# Enregistrer les plugins
xcore.register(AuthPlugin, "auth")
xcore.register(BlogPlugin, "blog")
xcore.register(CartPlugin, "cart")

# Créer le moteur
engine = create_xcore_engine(
    xcore_instance=xcore,
    directory="templates",
    enable_ui=True,
    enable_minify=True,
    enable_cache=True,
)

register_action_routes(app)
register_engine_service(xcore, engine)
mount_template_static(app, "templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    html = await engine.render("home.html", {
        "request": request,
    })
    return HTMLResponse(html)
```

### Template avec plusieurs remote

```html
<!-- templates/home.html -->
<!DOCTYPE html>
<html lang="fr">
<head>
  <title>{{ title|default("Blog") }}</title>
  <script src="https://unpkg.com/htmx.org@2"></script>
</head>
<body>
  <header>
    <remote name="auth.navbar" user_id="{{ request.user.id|default('') }}">
      <nav><a href="/login">Connexion</a></nav>
    </remote>
  </header>

  <main>
    <remote name="blog.featured">
      <p>Chargement des articles…</p>
    </remote>

    <aside>
      <remote name="cart.mini">
        <p>Panier vide</p>
      </remote>
    </aside>
  </main>
</body>
</html>
```

## 7. API de l'intégration

### `create_xcore_engine`

Crée un `TemplateEngine` pré-câblé à l'instance XCore.

```python
engine = create_xcore_engine(
    xcore_instance=xcore,      # Instance XCore
    directory="templates",      # Dossier des templates
    enable_ui=False,            # Activer les composants microui
    enable_minify=True,         # Minification HTML
    enable_cache=False,         # Cache du rendu
    cache_ttl=300,              # Durée du cache (s)
    debug=True,                 # Mode debug
    static_prefix="/static",    # Préfixe pour static()
)
```

Ce qu'elle fait automatiquement :

| Élément | Description |
|---|---|
| `remote_caller` | Appelle `xcore.plugins.call(plugin, action, kwargs)` |
| `action_resolver` | Génère des URLs opaques `/_/a/<token>` pour les formulaires |
| `static()` | Helper `XCoreStatic` avec versionnement d'assets |
| Cache | Bridge vers `CacheService` de xcore si disponible |

### `register_action_routes`

Enregistre la route `POST /_/a/<token>` sur l'application FastAPI.

```python
register_action_routes(app, prefix="/_/a")
```

Ce que fait la route :

1. Reçoit les données du formulaire
2. Valide le token CSRF
3. Cherche le plugin et l'action dans la map des tokens
4. Appelle `xcore.plugins.call(plugin, action, form_data)`
5. Si `redirect` est présent, redirige (303)
6. Sinon, retourne le HTML

### `register_engine_service`

Enregistre le moteur comme service xcore pour que les plugins puissent l'utiliser.

```python
register_engine_service(xcore, engine, service_name="template_engine")
```

### `mount_template_static`

Monte le dossier `templates/static/` sur l'application FastAPI.

```python
mount_template_static(app, template_dir="templates", url_prefix="/static")
```

## 8. Résumé du flux

```
Template avec <remote>
        │
        ▼
MicroFrame rend le template
        │
        ▼
Tag <remote> → appelle _remote_caller
        │
        ▼
xcore.plugins.call("plugin", "action", kwargs)
        │
        ▼
Méthode du plugin → retourne {"html": "..."}
        │
        ▼
HTML inséré dans le template


Template avec <action>
        │
        ▼
MicroFrame génère un <form> avec URL opaque /_/a/<token>
        │
        ▼
Soumission du formulaire → POST /_/a/<token>
        │
        ▼
register_action_routes vérifie le CSRF
        │
        ▼
xcore.plugins.call("plugin", "action", form_data)
        │
        ▼
Méthode du plugin → traitement → {"html": "..."} ou redirect
```
