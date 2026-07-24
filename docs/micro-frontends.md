# Micro-frontends

Si tu decouvres MicroFrame, commence par `guide.md` puis utilise cette page pour brancher des fragments HTTP asynchrones.

MicroFrame peut intégrer des fragments HTML servis par d'autres services HTTP, rendus de manière asynchrone.

## Configuration

```python
from microframe import TemplateEngine

engine = TemplateEngine(directory="templates", mfe_timeout=5.0)
```

## Enregistrement

```python
engine.mfe.register("header", "http://header-service:8000/fragment")
engine.mfe.register("footer", "http://footer-service:8000/fragment")

# Enregistrement multiple
engine.mfe.register_many({
    "cart":   "http://cart-service:8000/fragment",
    "search": "http://search-service:8000/fragment",
})
```

## Utilisation dans un template

```html
<!DOCTYPE html>
<html>
  <head><title>{{ title }}</title></head>
  <body>
    {{ render_mfe("header") }}

    <main>
      <h1>{{ title }}</h1>
      {{ content }}
    </main>

    {{ render_mfe("footer") }}
  </body>
</html>
```

Avec paramètres :

```html
{{ render_mfe("cart", user_id=42) }}
<!-- → GET http://cart-service:8000/fragment?user_id=42 -->
```

## Gestion des erreurs

Si un service MFE est injoignable ou timeout, un commentaire HTML est inséré à la place :

```html
<!-- MFE 'header' timeout -->
<!-- MFE 'cart' HTTP error: 500 -->
<!-- MFE 'header' not found -->
```

## Exemple complet

### Service MFE (Express)

```jsx
// server.jsx — fragment SSR
const express = require("express");
const React = require("react");
const { renderToString } = require("react-dom/server");

const app = express();

app.get("/fragment/navbar", (req, res) => {
  const html = renderToString(<Navbar user={req.query.user} />);
  res.set("Content-Type", "text/html");
  res.send(html);
});

app.listen(4000);
```

### Template MicroFrame

```html
{{ render_mfe("navbar", user="Alice") }}
```
