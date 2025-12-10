#!/usr/bin/env python3
"""
Script pour ajouter une navigation unifiée à tous les fichiers de documentation MicroFrame
"""

from pathlib import Path

# Configuration des footers de navigation par module
NAVIGATION_TEMPLATES = {
    "microframe": """
---

## 📖 Navigation

**Documentation Modules Core** :
- [Index Modules](README.md)
- [Application](application.md)
- [Config](config.md)
- [Router](router.md)
- [Routing Models](routing_models.md)
- [Route Registry](registry.md)
- [Routing Decorators](decorators.md)
- [Dependencies](dependencies.md)
- [Validation](validation.md)
- [Middleware](middleware.md)
- [Exceptions](exceptions.md)
- [Templates](templates.md)
- [UI Components](ui.md)
- [Configurations](configurations.md)
- [OpenAPI Generator](openapi.md)
- [Documentation UI](docs_ui.md)
- [Logger](logger.md)

---

**[↑ Index Principal](../README.md)** | **[📚 Guides Pratiques](../guides/getting-started.md)**
""",
    "authx": """
---

## 📖 Navigation

**Documentation AuthX** :
- [Introduction](intro.md)
- [Configuration](config.md)
- [JWT Tokens](jwt.md)
- [Auth Manager](manager.md)
- [Models](model.md)
- [Exceptions](exceptions.md)
- [Dependencies](dependencies.md)
- [Security](security.md)
- [License](LICENSE.md)

---

**[↑ Index Principal](../README.md)** | **[📚 Guide Authentication](../guides/authentication.md)**
""",
    "ws": """
---

## 📖 Navigation

**Documentation WebSocket** :
- [WebSocket Manager](websocket.md)

---

**[↑ Index Principal](../README.md)** | **[📚 Guide WebSocket](../guides/websocket-chat.md)**
""",
}


def add_navigation_footer(file_path: Path, navigation_template: str):
    """Ajoute un footer de navigation à un fichier markdown"""

    # Lire le contenu actuel
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Vérifier si navigation existe déjà
    if "## 📖 Navigation" in content:
        print(f"✓ {file_path.name} - Navigation déjà présente")
        return False

    # Supprimer ancien footer simple si présent
    if "**[Back to" in content or "📚 **[Back to" in content:
        lines = content.split("\n")
        # Trouver et supprimer les dernières lignes de footer
        while lines and (
            lines[-1].strip() == "" or "**[Back to" in lines[-1] or "---" in lines[-1]
        ):
            lines.pop()
        content = "\n".join(lines)

    # Ajouter nouveau footer
    new_content = content.rstrip() + "\n" + navigation_template

    # Écrire le nouveau contenu
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"✅ {file_path.name} - Navigation ajoutée")
    return True


def main():
    """Fonction principale"""
    docs_dir = Path("/home/eliezer/devs/microframework/docs")

    updated_count = 0

    # Traiter microframe/
    microframe_dir = docs_dir / "microframe"
    if microframe_dir.exists():
        print("\n📁 Traitement microframe/...")
        for md_file in microframe_dir.glob("*.md"):
            if md_file.name not in ["templates.md", "configurations.md"]:  # Déjà fait
                if add_navigation_footer(md_file, NAVIGATION_TEMPLATES["microframe"]):
                    updated_count += 1

    # Traiter authx/
    authx_dir = docs_dir / "authx"
    if authx_dir.exists():
        print("\n📁 Traitement authx/...")
        for md_file in authx_dir.glob("*.md"):
            if add_navigation_footer(md_file, NAVIGATION_TEMPLATES["authx"]):
                updated_count += 1

    # Traiter ws/
    ws_dir = docs_dir / "ws"
    if ws_dir.exists():
        print("\n📁 Traitement ws/...")
        for md_file in ws_dir.glob("*.md"):
            if add_navigation_footer(md_file, NAVIGATION_TEMPLATES["ws"]):
                updated_count += 1

    print(f"\n✅ Terminé ! {updated_count} fichiers mis à jour")


if __name__ == "__main__":
    main()
