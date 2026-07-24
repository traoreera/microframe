# Composants

Si tu decouvres MicroFrame, commence par `guide.md` puis reviens ici pour les composants HTML et microui.

MicroFrame gère deux systèmes de composants : les **composants HTML** (fichiers dans `components/`) et les **composants Python** (microui, class-based).

## Composants HTML

Placez des fichiers `.html` dans `templates/components/`. Ils sont automatiquement enregistrés au démarrage.

```html
<!-- templates/components/card.html -->
<div class="card">
  <h2>{{ title }}</h2>
  <div class="content">{{ slot }}</div>
</div>
```

### Syntaxe Jinja2

```html
{% component "card" title="Mon titre" %}
  <p>Contenu du slot</p>
{% endcomponent %}
```

### Syntaxe HTML (recommandée)

La syntaxe `<component.X>` est automatiquement convertie en tags Jinja2 par le préprocesseur.

```html
<component.card title="Mon titre">
  <p>Contenu du slot</p>
</component.card>

<!-- Self-closing -->
<component.avatar src="/img/user.png" />
```

Les props peuvent être des chaînes, des nombres, des booléens ou des expressions Jinja2 :

```html
<component.card title="{{ page.title }}" color="primary" count=42>
  {{ content }}
</component.card>
```

### Enregistrement manuel

```python
from microframe import ComponentRegistry

ComponentRegistry.register("alert", """
  <div class="alert {{ type }}">
    {{ slot }}
  </div>
""")
```

```html
{% component "alert" type="warning" %}
  Attention !
{% endcomponent %}
```

## Composants Python (microui)

Système de composants Python class-based, activé avec `enable_ui=True` et rendu avec une instance neuve a chaque appel.

```python
from microframe import UIComponent, ui_register

@ui_register
class Alert(UIComponent):
    def render(self):
        return f'<div class="alert">{self.props.get("text", "")}</div>'
```

```html
{{ render_microui("alert", text="Hello") }}
```

### Props et enfants

```python
@ui_register
class Card(UIComponent):
    def render(self):
        title = self.props.get("title", "")
        children = self.props.get("children", "")
        return f"""
        <div class="card">
            <h2>{title}</h2>
            <div class="content">{children}</div>
        </div>
        """
```

```html
{{ render_microui("card", title="Titre", children="<p>Contenu</p>") }}
```
