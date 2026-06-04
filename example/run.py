"""
Test du moteur MicroFrame.
Exécuter depuis le dossier example/ :
    python run.py
"""

import asyncio
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Rendre microframe importable depuis example/
sys.path.insert(0, str(Path(__file__).parent.parent))

from microframe import TemplateEngine


async def main():
    engine = TemplateEngine(
        directory="templates",
        debug=True,
        enable_minify=False,   # False pour lisibilité en dev
        enable_cache=False,
    )

    # Versionnement d'un asset
    engine.set_asset_version("style.css", "1.0.0")

    # Contexte de test
    ctx = {
        "user": "Eliezer",
        "title": "Mon Super Article De Blog",
        "description": "Ceci est une longue description qui devrait être tronquée car elle dépasse la limite fixée.",
        "price": 1299.99,
        "published_at": datetime.now() - timedelta(minutes=42),
        "data": {"id": 1, "tags": ["python", "jinja2"], "active": True},
        "items": ["Pomme", "Banane", "Cerise", "Mangue", "Fraise", "Kiwi", "Ananas"],
        "current_page": 2,
    }

    print("=== Rendu de index.html ===\n")
    html = await engine.render("index.html", ctx)
    print(html)

    # Sauvegarder dans un fichier pour ouvrir dans le navigateur
    output = Path("output.html")
    output.write_text(html)
    print(f"\n→ HTML sauvegardé dans {output.resolve()}")

    # Test cache
    print("\n=== Test cache ===")

    from microframe import CacheManager

    class InstrumentedCache(CacheManager):
        def __init__(self):
            super().__init__()
            self.hits = 0
            self.misses = 0

        def get(self, key, ttl=None):
            value = super().get(key, ttl)
            if value is None:
                self.misses += 1
            else:
                self.hits += 1
            return value

    cache = InstrumentedCache()
    engine2 = TemplateEngine(
        directory="templates",
        enable_cache=True,
        cache_ttl=60,
        cache_backend=cache,
    )

    await engine2.render("index.html", ctx)   # miss attendu
    await engine2.render("index.html", ctx)   # hit attendu
    await engine2.render("index.html", ctx)   # hit attendu

    print(f"  Hits  : {cache.hits}   (attendu: 2)")
    print(f"  Misses: {cache.misses}  (attendu: 1)")
    assert cache.hits == 2 and cache.misses == 1, "ECHEC — cache ne fonctionne pas"
    print("  Cache OK ✓")

    # Test expiration TTL
    import time
    cache_ttl = InstrumentedCache()
    engine3 = TemplateEngine(
        directory="templates",
        enable_cache=True,
        cache_ttl=1,
        cache_backend=cache_ttl,
    )
    await engine3.render("index.html", ctx)   # miss
    time.sleep(1.1)
    await engine3.render("index.html", ctx)   # miss (TTL expiré)
    print(f"  TTL expiré — Misses: {cache_ttl.misses}  (attendu: 2)")
    assert cache_ttl.misses == 2, "ECHEC — expiration TTL ne fonctionne pas"
    print("  TTL OK ✓")

    # Test liste des templates
    print("\n=== Templates disponibles ===")
    for t in engine.list_templates():
        print(f"  {t}")


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)   # CWD = example/
    asyncio.run(main())
