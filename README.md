# MicroFrame

Moteur de rendu Jinja2 modulaire pour Python. Rendu async, composants reutilisables, cache TTL, minification HTML et support micro-frontends.

Guide d usage rapide: docs/guide.md couvre le flux complet, puis docs/components.md, docs/remote-action.md et docs/micro-frontends.md detailent les usages avances.

## Installation

```bash
pip install microframe
# ou avec Poetry
poetry add microframe
```

## Démarrage rapide

```python
from microframe import TemplateEngine

engine = TemplateEngine(directory="templates")
html = await engine.render("index.html", {"title": "Accueil", "user": "Alice"})
```

```html
<!-- templates/index.html -->
<!DOCTYPE html>
<html>
  <head><title>{{ title }}</title></head>
  <body>
    <h1>Bonjour, {{ user }} !</h1>
  </body>
</html>
```

## Configuration

```python
engine = TemplateEngine(
    directory="templates",      # dossier des templates (défaut: "templates")
    debug=True,                 # rechargement auto des templates
    bytecode_cache=False,       # cache bytecode Jinja2 sur disque (.jinja_cache/)
    enable_minify=True,         # minification du HTML généré
    enable_cache=False,         # cache du rendu final en mémoire
    cache_ttl=300,              # durée du cache en secondes
    mfe_timeout=5.0,            # timeout HTTP pour les micro-frontends
)
```

## Composants

Les composants sont des fichiers HTML placés dans `templates/components/`. Ils sont enregistrés automatiquement au démarrage.

```html
<!-- templates/components/card.html -->
<div class="card">
  <h2>{{ title }}</h2>
  <div class="content">{{ slot }}</div>
</div>
```

**Syntaxe tag Jinja2 :**

```html
{% component "card" title="Mon titre" %}
  <p>Contenu du slot</p>
{% endcomponent %}
```

**Syntaxe HTML (auto-convertie) :**

```html
<component.card title="Mon titre">
  <p>Contenu du slot</p>
</component.card>

<!-- Self-closing -->
<component.avatar src="/img/user.png" />
```

Enregistrement manuel d'un composant :

```python
from microframe import ComponentRegistry

ComponentRegistry.register("alert", "<div class='alert {{ type }}'>{{ slot }}</div>")
```

## Filtres

| Filtre | Description | Exemple |
|---|---|---|
| `truncate` | Tronque le texte | `{{ text\|truncate(80) }}` |
| `slugify` | Convertit en slug URL | `{{ title\|slugify }}` |
| `currency` | Formate en monnaie | `{{ price\|currency("€") }}` |
| `timeago` | Temps relatif | `{{ created_at\|timeago }}` |
| `json_pretty` | JSON indenté | `{{ data\|json_pretty }}` |
| `json` | JSON inline sûr | `{{ obj\|json }}` |

Ajouter un filtre personnalisé :

```python
engine.add_filter("upper_first", lambda s: s[0].upper() + s[1:])
```

## Globals

Fonctions disponibles dans tous les templates :

| Global | Description |
|---|---|
| `static(path)` | URL d'un asset avec versionnement (`/static/app.css?v=abc`) |
| `url(name, **params)` | Construction d'URL avec query params |
| `csrf_token()` | Génère un champ `<input hidden>` CSRF |
| `paginate(items, page, per_page)` | Pagination d'une liste |
| `breadcrumbs(path)` | Fil d'Ariane depuis un chemin URL |
| `now()` | `datetime.now()` |

```html
<link rel="stylesheet" href="{{ static('app.css') }}">
<a href="{{ url('users', page=2) }}">Page suivante</a>
{{ csrf_token() }}
```

Ajouter une variable/fonction globale :

```python
engine.add_global("app_name", "MonApp")
engine.add_global("format_date", lambda d: d.strftime("%d/%m/%Y"))
```

## Cache

Cache en mémoire avec TTL (activé par template ou globalement) :

```python
# Global
engine = TemplateEngine(enable_cache=True, cache_ttl=600)

# Par rendu
html = await engine.render("page.html", ctx, use_cache=True)

# Vider le cache
engine.clear_cache()
```

Cache backend personnalisé :

```python
from microframe import CacheManager

class RedisCache(CacheManager):
    def get(self, key, ttl=None): ...
    def set(self, key, value): ...

engine = TemplateEngine(cache_backend=RedisCache())
```

## Versionnement des assets

```python
engine.set_asset_version("app.css", "v3.2.1")
# → /static/app.css?v=v3.2.1
```

## Micro-frontends

Intégration de fragments HTML servis par d'autres services :

```python
engine.mfe.register("header", "http://header-service/fragment")
engine.mfe.register_many({
    "footer": "http://footer-service/fragment",
    "cart":   "http://cart-service/fragment",
})
```

```html
<!-- Dans un template -->
{{ render_mfe("header") }}
{{ render_mfe("cart", user_id=42) }}
```

## Singleton global

Pour les projets qui n'ont besoin que d'une seule instance :

```python
from microframe.engine.core import TemplateEngine

# Initialisation unique (ex: au démarrage de l'app)
TemplateEngine.instance(directory="templates", debug=False)

# Récupération depuis n'importe où
engine = TemplateEngine.instance()
html = await engine.render("index.html", ctx)
```

## Structure du projet

```
microframe/
└── engine/
    ├── cache/        # CacheBackend, CacheManager
    ├── components/   # ComponentRegistry, extensions Jinja2
    ├── filters/      # Filtres built-in
    ├── globals/      # Fonctions globales built-in
    ├── mfe/          # Client micro-frontends (HTTP async)
    └── core/
        ├── environment.py   # Construction de l'environnement Jinja2
        └── renderer.py      # TemplateEngine — render, cache, minify
```

## Licence

MIT
