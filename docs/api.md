# Référence API

Commence par `guide.md` si tu veux un parcours pas a pas, puis reviens ici pour les signatures completes.

## TemplateEngine

`microframe.engine.core.renderer.TemplateEngine`

### Constructeur

```python
TemplateEngine(
    directory="templates",
    debug=True,
    bytecode_cache=False,
    enable_minify=True,
    enable_cache=False,
    enable_ui=False,
    cache_ttl=300,
    cache_backend=None,
    mfe_timeout=5.0,
    remote_caller=None,
    action_resolver=None,
)
```

| Paramètre | Type | Défaut | Description |
|---|---|---|---|
| `directory` | `str` | `"templates"` | Dossier des templates |
| `debug` | `bool` | `True` | Mode debug (rechargement auto) |
| `bytecode_cache` | `bool` | `False` | Cache bytecode Jinja2 sur disque |
| `enable_minify` | `bool` | `True` | Minification HTML automatique |
| `enable_cache` | `bool` | `False` | Cache du rendu final en mémoire |
| `enable_ui` | `bool` | `False` | Active les composants microui |
| `cache_ttl` | `int` | `300` | Durée du cache en secondes |
| `cache_backend` | `CacheBackend` | `None` | Backend de cache personnalisé |
| `mfe_timeout` | `float` | `5.0` | Timeout HTTP pour les MFE |
| `remote_caller` | `Callable` | `None` | Fonction pour les tags `<remote>` |
| `action_resolver` | `Callable` | `None` | Fonction pour les tags `<action>` |

### Méthodes

#### `render(template_name, ctx=None, use_cache=None) -> str`

Rend un template et retourne le HTML.

```python
html = await engine.render("page.html", {"title": "Hello"})
html = await engine.render("page.html", ctx, use_cache=True)
```

#### `add_global(name, value)`

Ajoute une variable/fonction globale disponible dans tous les templates.

```python
engine.add_global("site_name", "MonSite")
engine.add_global("now", datetime.now)
```

#### `add_filter(name, func)`

Ajoute un filtre Jinja2.

```python
engine.add_filter("upper_first", lambda s: s[0].upper() + s[1:])
```

#### `add_context_processor(func)`

Ajoute un context processor (sync ou async).

```python
engine.add_context_processor(lambda ctx: {"extra": "value"})
```

#### `set_asset_version(path, version)`

Définit la version d'un fichier static.

```python
engine.set_asset_version("app.css", "v2")
# static("app.css") → "/static/app.css?v=v2"
```

#### `list_templates() -> list[str]`

Liste tous les templates disponibles.

#### `clear_cache()`

Vide le cache de rendu.

---

## CacheBackend

`microframe.engine.cache.manager.CacheBackend`

Classe abstraite pour les backends de cache.

```python
class CacheBackend(ABC):
    def get(key: str, ttl: Optional[int]) -> Optional[Any]: ...
    def set(key: str, value: Any): ...
    def delete(key: str): ...
    def clear(): ...
```

### CacheManager

Implémentation mémoire par défaut.

```python
from microframe import CacheManager

cache = CacheManager()
cache.set("key", "<html>...</html>")
value = cache.get("key", ttl=300)  # None si expiré
```

### Backend personnalisé

```python
from microframe import CacheBackend

class RedisCache(CacheBackend):
    def __init__(self, url="redis://localhost:6379"):
        self.client = redis.from_url(url)
    def get(self, key, ttl=None):
        return self.client.get(key)
    def set(self, key, value):
        self.client.set(key, value)
    def delete(self, key):
        self.client.delete(key)
    def clear(self):
        self.client.flushdb()
```

---

## MFEClient

`microframe.engine.mfe.client.MFEClient`

Gère l'enregistrement et la récupération de fragments micro-frontends.

```python
from microframe import MFEClient

client = MFEClient(timeout=5.0)
client.register("header", "http://localhost:4000/header")
client.register_many({
    "footer": "http://localhost:4000/footer",
})
html = await client.fetch("header", user_id=42)
```

---

## ComponentRegistry

`microframe.engine.components.registry.ComponentRegistry`

Registre global des composants HTML.

```python
from microframe import ComponentRegistry

ComponentRegistry.register("alert", "<div class='alert'>{{ slot }}</div>")
template = ComponentRegistry.get("alert")
all = ComponentRegistry.all()
```

---

## UIComponent

`microframe.engine.ui.component.Component`

Classe de base pour les composants microui. Active `enable_ui=True` sur `TemplateEngine` pour les rendre disponibles.

```python
from microframe import UIComponent, ui_register

@ui_register
class Button(UIComponent):
    def render(self):
        label = self.props.get("label", "Click")
        return f'<button class="btn">{label}</button>'
```

---

## Globals intégrées

Fonctions disponibles dans tous les templates :

| Global | Description |
|---|---|
| `static(path)` | URL d'asset avec version |
| `url(name, **params)` | Construction d'URL |
| `csrf_token()` | Token CSRF stable, genere par moteur |
| `paginate(items, page, per_page)` | Pagination |
| `breadcrumbs(path)` | Fil d'Ariane |
| `now()` | `datetime.now()` |

---

## Filtres intégrés

| Filtre | Description |
|---|---|
| `truncate(length, suffix)` | Tronque le texte |
| `slugify` | Slug URL |
| `currency(symbol)` | Format monnaie |
| `timeago` | Temps relatif |
| `json` | JSON inline (Markup safe) |
| `json_pretty` | JSON indenté |
