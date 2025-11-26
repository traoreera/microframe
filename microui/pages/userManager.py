# ============= GESTION DES UTILISATEURS =============
from markupsafe import Markup  # type: ignore

from microui.daisy_ui_kit import Card, Table

from .base import UsersManagementConfig


class UsersManagement:
    """Pages de gestion des utilisateurs (admin)"""

    @staticmethod
    def users_list_page(config: UsersManagementConfig = None) -> Markup:  # type: ignore
        """Liste des utilisateurs configurable"""

        if config is None:
            config = UsersManagementConfig()

        users = config.get("users", [])
        page = config.get("page", 1)
        total_pages = config.get("total_pages", 1)
        show_search = config.get("show_search", True)
        actions = config.get("actions", ["edit", "delete", "reset_password"])

        # Build table
        headers = ["ID", "Nom", "Email", "Rôle", "Statut", "Inscription", "Actions"]
        rows = []

        for user in users:
            status_badge = f"""
            <div class="badge {'badge-success' if user.get('status') == 'actif' else 'badge-warning'}">
                {user.get('status', 'inactif').capitalize()}
            </div>
            """

            # Build actions dropdown
            action_items = ""
            if "edit" in actions:
                action_items += (
                    f'<li><a href="/admin/users/{user.get("id")}/edit">Modifier</a></li>'
                )
            if "reset_password" in actions:
                action_items += f'<li><a href="/admin/users/{user.get("id")}/reset-password">Réinit. mot de passe</a></li>'
            if "delete" in actions:
                action_items += f'<li><a class="text-error">Supprimer</a></li>'

            actions_html = f"""
            <div class="dropdown dropdown-end">
                <button class="btn btn-sm btn-ghost">⋮</button>
                <ul class="dropdown-content menu p-2 shadow bg-base-100 rounded-box w-52">
                    {action_items}
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
                    actions_html,
                ]
            )

        # Search bar
        search_html = (
            """
        <div class="mb-4 flex gap-2">
            <input type="text" placeholder="Rechercher..." class="input input-bordered flex-1" />
            <button class="btn btn-outline">Rechercher</button>
        </div>
        """
            if show_search
            else ""
        )

        # Pagination
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
                        {search_html}
                        
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
