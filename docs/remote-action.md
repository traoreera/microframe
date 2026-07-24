# Remote & Action

Commence par `guide.md` si tu decouvres le projet, puis utilise cette page pour les tags distants et les formulaires d action.

Tags HTML `<remote>` et `<action>` pour appels de plugins distants et formulaires avec URLs opaques et HTMX. Les valeurs injectees sont echappees et le token CSRF est stable par moteur.

## Remote

Le tag `<remote>` appelle un handler distant (plugin, API, etc.) et affiche le résultat. Si le handler n'est pas disponible, le contenu du tag est utilisé comme fallback.

```html
<remote name="comments.latest" limit="5">
  <p>Chargement…</p>
</remote>

<!-- Self-closing : aucun fallback -->
<remote name="header.notifications" user_id="{{ user.id }}" />
```

### Fonctionnement

1. Le préprocesseur convertit `<remote>` en `{% remote %}…{% endremote %}`
2. Au rendu, `_remote_caller(name, kwargs)` est appelé
3. Si le caller retourne du contenu, il est inséré
4. Sinon, le body du tag est utilisé comme fallback
5. Sans body ni caller, un commentaire HTML est inséré

### Configuration

```python
from microframe import TemplateEngine

async def my_remote_caller(name, kwargs):
    if name == "comments.latest":
        return render_comments(kwargs.get("limit", 5))
    return None

engine = TemplateEngine(
    directory="templates",
    remote_caller=my_remote_caller,
)
```

## Action

Le tag `<action>` génère un formulaire HTML avec URL opaque, token CSRF et attributs HTMX optionnels.

```html
<!-- Formulaire simple -->
<action name="comments.create" redirect="/merci">
  <input name="title" placeholder="Titre">
  <textarea name="content"></textarea>
  <button type="submit">Envoyer</button>
</action>

<!-- Self-closing : soumission immédiate -->
<action name="auth.logout" redirect="/" hx_confirm="Déconnexion ?" />

<!-- Avec HTMX -->
<action name="cart.add" product_id="{{ product.id }}"
       hx_target="#cart-count" hx_swap="outerHTML">
  <button>Ajouter au panier</button>
</action>
```

### Attributs HTMX supportés

| Attribut | Description |
|---|---|
| `hx_target` | Cible du swap |
| `hx_swap` | Mode de swap |
| `hx_trigger` | Déclencheur |
| `hx_push_url` | URL dans l'historique |
| `hx_select` | Sélecteur de contenu |
| `hx_select_oob` | Out-of-band swap |
| `hx_confirm` | Confirmation |
| `hx_on` | Événement JS |

### Configuration

```python
def my_action_resolver(name, kwargs):
    return "/_/a/abc123"

engine = TemplateEngine(
    directory="templates",
    action_resolver=my_action_resolver,
)
```

### Structure générée

```html
<form action="/_/a/abc123" method="POST" hx-target="#cart-count">
  <input type="hidden" name="csrf_token" value="abc…">
  <input type="hidden" name="redirect" value="/merci">
  <!-- contenu original -->
  <button>Ajouter au panier</button>
</form>
```

## Intégration XCore

MicroFrame s'enregistre comme une extension xcore (déclarée dans `xcore.yaml`), et le câblage des tags `<remote>`/`<action>` se fait après `await xcore.boot(app)`. Détail complet : [integration-xcore.md](integration-xcore.md).

```python
from microframe.engine.integration.xcore import bind_engine, register_action_routes

# xcore.setup(app) puis await xcore.boot(app) déjà effectués
engine = xcore.services.get("ext.template_engine").engine
action_map = bind_engine(xcore, engine)

# Enregistre la route POST /_/a/{token}
register_action_routes(app, xcore, engine, action_map)
```
