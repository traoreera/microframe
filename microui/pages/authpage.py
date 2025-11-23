
from markupsafe import Markup  # type: ignore

from microui.daisy_ui_kit import Alert, Button, Card, Input

from .base import AuthComponents, LoginConfig, RegisterConfig

# ============= PAGES D'AUTHENTIFICATION =============


class AuthPages:
    """Générateur de pages d'authentification configurables"""

    @staticmethod
    def login_page(config: LoginConfig = None) -> Markup:  # type: ignore
        """Page de connexion configurable"""

        # Valeurs par défaut
        if config is None:
            config = LoginConfig()

        error = config.get("error")
        form_action = config.get("form_action", "/auth/login")
        show_remember_me = config.get("show_remember_me", True)
        show_social = config.get("show_social_login", True)
        social_providers = config.get("social_providers", ["google", "github"])
        title = config.get("title", "Connexion")
        subtitle = config.get("subtitle")
        logo = config.get("logo")
        bg_class = config.get("background_class", "bg-gradient-to-br from-base-200 to-base-300")

        # Composants conditionnels
        error_html = Alert.render(message=error, type="error", dismissible=True) if error else ""

        remember_me_html = (
            """
        <div class="form-control">
            <label class="label cursor-pointer">
                <span class="label-text">Se souvenir de moi</span>
                <input type="checkbox" class="checkbox checkbox-primary" name="remember" />
            </label>
        </div>
        """
            if show_remember_me
            else ""
        )

        social_html = AuthComponents.social_login_buttons(social_providers) if show_social else ""

        return Markup(
            f"""
        <div class="min-h-screen {bg_class} flex items-center justify-center p-4">
            <div class="w-full max-w-md">
                {Card.render(
            body=f'''
                        {AuthComponents.auth_header(title, subtitle, logo)}
                        <div id="result">{error_html}</div>
                        <form hx-post="{form_action}" hx-target="#result" hx-swap="innerHTML">
                            {Input.render(
                name="email",
                type="email",
                label="Email",
                placeholder="votre@email.com",
                classes="mb-4"
            )}
                            
                            {Input.render(
                name="password",
                type="password",
                label="Mot de passe",
                placeholder="••••••••",
                classes="mb-4"
            )}
                            
                            <div class="flex justify-between items-center mb-4">
                                <a href="/auth/forgot-password" class="link link-primary text-sm">
                                    Mot de passe oublié ?
                                </a>
                            </div>
                            
                            {remember_me_html}
                            
                            {Button.render(
                text="Se connecter",
                variant="primary",
                block=True,
                classes="mt-6"
            )}
                        </form>
                        
                        {social_html}
                    ''',
            classes="shadow-lg"
        )}
                
                <div class="text-center mt-6">
                    <p class="text-sm text-base-content/70">
                        Pas de compte ? <a href="/auth/register" class="link link-primary font-semibold">Créer un compte</a>
                    </p>
                </div>
            </div>
        </div>
        """
        )

    @staticmethod
    def register_page(config: RegisterConfig = None) -> Markup:  # type: ignore
        """Page d'inscription configurable"""

        if config is None:
            config = RegisterConfig()

        error = config.get("error")
        form_action = config.get("form_action", "/auth/register")
        show_terms = config.get("show_terms", True)
        show_social = config.get("show_social_register", True)
        social_providers = config.get("social_providers", ["google", "github"])
        require_phone = config.get("require_phone", False)
        title = config.get("title", "Créer un compte")
        subtitle = config.get("subtitle")
        logo = config.get("logo")
        bg_class = config.get("background_class", "bg-gradient-to-br from-base-200 to-base-300")

        error_html = Alert.render(message=error, type="error", dismissible=True) if error else ""

        phone_field = (
            Input.render(
                name="phone",
                type="tel",
                label="Téléphone",
                placeholder="+33 6 12 34 56 78",
                classes="mb-3",
            )
            if require_phone
            else ""
        )

        terms_html = (
            """
        <div class="form-control mb-4">
            <label class="label cursor-pointer">
                <span class="label-text text-sm">J'accepte les conditions d'utilisation</span>
                <input type="checkbox" class="checkbox checkbox-primary" name="terms" required />
            </label>
        </div>
        """
            if show_terms
            else ""
        )

        social_html = AuthComponents.social_login_buttons(social_providers) if show_social else ""

        return Markup(
            f"""
        <div class="min-h-screen {bg_class} flex items-center justify-center p-4">
            <div class="w-full max-w-md">
                {Card.render(
            body=f'''
                        {AuthComponents.auth_header(title, subtitle, logo)}
                        {error_html}
                        <form method="POST" action="{form_action}" class="space-y-3">
                            {Input.render(
                name="full_name",
                type="text",
                label="Nom complet",
                placeholder="Jean Dupont",
                classes="mb-3"
            )}
                            
                            {Input.render(
                name="email",
                type="email",
                label="Email",
                placeholder="votre@email.com",
                classes="mb-3"
            )}
                            
                            {phone_field}
                            
                            {Input.render(
                name="password",
                type="password",
                label="Mot de passe",
                placeholder="••••••••",
                classes="mb-3"
            )}
                            
                            {Input.render(
                name="confirm_password",
                type="password",
                label="Confirmer le mot de passe",
                placeholder="••••••••",
                classes="mb-4"
            )}
                            
                            {terms_html}
                            
                            {Button.render(
                text="Créer mon compte",
                variant="primary",
                block=True,
                classes="mt-6"
            )}
                        </form>
                        
                        {social_html}
                    ''',
            classes="shadow-lg"
        )}
                
                <div class="text-center mt-6">
                    <p class="text-sm text-base-content/70">
                        Vous avez déjà un compte ? <a href="/auth/login" class="link link-primary font-semibold">Se connecter</a>
                    </p>
                </div>
            </div>
        </div>
        """
        )

    @staticmethod
    def forgot_password_page(form_action: str = "/auth/forgot-password") -> Markup:
        """Page de réinitialisation du mot de passe"""

        return Markup(
            f"""
        <div class="min-h-screen bg-gradient-to-br from-base-200 to-base-300 flex items-center justify-center p-4">
            <div class="w-full max-w-md">
                {Card.render(
            body=f'''
                        {AuthComponents.auth_header(
                "Réinitialiser le mot de passe",
                "Entrez votre adresse email et nous vous enverrons un lien pour réinitialiser votre mot de passe."
            )}
                        
                        <form method="POST" action="{form_action}" class="space-y-4">
                            {Input.render(
                name="email",
                type="email",
                label="Email",
                placeholder="votre@email.com",
                classes="mb-6"
            )}
                            
                            {Button.render(
                text="Envoyer le lien",
                variant="primary",
                block=True
            )}
                        </form>
                    ''',
            classes="shadow-lg"
        )}
                
                <div class="text-center mt-6">
                    <a href="/auth/login" class="link link-primary text-sm">Retour à la connexion</a>
                </div>
            </div>
        </div>
        """
        )
