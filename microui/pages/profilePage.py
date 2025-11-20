from .base import ProfileConfig
from microui.daisy_ui_kit import Avatar, Button, Card, Input
from markupsafe import Markup # type: ignore
# ============= PAGES DE PROFIL =============

class ProfilePages:
    """Pages de profil utilisateur"""
    
    @staticmethod
    def profile_page(config: ProfileConfig = None) -> Markup: # type: ignore
        """Page de profil configurable"""
        
        
        if config is None:
            config = ProfileConfig()
        
        user = config.get('user', {})
        form_action = config.get('form_action', '/user/profile/update')
        show_avatar = config.get('show_avatar_upload', True)
        show_security = config.get('show_security_section', True)
        editable_fields = config.get('editable_fields', ['full_name', 'email', 'phone', 'city', 'bio'])
        
        # Avatar section
        avatar_html = f"""
        <div class="flex flex-col items-center gap-4">
            {Avatar.render(
                src=user.get("avatar", "https://api.dicebear.com/7.x/avataaars/svg?seed=default"),
                alt=user.get("full_name", "Utilisateur"),
                size="lg"
            )}
            <label class="btn btn-sm btn-outline">
                <input type="file" class="hidden" accept="image/*" />
                Changer la photo
            </label>
        </div>
        """ if show_avatar else ""
        
        # Build form fields dynamically
        form_fields = ""
        field_configs = {
            'full_name': {
                'name': 'full_name',
                'type': 'text',
                'label': 'Nom complet',
                'value': user.get('full_name', ''),
                'classes': 'md:col-span-2'
            },
            'email': {
                'name': 'email',
                'type': 'email',
                'label': 'Email',
                'value': user.get('email', ''),
                'classes': 'md:col-span-2'
            },
            'phone': {
                'name': 'phone',
                'type': 'tel',
                'label': 'Téléphone',
                'value': user.get('phone', '')
            },
            'city': {
                'name': 'city',
                'type': 'text',
                'label': 'Ville',
                'value': user.get('city', '')
            }
        }
        
        for field_name in editable_fields:
            if field_name == 'bio':
                form_fields += f"""
                <div class="form-control md:col-span-2">
                    <label class="label">
                        <span class="label-text">Biographie</span>
                    </label>
                    <textarea class="textarea textarea-bordered" name="bio" rows="4" placeholder="Parlez-nous de vous...">{user.get("bio", "")}</textarea>
                </div>
                """
            elif field_name in field_configs:
                config = field_configs[field_name]
                form_fields += Input.render(**config)
        
        # Security section
        security_html = f"""
        <div class="mt-6">
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
        """ if show_security else ""
        
        return Markup(f"""
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
                            {avatar_html}
                            
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
                                {form_fields}
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
                
                {security_html}
            </div>
        </div>
        """)

