# Context Processors

Commence par `guide.md` si tu veux voir le flux complet, puis reviens ici pour les injections de contexte automatisees.

Les context processors sont des fonctions appelées automatiquement avant chaque rendu. Elles reçoivent le dictionnaire de contexte et peuvent l'enrichir.

## Définition

### Processeur synchrone

```python
def inject_settings(ctx):
    ctx["site_name"] = "MonSite"
    ctx["debug"] = True
    return ctx

engine.add_context_processor(inject_settings)
```

### Processeur asynchrone

```python
async def inject_user(ctx):
    ctx["current_user"] = await fetch_user(ctx.get("user_id"))
    return ctx

engine.add_context_processor(inject_user)
```

### Processeur sans argument

```python
def inject_globals():
    return {"app_version": "2.0.0", "year": 2025}

engine.add_context_processor(inject_globals)
```

## Ordre d'exécution

Les processeurs sont exécutés dans l'ordre d'ajout. Les valeurs retournées écrasent les clés existantes dans le contexte.

```python
engine.add_context_processor(lambda ctx: {"title": "from processor"})
engine.add_context_processor(lambda ctx: {"title": "overwritten"})

html = await engine.render("page.html", {"title": "original"})
# → title sera "overwritten"
```

## Cas d'usage

### Configuration globale

```python
def inject_config(ctx):
    ctx["SITE_NAME"] = "MonApp"
    ctx["SITE_URL"] = "https://example.com"
    ctx["GA_ID"] = "UA-12345"
    return ctx
```

### Base de données

```python
async def inject_categories(ctx):
    ctx["categories"] = await db.fetch_all("SELECT * FROM categories")
    return ctx
```

### Authentification

```python
async def inject_current_user(ctx):
    user_id = ctx.get("user_id")
    ctx["current_user"] = await get_user(user_id) if user_id else None
    return ctx
```
