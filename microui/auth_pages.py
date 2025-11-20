# auth_pages.py
"""
Pages d'authentification et gestion d'utilisateurs avec DaisyUI
"""
from typing import Optional

from markupsafe import Markup

from .advance import Tabs
from .daisy_ui_kit import Alert, Button, Card, Input, Modal


class AuthPages:
    """Générateur de pages d'authentification"""

    @staticmethod
    def login_page(error: Optional[str] = None, form_action: str = "/auth/login") -> Markup:
        """Page de connexion"""
        error_html = Alert.render(message=error, type="error", dismissible=True) if error else ""

        return Markup(
            f"""
        <div class="min-h-screen bg-gradient-to-br from-base-200 to-base-300 flex items-center justify-center p-4">
            <div class="w-full max-w-md">
                {Card.render(
            title="Connexion",
            body=f'''
                        {error_html}
                        <form method="POST" action="{form_action}" class="space-y-4">
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
                classes="mb-6"
            )}
                            
                            <div class="form-control">
                                <label class="label cursor-pointer">
                                    <span class="label-text">Se souvenir de moi</span>
                                    <input type="checkbox" class="checkbox checkbox-primary" name="remember" />
                                </label>
                            </div>
                            
                            {Button.render(
                text="Se connecter",
                variant="primary",
                size="md",
                block=True,
                classes="mt-6"
            )}
                        </form>
                        
                        <div class="divider">OU</div>
                        
                        <div class="space-y-2">
                            <button class="btn btn-outline btn-block btn-sm">
                                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                                    <path d="M15.545 6.558a9.42 9.42 0 0 1 .139 1.626c0 2.449-.901 4.711-2.484 6.469-1.533 1.634-3.557 2.676-5.848 2.676a6.287 6.287 0 0 1-3.453-1.012 6.326 6.326 0 0 1-1.335-1.623 5.998 5.998 0 0 1-.923-2.34 5.987 5.987 0 0 1 .564-3.456 6.029 6.029 0 0 1 1.379-2.126A5.89 5.89 0 0 1 5.75 3.5c1.059 0 2.062.338 2.981.975a5.738 5.738 0 0 1 1.646 1.193l.812-.812a.5.5 0 1 1 .707.707l-.814.814a5.952 5.952 0 0 1 .214 5.191z"/>
                                </svg>
                                Google
                            </button>
                            <button class="btn btn-outline btn-block btn-sm">
                                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                                    <path fill-rule="evenodd" d="M10 0C4.477 0 0 4.484 0 10.017c0 4.425 2.865 8.18 6.839 9.49.5.092.682-.217.682-.482 0-.237-.008-.868-.013-1.703-2.782.603-3.369-1.343-3.369-1.343-.454-1.156-1.11-1.463-1.11-1.463-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.544 2.914 1.19.092-.926.35-1.545.636-1.9-2.22-.253-4.555-1.11-4.555-4.943 0-1.091.39-1.984 1.029-2.683-.103-.253-.446-1.27.098-2.647 0 0 .84-.269 2.75 1.025A9.578 9.578 0 0 1 10 4.817c.85.004 1.705.114 2.504.336 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.203 2.398.1 2.651.64.699 1.028 1.592 1.028 2.683 0 3.842-2.339 4.687-4.566 4.935.359.309.678.919.678 1.852 0 1.336-.012 2.415-.012 2.743 0 .267.18.578.688.48C17.137 18.191 20 14.432 20 10.017 20 4.484 15.522 0 10 0z" fill-rule="evenodd"/>
                                </svg>
                                GitHub
                            </button>
                        </div>
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
    def register_page(error: Optional[str] = None, form_action: str = "/auth/register") -> Markup:
        """Page d'inscription"""
        error_html = Alert.render(message=error, type="error", dismissible=True) if error else ""

        return Markup(
            f"""
        <div class="min-h-screen bg-gradient-to-br from-base-200 to-base-300 flex items-center justify-center p-4">
            <div class="w-full max-w-md">
                {Card.render(
            title="Créer un compte",
            body=f'''
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
                            
                            <div class="form-control mb-4">
                                <label class="label cursor-pointer">
                                    <span class="label-text text-sm">J'accepte les conditions d'utilisation</span>
                                    <input type="checkbox" class="checkbox checkbox-primary" name="terms" required />
                                </label>
                            </div>
                            
                            {Button.render(
                text="Créer mon compte",
                variant="primary",
                size="md",
                block=True,
                classes="mt-6"
            )}
                        </form>
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
            title="Réinitialiser le mot de passe",
            body=f'''
                        <p class="text-sm text-base-content/70 mb-4">
                            Entrez votre adresse email et nous vous enverrons un lien pour réinitialiser votre mot de passe.
                        </p>
                        
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
                size="md",
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

    @staticmethod
    def profile_page(user: dict, form_action: str = "/user/profile/update") -> Markup:
        """Page de profil utilisateur"""
        from advance import Avatar

        return Markup(
            f"""
        <div class="min-h-screen bg-base-200 p-4">
            <div class="max-w-4xl mx-auto">
                <div class="breadcrumbs text-sm mb-6">
                    <ul>
                        <li><a href="/">Accueil</a></li>
                        <li>Profil</li>
                    </ul>
                </div>
                
                {Card.render(
            title="Mon Profil",
            body=f'''
                        <div class="flex flex-col md:flex-row gap-6 mb-6">
                            <div class="flex flex-col items-center gap-4">
                                {Avatar.render(
                src=user.get(
                    "avatar", "https://api.dicebear.com/7.x/avataaars/svg?seed=default"),
                alt=user.get("full_name", "Utilisateur"),
                size="lg"
            )}
                                <label class="btn btn-sm btn-outline">
                                    <input type="file" class="hidden" accept="image/*" />
                                    Changer la photo
                                </label>
                            </div>
                            
                            <div class="flex-1">
                                <h2 class="text-2xl font-bold mb-2">{user.get("full_name", "N/A")}</h2>
                                <p class="text-base-content/70 mb-4">{user.get("email", "N/A")}</p>
                                
                                <div class="space-y-2 text-sm">
                                    <p><span class="font-semibold">Inscrit le :</span> {user.get("created_at", "N/A")}</p>
                                    <p><span class="font-semibold">Dernière connexion :</span> {user.get("last_login", "N/A")}</p>
                                </div>
                            </div>
                        </div>
                        
                        <div class="divider"></div>
                        
                        <form method="POST" action="{form_action}" class="space-y-4">
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                {Input.render(
                name="full_name",
                type="text",
                label="Nom complet",
                value=user.get("full_name", ""),
                classes="md:col-span-2"
            )}
                                
                                {Input.render(
                name="email",
                type="email",
                label="Email",
                value=user.get("email", ""),
                classes="md:col-span-2"
            )}
                                
                                {Input.render(
                name="phone",
                type="tel",
                label="Téléphone",
                value=user.get("phone", "")
            )}
                                
                                {Input.render(
                name="city",
                type="text",
                label="Ville",
                value=user.get("city", "")
            )}
                            </div>
                            
                            <div class="form-control">
                                <label class="label">
                                    <span class="label-text">Biographie</span>
                                </label>
                                <textarea class="textarea textarea-bordered" name="bio" rows="4" placeholder="Parlez-nous de vous...">{user.get("bio", "")}</textarea>
                            </div>
                            
                            {Button.render(
                text="Enregistrer les modifications",
                variant="primary",
                block=True,
                classes="mt-6"
            )}
                        </form>
                    ''',
            classes="shadow-lg"
        )}
                
                <div class="mt-6 space-y-4">
                    {Card.render(
            title="Sécurité",
            body='''
                            <div class="space-y-3">
                                <button class="btn btn-outline btn-block">
                                    Changer le mot de passe
                                </button>
                                <button class="btn btn-outline btn-block">
                                    Activer l'authentification à deux facteurs
                                </button>
                                <button class="btn btn-outline btn-block">
                                    Voir les sessions actives
                                </button>
                            </div>
                        ''',
            classes="shadow"
        )}
                </div>
            </div>
        </div>
        """
        )

    @staticmethod
    def users_management_page(users: list, page: int = 1, total_pages: int = 1) -> Markup:
        """Page de gestion des utilisateurs (admin)"""
        from daisy_ui_kit import Table

        headers = ["ID", "Nom", "Email", "Rôle", "Statut", "Inscription", "Actions"]
        rows = []

        for user in users:
            status_badge = f"""
                <div class="badge {
                'badge-success' if user.get(
                    'status') == 'actif' else 'badge-warning'
            }">
                    {user.get('status', 'inactif').capitalize()}
                </div>
            """

            actions = f"""
                <div class="dropdown dropdown-end">
                    <button class="btn btn-sm btn-ghost">⋮</button>
                    <ul class="dropdown-content menu p-2 shadow bg-base-100 rounded-box w-52">
                        <li><a href="/admin/users/{user.get("id")}/edit">Modifier</a></li>
                        <li><a href="/admin/users/{user.get("id")}/reset-password">Réinit. mot de passe</a></li>
                        <li><a class="text-error">Supprimer</a></li>
                    </ul>
                </div>
            """

            rows.append(
                [
                    user.get("id", ""),
                    user.get("full_name", ""),
                    user.get("email", ""),
                    user.get("role", "user").capitalize(),
                    status_badge,
                    user.get("created_at", ""),
                    actions,
                ]
            )

        pagination = f"""
            <div class="join mt-6">
                <a href="?page={page-1}" class="join-item btn {'btn-disabled' if page <= 1 else ''}">«</a>
                <button class="join-item btn">Page {page} / {total_pages}</button>
                <a href="?page={page+1}" class="join-item btn {'btn-disabled' if page >= total_pages else ''}">»</a>
            </div>
        """

        return Markup(
            f"""
        <div class="min-h-screen bg-base-200 p-4">
            <div class="max-w-6xl mx-auto">
                <div class="flex justify-between items-center mb-6">
                    <h1 class="text-3xl font-bold">Gestion des utilisateurs</h1>
                    <a href="/admin/users/new" class="btn btn-primary">Nouvel utilisateur</a>
                </div>
                
                {Card.render(
            body=f'''
                        <div class="mb-4 flex gap-2">
                            <input type="text" placeholder="Rechercher..." class="input input-bordered flex-1" />
                            <button class="btn btn-outline">Rechercher</button>
                        </div>
                        
                        {Table.render(
                headers=headers,
                rows=rows,
                zebra=True,
                hoverable=True,
                classes="w-full"
            )}
                        
                        {pagination}
                    ''',
            classes="shadow-lg"
        )}
            </div>
        </div>
        """
        )

    @staticmethod
    def user_form_page(
        user: Optional[dict] = None, form_action: str = "/admin/users/create"
    ) -> Markup:
        """Page d'édition/création d'utilisateur (admin)"""
        is_edit = user is not None
        title = "Modifier l'utilisateur" if is_edit else "Créer un nouvel utilisateur"

        return Markup(
            f"""
        <div class="min-h-screen bg-base-200 p-4">
            <div class="max-w-2xl mx-auto">
                <div class="mb-6">
                    <a href="/admin/users" class="link link-primary">← Retour aux utilisateurs</a>
                </div>
                
                {Card.render(
            title=title,
            body=f'''
                        <form method="POST" action="{form_action}" class="space-y-4">
                            {Input.render(
                name="full_name",
                type="text",
                label="Nom complet",
                value=user.get("full_name", "") if user else "",
                classes="mb-4"
            )}
                            
                            {Input.render(
                name="email",
                type="email",
                label="Email",
                value=user.get("email", "") if user else "",
                classes="mb-4"
            )}
                            
                            <div class="form-control mb-4">
                                <label class="label">
                                    <span class="label-text">Rôle</span>
                                </label>
                                <select class="select select-bordered" name="role" required>
                                    <option value="user" {
                'selected' if user and user.get("role") == "user" else ''
            }>Utilisateur</option>
                                    <option value="moderator" {
                'selected' if user and user.get(
                    "role") == "moderator" else ''
            }>Modérateur</option>
                                    <option value="admin" {
                'selected' if user and user.get(
                    "role") == "admin" else ''
            }>Administrateur</option>
                                </select>
                            </div>
                            
                            <div class="form-control mb-4">
                                <label class="label">
                                    <span class="label-text">Statut</span>
                                </label>
                                <select class="select select-bordered" name="status" required>
                                    <option value="actif" {
                'selected' if user and user.get(
                    "status") == "actif" else ''
            }>Actif</option>
                                    <option value="inactif" {
                'selected' if user and user.get(
                    "status") == "inactif" else ''
            }>Inactif</option>
                                    <option value="suspendu" {
                'selected' if user and user.get(
                    "status") == "suspendu" else ''
            }>Suspendu</option>
                                </select>
                            </div>
                            
                            {
                '' if is_edit else f'''
                                {Input.render(
                    name="password",
                    type="password",
                    label="Mot de passe",
                    placeholder="••••••••",
                    classes="mb-4"
                )}
                                '''
            }
                            
                            <div class="flex gap-2 mt-6">
                                {Button.render(
                text="Enregistrer",
                variant="primary",
                classes="flex-1"
            )}
                                <a href="/admin/users" class="btn flex-1">Annuler</a>
                            </div>
                        </form>
                    ''',
            classes="shadow-lg"
        )}
            </div>
        </div>
        """
        )


# settings_page.py
class SettingsPage:
    """Pages de paramètres"""

    @staticmethod
    def general_settings(settings: dict, form_action: str = "/settings/general") -> Markup:
        """Paramètres généraux de l'application"""
        return Markup(
            f"""
        <div class="min-h-screen bg-base-200 p-4">
            <div class="max-w-2xl mx-auto">
                <h1 class="text-3xl font-bold mb-6">Paramètres généraux</h1>
                
                {Card.render(
            title="Paramètres de l'application",
            body=f'''
                        <form method="POST" action="{form_action}" class="space-y-4">
                            {Input.render(
                name="app_name",
                type="text",
                label="Nom de l'application",
                value=settings.get("app_name", ""),
                classes="mb-4"
            )}
                            
                            {Input.render(
                name="app_description",
                type="text",
                label="Description",
                value=settings.get("app_description", ""),
                classes="mb-4"
            )}
                            
                            <div class="form-control mb-4">
                                <label class="label">
                                    <span class="label-text">Thème par défaut</span>
                                </label>
                                <select class="select select-bordered" name="default_theme">
                                    <option value="light">Clair</option>
                                    <option value="dark" selected>Sombre</option>
                                </select>
                            </div>
                            
                            <div class="form-control mb-6">
                                <label class="label cursor-pointer">
                                    <span class="label-text">Activer les inscriptions publiques</span>
                                    <input type="checkbox" class="checkbox checkbox-primary" 
                                           name="public_registration" 
                                           {'checked' if settings.get("public_registration") else ''} />
                                </label>
                            </div>
                            
                            {Button.render(
                text="Enregistrer les paramètres",
                variant="primary",
                block=True
            )}
                        </form>
                    ''',
            classes="shadow-lg"
        )}
            </div>
        </div>
        """
        )

    @staticmethod
    def email_settings(settings: dict, form_action: str = "/settings/email") -> Markup:
        """Paramètres d'email"""
        return Markup(
            f"""
        <div class="min-h-screen bg-base-200 p-4">
            <div class="max-w-2xl mx-auto">
                <h1 class="text-3xl font-bold mb-6">Paramètres d'email</h1>
                
                {Card.render(
            title="Configuration SMTP",
            body=f'''
                        <form method="POST" action="{form_action}" class="space-y-4">
                            {Input.render(
                name="smtp_host",
                type="text",
                label="Serveur SMTP",
                value=settings.get("smtp_host", ""),
                placeholder="smtp.gmail.com",
                classes="mb-4"
            )}
                            
                            {Input.render(
                name="smtp_port",
                type="number",
                label="Port",
                value=settings.get("smtp_port", "587"),
                classes="mb-4"
            )}
                            
                            {Input.render(
                name="smtp_user",
                type="email",
                label="Email",
                value=settings.get("smtp_user", ""),
                classes="mb-4"
            )}
                            
                            {Input.render(
                name="smtp_password",
                type="password",
                label="Mot de passe",
                placeholder="••••••••",
                classes="mb-4"
            )}
                            
                            {Input.render(
                name="from_email",
                type="email",
                label="Email d'envoi",
                value=settings.get("from_email", ""),
                classes="mb-6"
            )}
                            
                            {Button.render(
                text="Tester la connexion",
                variant="outline",
                classes="mb-4 w-full"
            )}
                            
                            {Button.render(
                text="Enregistrer les paramètres",
                variant="primary",
                block=True
            )}
                        </form>
                    ''',
            classes="shadow-lg"
        )}
            </div>
        </div>
        """
        )
