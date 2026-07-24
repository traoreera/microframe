# MicroFrame — Vision & Features à implémenter

Ce document décrit les fonctionnalités prévues pour les prochaines versions du moteur.
Chaque section indique l'état actuel et ce qui reste à construire.

---

## État actuel (v2.0)

| Feature | Statut |
|---|---|
| Rendu Jinja2 async | ✅ |
| Composants (`{% component %}` + `<component.X>`) | ✅ |
| Cache mémoire avec TTL | ✅ |
| Filtres built-in | ✅ |
| Globals built-in (paginate, breadcrumbs, csrf) | ✅ |
| Minification HTML | ✅ |
| Versionnement des assets | ✅ |
| Micro-frontends async (MFEClient) | ✅ |

---

## Cache (v2.1)

### Backends pluggables
Actuellement seul `CacheManager` (in-memory) est disponible.
Il faut implémenter des backends alternatifs via l'interface `CacheBackend`.

```python
# Usage visé
from microframe.engine.cache import RedisCache

engine = TemplateEngine(
    cache_backend=RedisCache(url="redis://localhost:6379", prefix="mf:")
)
```

**À implémenter :**
- `RedisCache` — backend Redis via `aioredis`
- `FilesystemCache` — cache HTML sur disque (utile pour le SSG)
- `MemcachedCache` — backend Memcached
- Invalidation par tag : `cache.invalidate_tag("blog")` pour invalider tous les templates tagués `blog`

```python
html = await engine.render("post.html", ctx, cache_tags=["blog", "post-42"])
engine.cache.invalidate_tag("blog")  # invalide tous les templates avec ce tag
```

---

## Context processors (v2.1)

Fonctions appelées automatiquement avant chaque rendu pour injecter des variables globales dans le contexte.

```python
# Usage visé
def inject_settings(ctx: dict) -> dict:
    ctx["DEBUG"] = True
    ctx["SITE_NAME"] = "MonSite"
    return ctx

engine.add_context_processor(inject_settings)
```

Les context processors async doivent aussi être supportés :

```python
async def inject_user(ctx: dict) -> dict:
    ctx["current_user"] = await fetch_user(ctx.get("user_id"))
    return ctx
```

**À implémenter :**
- `TemplateEngine.add_context_processor(func)` 
- Appel automatique des processors avant `template.render_async()`
- Support sync et async

---

## Internationalisation / i18n (v2.2)

Traduction des chaînes dans les templates via un système de catalogues.

```html
<!-- Dans un template -->
<h1>{{ _("Bonjour") }}</h1>
<p>{{ ngettext("%(num)d article", "%(num)d articles", count) }}</p>
```

```python
# Configuration
engine = TemplateEngine(
    directory="templates",
    locale="fr_FR",
    translations_dir="locales",
)
```

**À implémenter :**
- Intégration `Babel` pour la gestion des catalogues `.po` / `.mo`
- Global `_()` et `ngettext()` dans l'environnement Jinja2
- Changement de locale dynamique par rendu : `await engine.render("page.html", ctx, locale="en_US")`
- Extension Jinja2 `{% trans %}...{% endtrans %}`

---

## Rechargement à chaud / Watcher (v2.2)

En mode `debug=True`, surveiller les fichiers templates et recharger automatiquement les composants enregistrés sans redémarrer.

```python
engine = TemplateEngine(directory="templates", debug=True, watch=True)
# → les composants dans templates/components/ se rechargent dès qu'un .html est modifié
```

**À implémenter :**
- `Watcher` dans `engine/watcher.py` basé sur `watchdog`
- Écoute des modifications dans `templates/components/`
- Rappel de `auto_register_components()` sur chaque changement
- Invalidation du cache bytecode Jinja2 sur modification d'un template

---

## Streaming (v2.3)

Rendu progressif du template : envoyer les premiers octets au client avant que le rendu soit terminé. Utile pour les grandes pages.

```python
# Usage visé
async for chunk in engine.stream("page.html", ctx):
    await response.write(chunk)
```

**À implémenter :**
- `TemplateEngine.stream(template_name, ctx)` → `AsyncIterator[str]`
- Basé sur `jinja2.Environment.generate_async()`
- Option `chunk_size` pour contrôler la granularité

---

## Composants avancés (v2.3)

### Composants Python (class-based)

```python
from microframe.engine.components import Component

class Card(Component):
    template = "components/card.html"

    def get_context(self):
        return {
            "title": self.props.get("title", ""),
            "slot": self.children,
        }

ComponentRegistry.register("card", Card)
```

### Composants avec validation des props

```python
class Button(Component):
    template = "components/button.html"
    props_schema = {
        "label": str,
        "variant": ("primary", "secondary", "danger"),
        "disabled": bool,
    }
```

**À implémenter :**
- Classe de base `Component` dans `engine/components/base.py`
- Méthode `get_context()` overridable
- Validation des props avec levée d'erreur claire en mode debug

---

## Filtres supplémentaires (v2.3)

Filtres à ajouter dans `engine/filters/builtin.py` :

| Filtre | Description |
|---|---|
| `markdown` | Convertit du Markdown en HTML (via `mistune`) |
| `humanize` | Nombres lisibles : `1200` → `1 200`, `1500000` → `1.5M` |
| `highlight` | Coloration syntaxique de code (via `Pygments`) |
| `gravatar` | URL Gravatar depuis un email |
| `nl2br` | Convertit les sauts de ligne en `<br>` |
| `pluralize` | `{{ count }} article{{ count|pluralize }}` |

---

## Pages d'erreur (v2.3)

Rendu automatique de templates dédiés quand un template est introuvable ou plante.

```
templates/
└── errors/
    ├── 404.html   ← template non trouvé
    └── 500.html   ← erreur de rendu
```

```python
engine = TemplateEngine(
    directory="templates",
    error_templates={"404": "errors/404.html", "500": "errors/500.html"},
)
```

**À implémenter :**
- Détection `TemplateNotFound` → rendu de `errors/404.html`
- Détection `Exception` → rendu de `errors/500.html` avec contexte d'erreur en mode debug
- Fallback sur le message HTML inline si le template d'erreur est lui-même introuvable

---

## CLI (v2.4)

Commande `microframe` pour rendre des templates depuis le terminal, utile pour la génération de sites statiques.

```bash
# Rendre un template avec un contexte JSON
microframe render index.html --ctx '{"title": "Accueil"}' --out dist/index.html

# Générer tous les templates d'un dossier
microframe build --templates templates/ --out dist/ --ctx ctx.json

# Lister les templates disponibles
microframe list

# Vider le cache
microframe cache clear
```

**À implémenter :**
- `microframe/cli.py` basé sur `typer`
- Commandes : `render`, `build`, `list`, `cache`
- Chargement du contexte depuis fichier JSON ou stdin
- Rapport de génération (nb fichiers, temps total)

---

## Utilitaires de test (v2.4)

Helpers pour tester les templates sans serveur web.

```python
from microframe.testing import TemplateTestCase

class TestCard(TemplateTestCase):
    engine = TemplateEngine(directory="tests/templates")

    async def test_renders_title(self):
        html = await self.render("components/card.html", {"title": "Test", "slot": ""})
        self.assertIn("Test", html)

    async def test_component_slot(self):
        html = await self.render_component("card", title="Hello", slot="<p>Content</p>")
        self.assertIn("<p>Content</p>", html)
```

**À implémenter :**
- `TemplateTestCase` dans `microframe/testing.py`
- Méthodes : `render()`, `render_component()`, `assertContains()`, `assertNotContains()`
- Fixture `engine` overridable par test

---

## Génération de site statique / SSG (v2.5)

Rendre un ensemble de pages en fichiers HTML statiques à partir d'une configuration.

```python
from microframe.ssg import StaticGenerator

gen = StaticGenerator(engine, output_dir="dist/")

gen.add_page("index.html",  ctx={"title": "Accueil"},  output="index.html")
gen.add_page("about.html",  ctx={"title": "À propos"}, output="about.html")

# Pages dynamiques depuis une liste
gen.add_collection(
    template="post.html",
    items=posts,           # liste de dicts
    output=lambda item: f"posts/{item['slug']}.html",
)

await gen.build()
# → dist/index.html, dist/about.html, dist/posts/mon-article.html ...
```

**À implémenter :**
- `StaticGenerator` dans `microframe/ssg.py`
- `add_page()`, `add_collection()`, `build()`
- Copie des assets statiques vers `dist/`
- Rapport de build (pages générées, erreurs, durée)
