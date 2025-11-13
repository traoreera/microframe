# microframework/templating/manager.py
"""
Template Manager — Jinja2 + HTMX + Bytecode Cache Optimisé

Fonctionnalités :
- Rendu HTML complet ou partiel (HTMX)
- Cache bytecode pour performance
- Filtres et fonctions globales personnalisables
- Support async complet
- Gestion d'erreurs robuste
- Intégration Depends()
- Templates imbriqués et layouts
- Auto-reload en développement
"""
import os
import logging
from pathlib import Path
from typing import Any, Dict, Optional, Union, Callable
from datetime import datetime
from pathlib import Path
import jinja2
from jinja2 import TemplateNotFound, TemplateSyntaxError
from starlette.requests import Request
from starlette.responses import HTMLResponse

from ..dependencies import Depends

logger = logging.getLogger(__name__)


class TemplateError(Exception):
    """Exception pour erreurs de template"""
    pass


class TemplateManager:
    """
    Gestionnaire de templates Jinja2 avec support HTMX
    
    Support HTMX automatique :
        - Détecte HX-Request header
        - Rend fragments pour requêtes HTMX
        - Rend page complète sinon
    
    Exemple :
        templates = TemplateManager("templates")
        
        @app.get("/users")
        async def users(request: Request, templates = Depends(get_templates)):
            return await templates.render("users/list.html", {
                "users": [...]
            }, request)
    """
    
    _instance: Optional['TemplateManager'] = None
    
    def __init__(
        self,
        directory: Union[str, Path] = "templates",
        auto_reload: bool = None,
        enable_cache: bool = None,
        cache_dir: Union[str, Path] = ".jinja_cache",
        static_url: str = "/static",
        debug: bool = False
    ):
        """
        Initialise le gestionnaire de templates
        
        Args:
            directory: Dossier des templates
            auto_reload: Recharge les templates si modifiés (auto: True en dev, False en prod)
            enable_cache: Active le cache bytecode (auto: False en dev, True en prod)
            cache_dir: Dossier du cache bytecode
            static_url: URL de base pour les fichiers statiques
            debug: Mode debug (logs verbeux)
        """
        self.directory = Path(directory)
        self.cache_dir = Path(cache_dir)
        self.static_url = static_url.rstrip("/")
        self.debug = debug
        
        # Configuration automatique dev/prod
        if auto_reload is None:
            auto_reload = debug or os.getenv("ENV", "development") == "development"
        if enable_cache is None:
            enable_cache = not debug and os.getenv("ENV", "development") == "production"
        
        self.auto_reload = auto_reload
        self.enable_cache = enable_cache
        
        # Vérifier que le dossier existe
        if not self.directory.is_dir():
            raise FileNotFoundError(f"Template directory not found: {self.directory}")
        
        # Configuration du cache bytecode
        bytecode_cache = None
        if enable_cache:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            bytecode_cache = jinja2.FileSystemBytecodeCache(str(self.cache_dir))
            logger.info(f"Template bytecode cache enabled: {self.cache_dir}")
        
        # Configuration de l'environnement Jinja2
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(self.directory)),
            autoescape=jinja2.select_autoescape(["html", "xml", "jinja2"]),
            auto_reload=auto_reload,
            enable_async=True,
            bytecode_cache=bytecode_cache,
            cache_size=500 if enable_cache else 0,
            # Options de sécurité
            trim_blocks=True,
            lstrip_blocks=True,
        )
        
        # Enregistrer les filtres personnalisés
        self._register_filters()
        
        # Enregistrer les fonctions globales
        self._register_globals()
        
        logger.info(f"TemplateManager initialized: {self.directory} (auto_reload={auto_reload}, cache={enable_cache})")
    
    def _register_filters(self):
        """Enregistre les filtres Jinja2 personnalisés"""
        filters = {
            # Texte
            "upper": str.upper,
            "lower": str.lower,
            "title": str.title,
            "capitalize": str.capitalize,
            "truncate": lambda s, length=100, suffix="...": (
                s[:length] + suffix if len(s) > length else s
            ),
            "slugify": lambda s: s.lower().replace(" ", "-").replace("_", "-"),
            
            # Nombres
            "currency": lambda n, symbol="$": f"{symbol}{n:,.2f}",
            "percent": lambda n: f"{n:.1f}%",
            
            # Dates (si datetime fourni)
            "date": lambda d, fmt="%Y-%m-%d": (
                d.strftime(fmt) if isinstance(d, datetime) else str(d)
            ),
            "datetime": lambda d, fmt="%Y-%m-%d %H:%M": (
                d.strftime(fmt) if isinstance(d, datetime) else str(d)
            ),
            "timeago": self._timeago_filter,
            
            # Listes
            "join_and": lambda items: ", ".join(items[:-1]) + " et " + items[-1] if len(items) > 1 else items[0] if items else "",
            
            # HTML
            "safe": lambda s: jinja2.Markup(s),
            "nl2br": lambda s: jinja2.Markup(s.replace("\n", "<br>")),
        }
        
        self.env.filters.update(filters)
        logger.debug(f"Registered {len(filters)} custom filters")
    
    def _register_globals(self):
        """Enregistre les fonctions globales"""
        globals_dict = {
            # HTMX helpers
            "htmx_attrs": self._htmx_attrs,
            "hx": self._htmx_attrs,  # Alias court
            
            # URL helpers
            "static": self._static_path,
            "url": self._url_for,
            
            # Utilitaires
            "now": datetime.now,
            "len": len,
            "enumerate": enumerate,
            "zip": zip,
            
            # Debug
            "debug": self._debug_info,
        }
        
        self.env.globals.update(globals_dict)
        logger.debug(f"Registered {len(globals_dict)} global functions")
    
    async def render(
        self,
        name: str,
        context: Optional[Dict[str, Any]] = None,
        request: Optional[Request] = None,
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None
    ) -> HTMLResponse:
        """
        Rend un template Jinja2
        
        Args:
            name: Nom du template (ex: "users/list.html")
            context: Variables du template
            request: Request Starlette (pour HTMX detection)
            status_code: Code HTTP
            headers: Headers HTTP supplémentaires
        
        Returns:
            HTMLResponse avec le HTML rendu
        """
        context = context or {}
        
        # Ajouter request au contexte
        if request:
            context["request"] = request
            
            # Ajouter des helpers de request
            context.update({
                "method": request.method,
                "path": request.url.path,
                "query": dict(request.query_params),
                "is_htmx": self._is_htmx_request(request),
            })
        
        try:
            # Détecter si c'est une requête HTMX
            is_htmx = request and self._is_htmx_request(request)
            
            # Pour HTMX, on peut rendre un partial
            template_name = name
            if is_htmx and not name.startswith("partials/"):
                # Chercher si un partial existe
                partial_name = f"partials/{name}"
                if self._template_exists(partial_name):
                    template_name = partial_name
                    logger.debug(f"Using partial template for HTMX: {partial_name}")
            
            # Charger le template
            template = self.env.get_template(template_name)
            
            # Rendu asynchrone
            html = await template.render_async(**context)
            
            # Préparer les headers
            response_headers = headers or {}
            
            # Ajouter des headers HTMX si nécessaire
            if is_htmx:
                # Exemple: refresh si nécessaire
                if context.get("hx_refresh"):
                    response_headers["HX-Refresh"] = "true"
                if context.get("hx_redirect"):
                    response_headers["HX-Redirect"] = context["hx_redirect"]
            
            return HTMLResponse(
                content=html,
                status_code=status_code,
                headers=response_headers
            )
        
        except TemplateNotFound as e:
            logger.error(f"Template not found: {name}")
            raise TemplateError(f"Template not found: {name}") from e
        
        except TemplateSyntaxError as e:
            logger.error(f"Template syntax error in {name}: {e}")
            raise TemplateError(f"Template syntax error: {e}") from e
        
        except Exception as e:
            logger.error(f"Error rendering template {name}: {e}", exc_info=True)
            raise TemplateError(f"Error rendering template: {e}") from e
    
    def render_string(
        self,
        template_string: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Rend un template depuis une string
        
        Args:
            template_string: Template Jinja2 en string
            context: Variables du template
        
        Returns:
            HTML rendu
        """
        context = context or {}
        template = self.env.from_string(template_string)
        return template.render(**context)
    
    def add_filter(self, name: str, func: Callable):
        """
        Ajoute un filtre personnalisé
        
        Args:
            name: Nom du filtre
            func: Fonction du filtre
        """
        self.env.filters[name] = func
        logger.debug(f"Added custom filter: {name}")
    
    def add_global(self, name: str, value: Any):
        """
        Ajoute une variable/fonction globale
        
        Args:
            name: Nom de la variable
            value: Valeur ou fonction
        """
        self.env.globals[name] = value
        logger.debug(f"Added global: {name}")
    
    def clear_cache(self):
        """Vide le cache des templates"""
        self.env.cache.clear()
        logger.info("Template cache cleared")
    
    # ========================================================================
    # Méthodes privées / helpers
    # ========================================================================
    
    def _is_htmx_request(self, request: Request) -> bool:
        """Vérifie si c'est une requête HTMX"""
        return request.headers.get("HX-Request", "").lower() == "true"
    
    def _template_exists(self, name: str) -> bool:
        """Vérifie si un template existe"""
        try:
            self.env.get_template(name)
            return True
        except TemplateNotFound:
            return False
    
    def _htmx_attrs(
        self,
        target: Optional[str] = None,
        swap: str = "innerHTML",
        trigger: Optional[str] = None,
        **kwargs
    ):
        """
        Génère des attributs HTMX
        
        Exemple:
            {{ hx(target="#content", swap="outerHTML", trigger="click") }}
            → hx-target="#content" hx-swap="outerHTML" hx-trigger="click"
        """
        attrs = []
        
        if target:
            attrs.append(f'hx-target="{target}"')
        if swap:
            attrs.append(f'hx-swap="{swap}"')
        if trigger:
            attrs.append(f'hx-trigger="{trigger}"')
        
        # Autres attributs HTMX
        for key, value in kwargs.items():
            hx_key = f"hx-{key.replace('_', '-')}"
            attrs.append(f'{hx_key}="{value}"')
        
        return jinja2.Markup(" ".join(attrs))
    
    def _static_path(self, file_path: str) -> str:
        """
        Retourne l'URL complète pour un fichier statique
        
        Exemple:
            {{ static("css/style.css") }} → /static/css/style.css
        """
        return f"{self.static_url}/{file_path.lstrip('/')}"
    
    def _url_for(self, name: str, **params) -> str:
        """
        Génère une URL (à implémenter selon votre router)
        
        Exemple:
            {{ url("user_profile", user_id=123) }}
        """
        # TODO: Intégrer avec votre système de routing
        query = "&".join(f"{k}={v}" for k, v in params.items())
        return f"/{name}?{query}" if query else f"/{name}"
    
    def _timeago_filter(self, dt: datetime) -> str:
        """
        Filtre pour afficher "il y a X minutes/heures/jours"
        """
        if not isinstance(dt, datetime):
            return str(dt)
        
        now = datetime.now()
        diff = now - dt
        
        seconds = diff.total_seconds()
        
        if seconds < 60:
            return "à l'instant"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            return f"il y a {minutes} minute{'s' if minutes > 1 else ''}"
        elif seconds < 86400:
            hours = int(seconds / 3600)
            return f"il y a {hours} heure{'s' if hours > 1 else ''}"
        else:
            days = int(seconds / 86400)
            return f"il y a {days} jour{'s' if days > 1 else ''}"
    
    def _debug_info(self, obj: Any):
        """
        Affiche des infos de debug (seulement en mode debug)
        
        Exemple:
            {{ debug(user) }}
        """
        if not self.debug:
            return jinja2.Markup("")
        
        import pprint
        info = pprint.pformat(obj, indent=2)
        return jinja2.Markup(f"<pre>{jinja2.escape(info)}</pre>")
    
    @classmethod
    def get_instance(cls, **kwargs) -> 'TemplateManager':
        """
        Singleton pattern pour réutiliser la même instance
        """
        if cls._instance is None:
            cls._instance = cls(**kwargs)
        return cls._instance


# =============================================================================
# Dépendance pour injection
# =============================================================================

_template_manager: Optional[TemplateManager] = None


def get_templates(
    directory: str = "templates",
    debug: bool = False
) -> TemplateManager:
    """
    Dépendance pour injection via Depends()
    
    Exemple:
        @app.get("/users")
        async def users(
            request: Request,
            templates = Depends(get_templates)
        ):
            return await templates.render("users.html", {}, request)
    """
    global _template_manager
    
    if _template_manager is None:
        _template_manager = TemplateManager(
            directory=directory,
            debug=debug or os.getenv("DEBUG", "false").lower() == "true"
        )
    
    return _template_manager


def configure_templates(
    directory: str = "templates",
    auto_reload: bool = None,
    enable_cache: bool = None,
    **kwargs
) -> TemplateManager:
    """
    Configure le gestionnaire de templates global
    
    À appeler au démarrage de l'application:
        templates = configure_templates(
            directory="templates",
            debug=True
        )
    """
    global _template_manager
    _template_manager = TemplateManager(
        directory=directory,
        auto_reload=auto_reload,
        enable_cache=enable_cache,
        **kwargs
    )
    return _template_manager





TEMPLATE_STRUCTURE = {
    "": {
        "base.html": """\
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Application{% endblock %}</title>
    
    <link rel="stylesheet" href="{{ static('css/style.css') }}">
    <script src="https://unpkg.com/htmx.org@2.0.0" defer></script>
    <script src="https://unpkg.com/hyperscript.org@0.9.11" defer></script>
    
    {% block head %}{% endblock %}
</head>
<body hx-boost="true">
    {% include 'partials/navbar.html' %}
    
    <main id="content" class="container">
        {% block content %}
        <h1>Bienvenue</h1>
        {% endblock %}
    </main>
    
    {% include 'partials/footer.html' %}
    
    {% block scripts %}
    <script>
        document.addEventListener('htmx:afterSwap', (evt) => {
            console.log('HTMX swap:', evt.detail);
        });
    </script>
    {% endblock %}
</body>
</html>
"""
    },
    "partials": {
        "navbar.html": """\
<nav class="navbar">
    <a href="/" class="logo">🔥 MyApp</a>
    <ul>
        <li><a href="/users" hx-get="/users" hx-target="#content">Utilisateurs</a></li>
        <li><a href="/settings" hx-get="/settings" hx-target="#content">Paramètres</a></li>
    </ul>
</nav>
""",
        "footer.html": """\
<footer class="footer">
    <p>© {{ now().year }} - Propulsé par ton micro-framework ⚙️</p>
</footer>
""",
        "htmx_loader.html": """\
<div class="htmx-loading" 
     hx-ext="class-tools"
     _="on htmx:beforeRequest add .loading to me 
        then on htmx:afterRequest remove .loading from me">
    <div class="spinner"></div>
</div>
"""
    },
    "components": {
        "card.html": """\
<div class="card">
    <h3>{{ title }}</h3>
    <p>{{ content }}</p>
</div>
"""
    },
    "": {
        "index.html": """\
{% extends 'base.html' %}
{% block title %}Accueil{% endblock %}
{% block content %}
<section>
    <h1>🏠 Page d'accueil</h1>
    <p>Ceci est un template Jinja2 avec support HTMX.</p>
    <button hx-get="/users" hx-target="#content" class="btn">Charger les utilisateurs</button>
</section>
{% endblock %}
"""
    }
}


def create_templates(directory:Path):
    for folder, files in TEMPLATE_STRUCTURE.items():
        dir_path = directory / folder
        dir_path.mkdir(parents=True, exist_ok=True)
        for filename, content in files.items():
            file_path = dir_path / filename
            if not file_path.exists():
                file_path.write_text(content.strip() + "\n", encoding="utf-8")

