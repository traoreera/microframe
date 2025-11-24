# 🎨 Moteur de Templates - Jinja2

> Documentation du moteur de templates intégré dans MicroFrame basé sur Jinja2

## 📋 Vue d'ensemble

MicroFrame intègre un moteur de templates puissant basé sur **Jinja2** avec :
- ✅ Templates compilés et cachés
- ✅ Système de composants réutilisables
- ✅ Filtres et globals personnalisés
- ✅ Support async
- ✅ Intégration HTMX

---

## 🚀 Installation et Configuration

### Import

```python
from microframe.engine import TemplateEngine
```

### Configuration de Base

```python
from microframe import Application
from microframe.engine import TemplateEngine

app = Application()

# Initialiser le moteur
engine = TemplateEngine(
    templates_dir="templates",
    auto_reload=True,  # Dev mode
    cache_size=400
)
```

---

## 📝 Templates de Base

### Créer un Template

Créez `templates/index.html` :

```html
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
</head>
<body>
    <h1>{{ heading }}</h1>
    <p>{{ content }}</p>
</body>
</html>
```

### Rendre le Template

```python
@app.get("/")
async def index(request):
    return engine.render("index.html", {
        "title": "Accueil",
        "heading": "Bienvenue !",
        "content": "Ceci est rendu depuis un template"
    })
```

---

## 🧩 Héritage de Templates

### Template de Base

Créez `templates/base.html` :

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Mon Site{% endblock %}</title>
    {% block extra_head %}{% endblock %}
</head>
<body>
    <header>
        {% block header %}
        <nav>
            <a href="/">Accueil</a>
            <a href="/about">À propos</a>
        </nav>
        {% endblock %}
    </header>
    
    <main>
        {% block content %}{% endblock %}
    </main>
    
    <footer>
        {% block footer %}
        <p>&copy; 2025 Mon Site</p>
        {% endblock %}
    </footer>
    
    {% block scripts %}{% endblock %}
</body>
</html>
```

### Template Enfant

Créez `templates/page.html` :

```html
{% extends "base.html" %}

{% block title %}{{ page_title }} - Mon Site{% endblock %}

{% block content %}
<h1>{{ page_title }}</h1>
<div>{{ page_content }}</div>
{% endblock %}

{% block scripts %}
<script src="/static/js/page.js"></script>
{% endblock %}
```

---

## 🔧 Composants Réutilisables

### Définir un Composant

Créez `templates/components/card.html` :

```html
<div class="card">
    <div class="card-header">
        <h3>{{ title }}</h3>
    </div>
    <div class="card-body">
        {{ content }}
    </div>
    {% if actions %}
    <div class="card-footer">
        {{ actions }}
    </div>
    {% endif %}
</div>
```

### Utiliser le Composant

```html
{% include "components/card.html" with 
   title="Mon Titre", 
   content="Contenu de la carte",
   actions="<button>Action</button>"
%}
```

---

## 🎯 Macros (Fonctions)

### Définir une Macro

Créez `templates/macros.html` :

```html
{% macro render_button(text, variant="primary", url="#") %}
<a href="{{ url }}" class="btn btn-{{ variant }}">
    {{ text }}
</a>
{% endmacro %}

{% macro render_input(name, label, type="text", value="") %}
<div class="form-group">
    <label for="{{ name }}">{{ label }}</label>
    <input type="{{ type }}" 
           name="{{ name }}" 
           id="{{ name }}" 
           value="{{ value }}" 
           class="form-control">
</div>
{% endmacro %}

{% macro render_alert(message, type="info") %}
<div class="alert alert-{{ type }}" role="alert">
    {{ message }}
</div>
{% endmacro %}
```

### Utiliser les Macros

```html
{% from "macros.html" import render_button, render_input, render_alert %}

{{ render_alert("Bienvenue !", "success") }}

{{ render_input("email", "Email", "email") }}
{{ render_input("password", "Mot de passe", "password") }}

{{ render_button("Connexion", "primary", "/login") }}
{{ render_button("Annuler", "secondary", "/") }}
```

---

## 🔄 Boucles et Conditions

### Boucles

```html
<ul>
{% for item in items %}
    <li>{{ loop.index }}. {{ item.name }} - {{ item.price }}€</li>
{% else %}
    <li>Aucun élément</li>
{% endfor %}
</ul>

{# Variables de boucle disponibles:
   - loop.index (1-indexed)
   - loop.index0 (0-indexed)
   - loop.first
   - loop.last
   - loop.length
#}
```

### Conditions

```html
{% if user.is_authenticated %}
    <p>Bonjour, {{ user.name }} !</p>
    <a href="/logout">Déconnexion</a>
{% elif user.is_guest %}
    <p>Mode invité</p>
{% else %}
    <a href="/login">Connexion</a>
{% endif %}
```

---

## 🎨 Filtres Personnalisés

### Filtres Intégrés

```html
{# String filters #}
{{ "hello"|upper }}  {# HELLO #}
{{ "WORLD"|lower }}  {# world #}
{{ "hello"|capitalize }}  {# Hello #}
{{ "  spaces  "|trim }}  {# "spaces" #}

{# List filters #}
{{ items|length }}
{{ items|first }}
{{ items|last }}
{{ items|join(", ") }}

{# Number filters #}
{{ 42.12345|round(2) }}  {# 42.12 #}
{{ price|float }}

{# Date filters (avec arrow ou datetime) #}
{{ now|datetimeformat('%Y-%m-%d') }}
```

### Créer des Filtres Custom

```python
from microframe.engine import TemplateEngine

engine = TemplateEngine("templates")

# Ajouter un filtre custom
def format_currency(value):
    """Formatte en euros"""
    return f"{value:.2f} €"

engine.env.filters['currency'] = format_currency

# Utilisation dans template:
# {{ price|currency }}  → "19.99 €"
```

---

## 🌍 Globals Personnalisés

### Ajouter des Globals

```python
from datetime import datetime

def get_current_year():
    return datetime.now().year

def get_app_version():
    return "1.0.0"

# Ajouter au template engine
engine.env.globals['current_year'] = get_current_year
engine.env.globals['app_version'] = get_app_version

# Utilisation dans templates:
# <footer>© {{ current_year() }} Mon Site - v{{ app_version() }}</footer>
```

---

## ⚡ Cache de Templates

### Configuration du Cache

```python
engine = TemplateEngine(
    templates_dir="templates",
    cache_size=400,        # Nombre de templates cachés
    auto_reload=False      # Production: désactiver auto-reload
)
```

### Invalidation du Cache

```python
# Invalider tout le cache
engine.clear_cache()

# Recharger un template spécifique
engine.reload_template("index.html")
```

---

## 🔌 Intégration HTMX

### Template avec HTMX

```html
{% extends "base.html" %}

{% block content %}
<div id="user-list">
    <button hx-get="/api/users" 
            hx-target="#user-list" 
            hx-swap="innerHTML">
        Charger utilisateurs
    </button>
</div>
{% endblock %}
```

### Fragment de Template (Partial)

Créez `templates/partials/user_list.html` :

```html
<ul>
{% for user in users %}
    <li>
        {{ user.name }}
        <button hx-delete="/api/users/{{ user.id }}" 
                hx-target="closest li" 
                hx-swap="outerHTML">
            Supprimer
        </button>
    </li>
{% endfor %}
</ul>
```

### Route pour Fragment

```python
@app.get("/api/users")
async def get_users(request):
    users = await get_all_users()
    # Retourner seulement le fragment
    return engine.render("partials/user_list.html", {"users": users})
```

---

## 📚 Exemples Complets

### Dashboard Complet

```html
{# templates/dashboard.html #}
{% extends "base.html" %}
{% from "macros.html" import render_card, render_stat %}

{% block title %}Dashboard{% endblock %}

{% block content %}
<h1>Tableau de Bord</h1>

<div class="stats-grid">
    {{ render_stat("Utilisateurs", stats.users, "info") }}
    {{ render_stat("Ventes", stats.sales, "success") }}
    {{ render_stat("Revenue", stats.revenue | currency, "primary") }}
</div>

<div class="cards-grid">
    {% for item in recent_items %}
        {{ render_card(
            title=item.title,
            content=item.description,
            footer=item.created_at | datetimeformat
        ) }}
    {% endfor %}
</div>
{% endblock %}
```

### Formulaire avec Validation

```html
{# templates/forms/login.html #}
{% extends "base.html" %}

{% block content %}
<form method="POST" action="/auth/login">
    {% if errors %}
    <div class="alert alert-danger">
        <ul>
        {% for error in errors %}
            <li>{{ error }}</li>
        {% endfor %}
        </ul>
    </div>
    {% endif %}
    
    <div class="form-group">
        <label for="email">Email</label>
        <input type="email" 
               name="email" 
               value="{{ email|default('') }}"
               class="form-control {% if 'email' in errors %}is-invalid{% endif %}">
    </div>
    
    <div class="form-group">
        <label for="password">Mot de passe</label>
        <input type="password" 
               name="password" 
               class="form-control {% if 'password' in errors %}is-invalid{% endif %}">
    </div>
    
    <button type="submit" class="btn btn-primary">Connexion</button>
</form>
{% endblock %}
```

---

## 🔗 Intégration avec MicroFrame

### Route avec Template

```python
from microframe import Application
from microframe.engine import TemplateEngine

app = Application()
engine = TemplateEngine("templates")

@app.get("/")
async def index(request):
    context = {
        "title": "Accueil",
        "user": request.state.user if hasattr(request.state, 'user') else None,
        "items": await get_items()
    }
    return engine.render("index.html", context, request=request)
```

### Passer Request au Template

```python
# Le request est disponible dans les templates
@app.get("/profile")
async def profile(request):
    return engine.render("profile.html", {
        "user": await get_current_user(request)
    }, request=request)
```

```html
{# Dans le template #}
<p>Votre IP: {{ request.client.host }}</p>
<p>URL: {{ request.url.path }}</p>
```

---

## 📖 Ressources

- **[Jinja2 Documentation](https://jinja.palletsprojects.com/)** - Docs officielles
- **[HTMX Documentation](https://htmx.org/)** - Pour interactions dynamiques
- **[MicroUI Components](ui.md)** - Composants UI intégrés

---

---

## 📖 Navigation Modules

**Documentation Modules** :
- [Index Modules](README.md)
- **📍 Templates** (vous êtes ici)
- [Configurations](configurations.md)
- [UI Components](ui.md)

---

**[↑ Index Principal](../README.md)** | **[← Modules](README.md)** | **[Configurations →](configurations.md)**
