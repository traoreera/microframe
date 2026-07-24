# Django

Commence par `guide.md` pour le flux de base, puis utilise cette page pour integrer MicroFrame dans une app Django.

MicroFrame peut être utilisé comme moteur de rendu dans Django, à la place du template engine Django natif.

## Exemple

```python
# views.py
import asyncio
from django.http import HttpResponse
from microframe import TemplateEngine

engine = TemplateEngine(
    directory="pages/templates",
    enable_ui=True,
    enable_minify=False,
)

async def home(request):
    html = await engine.render("home.html", {
        "title": "Accueil",
        "user": request.user,
    })
    return HttpResponse(html)
```

## Projet exemple

```python
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
]
```

## Avec microui

```python
from microframe import UIComponent, ui_register

@ui_register
class Alert(UIComponent):
    def render(self):
        return f'<div class="alert">{self.props.get("text", "")}</div>'
```

```html
{{ render_microui("alert", text="Hello depuis Django") }}
```

## Avec micro-frontends React

```python
# views.py
async def mfe(request):
    engine.mfe.register("navbar", "http://localhost:4000/fragment/navbar")
    html = await engine.render("mfe_app.html", {"user": "Alice"})
    return HttpResponse(html)
```

```html
<!-- mfe_app.html -->
<body>
  {{ render_mfe("navbar") }}
  <main>
    <h1>Page MFE</h1>
  </main>
</body>
```
