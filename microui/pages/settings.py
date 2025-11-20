from .base import SettingsConfig
from markupsafe import Markup # type: ignore
from microui.daisy_ui_kit import Button, Card, Input
# ============= PARAMÈTRES =============

class SettingsPages:
    """Pages de paramètres configurables"""
    
    @staticmethod
    def general_settings(config: SettingsConfig = None) -> Markup: # type: ignore
        """Paramètres généraux"""
        
        
        if config is None:
            config = SettingsConfig()
        
        settings = config.get('settings', {})
        form_action = config.get('form_action', '/settings/general')
        editable_fields = config.get('editable_fields', ['app_name', 'app_description', 'default_theme', 'public_registration'])
        
        # Build form fields
        form_fields = ""
        
        if 'app_name' in editable_fields:
            form_fields += Input.render(
                name="app_name",
                type="text",
                label="Nom de l'application",
                value=settings.get("app_name", ""),
                classes="mb-4"
            )
        
        if 'app_description' in editable_fields:
            form_fields += Input.render(
                name="app_description",
                type="text",
                label="Description",
                value=settings.get("app_description", ""),
                classes="mb-4"
            )
        
        if 'default_theme' in editable_fields:
            form_fields += """
            <div class="form-control mb-4">
                <label class="label">
                    <span class="label-text">Thème par défaut</span>
                </label>
                <select class="select select-bordered" name="default_theme">
                    <option value="light">Clair</option>
                    <option value="dark" selected>Sombre</option>
                </select>
            </div>
            """
        
        if 'public_registration' in editable_fields:
            form_fields += f"""
            <div class="form-control mb-6">
                <label class="label cursor-pointer">
                    <span class="label-text">Activer les inscriptions publiques</span>
                    <input type="checkbox" class="checkbox checkbox-primary" 
                           name="public_registration" 
                           {'checked' if settings.get("public_registration") else ''} />
                </label>
            </div>
            """
        
        return Markup(f"""
        <div class="min-h-screen bg-base-200 p-4">
            <div class="max-w-2xl mx-auto">
                <h1 class="text-3xl font-bold mb-6">Paramètres</h1>
                
                {Card.render(
                    title="Paramètres de l'application",
                    body=f'''
                        <form method="POST" action="{form_action}" class="space-y-4">
                            {form_fields}
                            
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
        """)