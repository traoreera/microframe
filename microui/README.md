Voici un **README clair, pro, et prêt pour GitHub** — formaté comme un projet open-source moderne.

---

# 🌟 MicroFrame UI — DaisyUI Full Stack UI Kit

MicroFrame UI est un module frontend/UX complet pour **MicroFrame**, intégrant :

* 🎨 **TailwindCSS + DaisyUI**
* ⚡ **Composants UI réutilisables** (Button, Modal, Alert, Cards…)
* 🔁 **HTMX Ready** (Actions AJAX, Swap dynamique)
* 🌓 **Theme Manager** (Dark/Light/System + UI Toggle)
* 🧩 **Template Engine (Jinja2) avec injection dynamique**
* 🔌 **Router + State UI context**
* 🧠 **Architecture plug-and-play**

Ce kit permet de construire une UI moderne, réactive et élégante **sans React ni SPA**.

---

## 🚀 Installation

```sh
pip install microframe microui
```

---

## 🛠 Exemple Complet

```python
from microframe.ui import TemplateEngine
from starlette.responses import HTMLResponse
from microframe import AppConfig, Application, Router, Request
from microui import register_components, DaisyUI, Modal, Button, Alert, setup_daisy_ui, ThemeManager, get_theme_context


appConf = AppConfig(title="DaisyUI Kit", version="0.0.1", debug=True)

app = Application(configuration=appConf)
router = Router(tags=["Demo UI"])


# 1️⃣ Initialiser DaisyUI + Routes Thèmes
setup_daisy_ui(app=app, router=router)


# 2️⃣ Créer un composant Modal réutilisable
modal_html = Modal.render(
    id="my_modal",
    title="Confirmation",
    content="<p>Êtes-vous sûr de vouloir continuer ?</p>",
    actions=f"""
        {Button.render("Annuler", variant="ghost", onclick="my_modal.close()")}
        {Button.render("Confirmer", variant="primary", onclick="my_modal.close()")}
    """
)


# 3️⃣ Inject UI components au state global
app.state.ui = register_components()
app.state.modal_html = modal_html


# 4️⃣ Init moteur de templates
template = TemplateEngine(cache=False, debug=True).instance()


@app.get("/")
async def index(request: Request):

    # Theme switch UI
    switch = DaisyUI.theme_switcher(
        current_theme=ThemeManager.get_theme(request),
        position="dropdown-end"
    )
    
    # Add UI context
    ctx: dict = app.state.ui
    ctx.update(get_theme_context(request))

    app.state.themes = switch  # expose au template
    
    return await template.render(
        "pages/index.html",
        ctx,
        request
    )


@app.post('/submit')
async def submit(request: Request):
    form = await request.form()
    username = form.get("username", "")
    email = form.get("email", "")

    return HTMLResponse(Alert.render(
        message=f"Merci {username} 🎉 — Email reçu à {email} !",
        type="success",
        dismissible=True,
        icon="✔️"
    ))



@router.get("/dashboard")
async def dashboard(request: Request):
    """Page dashboard avec stats DaisyUI"""
    
    stats_cards = """
    <div class="stats shadow">
        <div class="stat">
            <div class="stat-title">Total Likes</div>
            <div class="stat-value text-primary">25.6K</div>
            <div class="stat-desc">21% more than last month</div>
        </div>
        
        <div class="stat">
            <div class="stat-title">Page Views</div>
            <div class="stat-value text-secondary">2.6M</div>
            <div class="stat-desc text-secondary">↗︎ 21% growth</div>
        </div>
        
        <div class="stat">
            <div class="stat-value">86%</div>
            <div class="stat-title">Tasks done</div>
            <div class="stat-desc text-secondary">31 tasks remaining</div>
        </div>
    </div>
    """
    
    return HTMLResponse(stats_cards)


# 5️⃣ Register router
app.include_router(router)
```
## pages/index.html
```html
{% extends "base.html" %}
{% block title %}UI Preview{% endblock %}

{% block sidebar %}

{{ navbar("DaisyUI Kit", [
{"text": "Accueil", "href": "/"},
{"text": "Dashboard", "hx_get": "/dashboard"},
{"text": "Projets", "href": "/demo/projects"},
{"text": "Équipe", "href": "/demo/team"},
{"text": "Paramètres", "href": "/demo/settings"}
],
end_items=request.app.state.themes)
}}
{% endblock %}


{% block content %}
<div class="container mx-auto p-4 space-y-6">
    <div class="hero bg-base-200 rounded-lg"></div>
    <div class="max-w-md">
        <h1 class="text-5xl font-bold">DaisyUI Kit 🎨</h1>
        <p class="py-6">Créez des interfaces magnifiques avec Python, HTMX et DaisyUI</p>
        {{button("Commencer", variant="primary", size="lg", onclick="my_modal.showModal()")}}
    </div>
    <!-- Cards Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {{card(
        title="Bienvenue sur DaisyUI Kit",
        body="<p>Un kit complet de composants UI pour Python avec HTMX et DaisyUI.</p>
        <p>Créez des interfaces magnifiques avec Python, HTMX et DaisyUI.</p>
        ",
        actions = button("Decouvrir", variant="primary", hx_get="/features", hx_swap="outerHTML", hx_target="#content")
        )}}

        {{card(
        title="Composants",
        body="Plus de 10 composants prêts à l'emploi",
        image="https://picsum.photos/400/300?random=1",
        actions=button("Explorer", variant="secondary", size="sm"),
        compact=True)}}

        {{card(
        title="Thèmes",
        body="30+ thèmes DaisyUI disponibles",
        image="https://picsum.photos/400/300?random=2",
        actions=button("Changer", variant="accent", size="sm"),
        compact=True
        )}}

    </div>

    <div class="space-y-2">
        <h2 class="text-2xl font-bold">Alertes</h2>
        {% for items in [alert("Opération réussie !", type="success", dismissible=True),alert("Attention : vérifiez vos
        données", type="warning"),alert("Information importante", type="info"),] %}
        {{items}}
        {% endfor %}
    </div>
    <div class="space-y-2">
        <div class="fles gap-2 flex-warp">
            {% for item in [
            badge("Nouveau", variant="primary", size="lg"),
            badge("En stock", variant="success"),
            badge("Promo", variant="error", outline=True),
            ]%}
            {{item}}
            {% endfor %}
        </div>
    </div>
    <div class="card bg-base-100 shadow-xl">
        <div class="card-body">
            <h2 class="card-title">Formulaire de contact</h2>
            <form hx-post="/submit" hx-target="#result" hx-swap="innerHTML">
                {{input(
                name="username",
                label="Nom d'utilisateur",
                placeholder="Entrez votre nom",
                size="md"
                )}}
                {{input(
                name="email",
                type="email",
                label="Email",
                placeholder="votre@email.com",
                size="md"
                )}}
                {{button("Envoyer", variant="primary", block=True)}}
            </form>
            <div id="result" class="mt-4"></div>
        </div>
    </div>
    <div class="space-y-2">
        <h2 class="text-2xl font-bold">Tableau</h2>
        {{
        table(
        headers=["ID", "Nom", "Email", "Status"],
        rows=[
        ["1", "Alice", "alice@example.com", badge("Actif", variant="success", size="sm")],
        ["2", "Bob", "bob@example.com", badge("Inactif", variant="error", size="sm")],
        ["3", "Charlie", "charlie@example.com", badge("Actif", variant="success", size="sm")],
        ],
        zebra=True,
        hoverable=True
        )
        }}
    </div>
    <div class="space-y-2">
        <h2 class="text-2xl font-bold">États de chargement</h2>
        <div class="flex gap-4 flex-wrap items-center">
            {{loading(type="spinner", size="sm")}}
            {{loading(type="dots", size="md")}}
            {{loading(type="ring", size="lg", color="primary")}}
            {{loading(type="ball", size="md", color="secondary")}}
            {{loading(type="bars", size="md", color="accent")}}
        </div>
    </div>
    {{ request.app.state.modal_html }}
</div>
{% endblock %}
```
## base.html
```html
<!DOCTYPE html>
<html lang="fr" data-theme="{{ request.state.theme }}">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Dashboard{% endblock %}</title>

    <!-- Tailwind + DaisyUI -->
    <link href="https://cdn.jsdelivr.net/npm/daisyui@4.12.14/dist/full.min.css" rel="stylesheet" />
    <script src="https://cdn.tailwindcss.com"></script>

    <!-- HTMX -->
    <script src="https://unpkg.com/htmx.org@2.0.3"></script>
    <script src="https://unpkg.com/htmx.org/dist/ext/ws.js"></script>

    <!-- Alpine.js -->
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>

    <style>
        * {
            transition: background 0.25s, color 0.25s;
        }
    </style>

    {% block head %}{% endblock %}
</head>

<body>
    {% block sidebar %}
    {% endblock %}
    {% block content %}
    {% endblock %}
    {% block scripts %}
    {% endblock %}
</body>

</html>
```

---

## 🧩 Structure recommandée

```
project/
│
├── templates/
│   ├── base.html
│   └── pages/
│       └── index.html
│
├── static/
│   └── css/tailwind.css
│
└── main.py
```

---

## 🎛 Composants disponibles

| Type           | Exemple                                    |
| -------------- | ------------------------------------------ |
| Buttons        | `Button.render("Save", variant="primary")` |
| Alerts         | `Alert.render("Saved!", type="success")`   |
| Modal          | `Modal.render(id="edit_user")`             |
| Cards          | DaisyUI card set                           |
| Theme Switcher | `DaisyUI.theme_switcher()`                 |
| Form Elements  | inputs, toggles, selects, badges…          |

---

## 🌓 Thèmes supportés

| Mode            | Exemple                                             |
| --------------- | --------------------------------------------------- |
| Light           | Default                                             |
| Dark            | `ThemeManager.set(request, "dark")`                 |
| DaisyUI Palette | `cupcake`, `dracula`, `synthwave`, `corporate`, etc |

---

## 🔥 HTMX Ready

Tous les composants peuvent être utilisés avec :

```html
<button hx-post="/submit" hx-target="#result">
    Envoyer
</button>
```

---

## 🎯 Avantages

* Pas de React, Vue ni build system
* UI dynamique via HTMX
* Web-ready en 2 fichiers
* Ultra rapide, zéro surcharge

---

## 📦 Roadmap

* [x] UI Kit DaisyUI
* [x] Theme System
* [x] Modal + Alert System
* [x] Form Helpers
* [ ] Websocket Live UI Preview
* [ ] Component Marketplace
* [ ] Drag-n-Drop UI Builder

---

## 🏁 Conclusion

MicroFrame UI transforme ton backend Python en une UI moderne **tailwindisé** avec interaction **temps réel**, sans frontend framework complexe.
