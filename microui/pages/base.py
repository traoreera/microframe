from typing import List, Optional, TypedDict

from markupsafe import Markup  # type: ignore

# ============= TYPES =============


class LoginConfig(TypedDict, total=False):
    """Configuration pour la page de login"""

    error: Optional[str]
    form_action: str
    show_remember_me: bool
    show_social_login: bool
    social_providers: List[str]  # ['google', 'github', 'facebook']
    redirect_to: Optional[str]
    title: str
    subtitle: Optional[str]
    logo: Optional[str]
    background_class: str


class RegisterConfig(TypedDict, total=False):
    """Configuration pour la page d'inscription"""

    error: Optional[str]
    form_action: str
    show_terms: bool
    show_social_register: bool
    social_providers: List[str]
    require_phone: bool
    require_full_name: bool
    title: str
    subtitle: Optional[str]
    logo: Optional[str]
    background_class: str


class ProfileConfig(TypedDict, total=False):
    """Configuration pour la page de profil"""

    user: dict
    form_action: str
    show_avatar_upload: bool
    show_security_section: bool
    # ['full_name', 'email', 'phone', 'city', 'bio']
    editable_fields: List[str]
    custom_fields: List[dict]
    title: str


class UsersManagementConfig(TypedDict, total=False):
    """Configuration pour la gestion des utilisateurs"""

    users: List[dict]
    page: int
    total_pages: int
    show_search: bool
    show_filters: bool
    actions: List[str]  # ['edit', 'delete', 'reset_password', 'suspend']
    custom_columns: List[dict]


class SettingsConfig(TypedDict, total=False):
    """Configuration pour les paramètres"""

    settings: dict
    form_action: str
    sections: List[dict]
    show_test_button: bool  # Pour email settings
    editable_fields: List[str]


# ============= COMPOSANTS DE BASE =============
class AuthComponents:
    """Composants réutilisables pour l'authentification"""

    @staticmethod
    # type: ignore
    def social_login_buttons(providers: List[str] = None) -> str:
        """Boutons de connexion sociale"""
        if providers is None:
            providers = ["google", "github"]

        buttons_config = {
            "google": {
                "icon": '<svg class="w-5 h-5" viewBox="0 0 24 24"><path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/></svg>',
                "text": "Google",
                "class": "btn-outline",
            },
            "github": {
                "icon": '<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>',
                "text": "GitHub",
                "class": "btn-outline",
            },
            "facebook": {
                "icon": '<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>',
                "text": "Facebook",
                "class": "btn-outline",
            },
        }

        buttons_html = ""
        for provider in providers:
            if provider in buttons_config:
                config = buttons_config[provider]
                buttons_html += f"""
                <button class="btn {config['class']} btn-block btn-sm" onclick="window.location.href='/auth/{provider}'">
                    {config['icon']}
                    {config['text']}
                </button>
                """

        return f"""
        <div class="divider">OU</div>
        <div class="space-y-2">
            {buttons_html}
        </div>
        """

    @staticmethod
    def auth_header(title: str, subtitle: Optional[str] = None, logo: Optional[str] = None) -> str:
        """En-tête d'authentification"""
        logo_html = f'<img src="{logo}" alt="Logo" class="h-12 mb-4" />' if logo else ""
        subtitle_html = (
            f'<p class="text-sm text-base-content/70 mt-2">{subtitle}</p>' if subtitle else ""
        )

        return f"""
        <div class="text-center mb-6">
            {logo_html}
            <h2 class="text-2xl font-bold">{title}</h2>
            {subtitle_html}
        </div>
        """
