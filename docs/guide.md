# Guide d'utilisation

## Configuration

```python
from microframe import TemplateEngine

engine = TemplateEngine(
    directory="templates",       # dossier des templates
    debug=True,                  # rechargement auto
    bytecode_cache=False,        # cache bytecode Jinja2 sur disque
    enable_minify=True,          # minification HTML
    enable_cache=False,          # cache du rendu final
    cache_ttl=300,               # durée du cache (secondes)
    enable_ui=False,             # active les composants microui
    mfe_timeout=5.0,             # timeout HTTP micro-frontends
)
```

## Rendre un template

```python
html = await engine.render("page.html", {"key": "value"})
```

Le contexte est un dictionnaire Python standard. Les cles deviennent des variables dans le template Jinja2. Parcours recommande: rendu de base, composants HTML, microui, context processors, remote/action, micro-frontends et CLI.

## Templates

MicroFrame utilise Jinja2 en mode async avec `trim_blocks` et `lstrip_blocks` activés.

### Variables

```html
<h1>{{ title }}</h1>
<p>{{ user.name }}</p>
```

### Filtres

```html
<p>{{ text|truncate(100) }}</p>
<p>{{ title|slugify }}</p>
<p>{{ price|currency("€") }}</p>
<p>{{ created_at|timeago }}</p>
<pre>{{ data|json_pretty }}</pre>
```

### Structure conditionnelle et boucles

```html
{% if user %}
  <p>Bonjour, {{ user }}!</p>
{% else %}
  <p>Bonjour, invité!</p>
{% endif %}

<ul>
{% for item in items %}
  <li>{{ item.name }}</li>
{% endfor %}
</ul>
```

## Ajouter des globals et filtres

```python
engine.add_global("app_name", "MonApp")
engine.add_global("format_date", lambda d: d.strftime("%d/%m/%Y"))

engine.add_filter("upper_first", lambda s: s[0].upper() + s[1:])
```

## Cache

```python
# Activer le cache globalement
engine = TemplateEngine(enable_cache=True, cache_ttl=600)

# Par rendu
html = await engine.render("page.html", ctx, use_cache=True)
html = await engine.render("page.html", ctx, use_cache=False)

# Backend personnalisé
from microframe import CacheBackend

class RedisCache(CacheBackend):
    def get(self, key, ttl=None): ...
    def set(self, key, value): ...
    def delete(self, key): ...
    def clear(self): ...

engine = TemplateEngine(cache_backend=RedisCache())

# Vider le cache (clear_cache est async : le backend peut lui-même être
# sync ou async — TemplateEngine attend le résultat dans les deux cas)
await engine.clear_cache()
```

## Assets

```python
engine.set_asset_version("app.css", "v3.2.1")
# → /static/app.css?v=v3.2.1
```

```html
<link rel="stylesheet" href="{{ static('app.css') }}">
```

## Singleton

Pour les projets qui n'ont besoin que d'une instance :

```python
# Initialisation unique
TemplateEngine.instance(directory="templates", debug=False)

# Réutilisation
engine = TemplateEngine.instance()
html = await engine.render("index.html", ctx)
```
