# CLI

Commence par `guide.md` si tu veux le flux complet, puis utilise cette page pour le rendu, le build et le scaffold.

L'outil en ligne de commande `microframe` permet de rendre des templates, générer des sites statiques et créer des composants.

## Installation

Le CLI est disponible dès l'installation du package :

```bash
microframe --help
```

## Commandes

### render

Rend un template unique et affiche le résultat sur stdout ou l'écrit dans un fichier.

```bash
# Afficher sur stdout
microframe render index.html --dir templates --ctx context.json

# Écrire dans un fichier
microframe render index.html \
    --dir templates \
    --ctx context.json \
    --out dist/index.html

# Contexte depuis stdin
echo '{"title": "Test"}' | microframe render index.html --ctx -

# Désactiver la minification
microframe render index.html --ctx ctx.json --no-minify
```

### build

Rend tous les templates d'un dossier vers un dossier de sortie.

```bash
# Générer tout le site
microframe build --dir templates --ctx context.json --out dist/

# Build sans minification
microframe build --dir templates --ctx ctx.json --out dist/ --no-minify
```

Seuls les fichiers `.html`, `.htm`, `.xml`, `.svg` sont rendus. Les autres fichiers (`.py`, `.css`, etc.) sont ignorés.

### scaffold

Crée un fichier de composant prêt à l'emploi.

```bash
# Composant HTML (défaut)
microframe scaffold component card --dir templates
# → crée templates/components/card.html

# Composant Python (microui)
microframe scaffold component alert --type py --dir templates
# → crée templates/alert.py
```

#### HTML scaffold

```html
<!-- templates/components/card.html -->
<div class="card">
  {{ slot }}
</div>
```

#### Python scaffold

```python
# templates/alert.py
from microframe import UIComponent, ui_register


@ui_register
class Alert(UIComponent):
    def render(self):
        return f'<div class="alert">{{ self.props.get("slot", "") }}</div>'
```
