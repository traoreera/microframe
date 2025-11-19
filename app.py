"""
Application complète avec toutes les pages et layouts
"""

from starlette.requests import Request
from starlette.responses import HTMLResponse

from microframe import Application, Router
from microui.daisy_ui_kit import *
from microui.thems import ThemeManager, setup_daisy_ui

app = Application()
router = Router("/", tags=["App"])


# ============= PAGE D'ACCUEIL =============


@router.get("/")
async def home(request: Request):
    """Page d'accueil complète"""
    theme = ThemeManager.get_theme(request)
    html = DefaultPages.home_page(theme=theme)
    return HTMLResponse(html)


# ============= PAGES D'AUTHENTIFICATION =============


@router.get("/auth/login")
async def login_page(request: Request):
    """Page de connexion"""
    html = AuthPages.login_page(brand_name="MonApp", social_login=True, remember_me=True)
    return HTMLResponse(html)


@router.post("/auth/login")
async def login_submit(request: Request):
    """Traitement du login"""
    form_data = await request.form()
    form_data.get("email")
    form_data.get("password")

    # TODO: Vérifier les credentials
    # Pour la démo, on redirige vers le dashboard
    from starlette.responses import RedirectResponse

    return RedirectResponse(url="/dashboard", status_code=303)


@router.get("/auth/register")
async def register_page(request: Request):
    """Page d'inscription"""
    html = AuthPages.register_page(brand_name="MonApp", social_register=True, terms_required=True)
    return HTMLResponse(html)


@router.post("/auth/register")
async def register_submit(request: Request):
    """Traitement de l'inscription"""
    await request.form()
    # TODO: Créer le compte utilisateur
    return HTMLResponse(Alert.render("Compte créé avec succès !", type="success"))


@router.get("/auth/forgot-password")
async def forgot_password_page(request: Request):
    """Page mot de passe oublié"""
    html = AuthPages.forgot_password_page(brand_name="MonApp")
    return HTMLResponse(html)


@router.post("/auth/forgot-password")
async def forgot_password_submit(request: Request):
    """Envoi du lien de réinitialisation"""
    form_data = await request.form()
    email = form_data.get("email")
    return HTMLResponse(Alert.render(f"Email de réinitialisation envoyé à {email}", type="success"))


# ============= DASHBOARD =============


@router.get("/dashboard")
async def dashboard(request: Request):
    """Dashboard principal"""
    theme = ThemeManager.get_theme(request)

    stats_html = Stats.render(
        stats=[
            {"title": "Total Projets", "value": "12", "desc": "↗︎ 3 ce mois", "color": "primary"},
            {
                "title": "Tâches en cours",
                "value": "24",
                "desc": "8 terminées aujourd'hui",
                "color": "secondary",
            },
            {"title": "Équipe", "value": "8", "desc": "2 nouveaux membres", "color": "accent"},
        ]
    )

    recent_activity = Timeline.render(
        items=[
            {
                "title": "Projet créé",
                "content": "<p>Nouveau projet 'Refonte Website'</p>",
                "date": "Il y a 2h",
            },
            {
                "title": "Tâche terminée",
                "content": "<p>Design de la page d'accueil</p>",
                "date": "Il y a 5h",
            },
            {
                "title": "Membre ajouté",
                "content": "<p>Alice a rejoint l'équipe</p>",
                "date": "Hier",
            },
        ],
        compact=True,
    )

    content = f"""
    <div class="space-y-8">
        <div>
            <h2 class="text-3xl font-bold mb-4">Dashboard</h2>
            <p class="text-base-content/70">Vue d'ensemble de votre activité</p>
        </div>
        
        {stats_html}
        
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div class="card bg-base-100 shadow-xl">
                <div class="card-body">
                    <h3 class="card-title">Activité récente</h3>
                    {recent_activity}
                </div>
            </div>
            
            <div class="card bg-base-100 shadow-xl">
                <div class="card-body">
                    <h3 class="card-title">Actions rapides</h3>
                    <div class="space-y-2">
                        {Button.render("➕ Nouveau projet", variant="primary", block=True)}
                        {Button.render("📝 Créer une tâche", variant="secondary", block=True)}
                        {Button.render("👥 Inviter un membre", variant="accent", block=True)}
                    </div>
                </div>
            </div>
        </div>
    </div>
    """

    html = Layouts.dashboard_layout(
        title="Dashboard",
        user_name="John Doe",
        user_avatar="https://i.pravatar.cc/150?img=3",
        content=content,
        theme=theme,
        sidebar_items=[
            {"text": "Dashboard", "href": "/dashboard", "icon": "📊", "active": True},
            {"text": "Projets", "href": "/projects", "icon": "📁"},
            {"text": "Tâches", "href": "/tasks", "icon": "✅"},
            {"text": "Équipe", "href": "/team", "icon": "👥"},
            {"text": "Calendrier", "href": "/calendar", "icon": "📅"},
            {"text": "Paramètres", "href": "/settings", "icon": "⚙️"},
        ],
    )

    return HTMLResponse(html)


# ============= PROJETS =============


@router.get("/projects")
async def projects(request: Request):
    """Liste des projets"""
    theme = ThemeManager.get_theme(request)

    projects_data = [
        {
            "title": "Refonte Website",
            "description": "Modernisation complète du site web",
            "status": "En cours",
            "progress": 65,
            "team": 5,
        },
        {
            "title": "Application Mobile",
            "description": "Développement app iOS et Android",
            "status": "Planifié",
            "progress": 20,
            "team": 3,
        },
        {
            "title": "Migration Cloud",
            "description": "Migration infrastructure vers AWS",
            "status": "Terminé",
            "progress": 100,
            "team": 4,
        },
    ]

    cards_html = ""
    for project in projects_data:
        status_color = {"En cours": "warning", "Planifié": "info", "Terminé": "success"}.get(
            project["status"], "neutral"
        )

        cards_html += Card.render(
            title=project["title"],
            body=f"""
                <p>{project['description']}</p>
                <div class="mt-4">
                    {Badge.render(project['status'], variant=status_color)}
                    {Badge.render(f"👥 {project['team']} membres", variant="ghost")}
                </div>
                {Progress.render(project['progress'], color=status_color)}
                <div class="text-sm text-right mt-2">{project['progress']}%</div>
            """,
            actions=f"""
                {Button.render("Voir", variant="primary", size="sm")}
                {Button.render("Éditer", variant="ghost", size="sm")}
            """,
            bordered=True,
            classes="mb-4",
        )

    content = f"""
    <div class="space-y-6">
        <div class="flex justify-between items-center">
            <div>
                <h2 class="text-3xl font-bold">Projets</h2>
                <p class="text-base-content/70">Gérez tous vos projets</p>
            </div>
            {Button.render("➕ Nouveau projet", variant="primary")}
        </div>
        
        {cards_html}
    </div>
    """

    html = Layouts.dashboard_layout(
        title="Projets",
        user_name="John Doe",
        content=content,
        theme=theme,
        sidebar_items=[
            {"text": "Dashboard", "href": "/dashboard", "icon": "📊"},
            {"text": "Projets", "href": "/projects", "icon": "📁", "active": True},
            {"text": "Tâches", "href": "/tasks", "icon": "✅"},
            {"text": "Équipe", "href": "/team", "icon": "👥"},
            {"text": "Calendrier", "href": "/calendar", "icon": "📅"},
            {"text": "Paramètres", "href": "/settings", "icon": "⚙️"},
        ],
    )

    return HTMLResponse(html)


# ============= KANBAN =============


@router.get("/kanban")
async def kanban(request: Request):
    """Vue Kanban"""
    theme = ThemeManager.get_theme(request)

    columns = [
        {
            "title": "À faire",
            "tasks": [
                {
                    "title": "Design homepage",
                    "description": "Créer les maquettes",
                    "priority": "Haute",
                    "assignee_avatar": "https://i.pravatar.cc/100?img=1",
                },
                {
                    "title": "Setup database",
                    "description": "Configuration PostgreSQL",
                    "priority": "Moyenne",
                    "assignee_avatar": "https://i.pravatar.cc/100?img=2",
                },
            ],
        },
        {
            "title": "En cours",
            "tasks": [
                {
                    "title": "API Development",
                    "description": "Routes REST",
                    "priority": "Haute",
                    "assignee_avatar": "https://i.pravatar.cc/100?img=3",
                }
            ],
        },
        {
            "title": "En revue",
            "tasks": [
                {
                    "title": "Tests unitaires",
                    "description": "Couverture 80%",
                    "priority": "Moyenne",
                    "assignee_avatar": "https://i.pravatar.cc/100?img=4",
                }
            ],
        },
        {
            "title": "Terminé",
            "tasks": [
                {
                    "title": "Setup projet",
                    "description": "Repository et CI/CD",
                    "priority": "Haute",
                    "assignee_avatar": "https://i.pravatar.cc/100?img=5",
                }
            ],
        },
    ]

    html = AdvancedLayouts.kanban_layout(title="Board Kanban", columns=columns, theme=theme)

    return HTMLResponse(html)


# ============= PARAMÈTRES =============


@router.get("/settings")
async def settings(request: Request):
    """Page de paramètres"""
    theme = ThemeManager.get_theme(request)

    user = {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "+33 6 12 34 56 78",
        "bio": "Développeur passionné",
        "avatar": "https://i.pravatar.cc/150?img=3",
        "premium": True,
    }

    settings_content = SettingsPage.render(user, theme)

    html = Layouts.dashboard_layout(
        title="Paramètres",
        user_name=user["name"],
        user_avatar=user["avatar"],
        content=settings_content,
        theme=theme,
        sidebar_items=[
            {"text": "Dashboard", "href": "/dashboard", "icon": "📊"},
            {"text": "Projets", "href": "/projects", "icon": "📁"},
            {"text": "Tâches", "href": "/tasks", "icon": "✅"},
            {"text": "Équipe", "href": "/team", "icon": "👥"},
            {"text": "Calendrier", "href": "/calendar", "icon": "📅"},
            {"text": "Paramètres", "href": "/settings", "icon": "⚙️", "active": True},
        ],
    )

    return HTMLResponse(html)


# ============= À PROPOS =============


@router.get("/about")
async def about(request: Request):
    """Page à propos"""
    theme = ThemeManager.get_theme(request)
    html = DefaultPages.about_page(theme=theme)
    return HTMLResponse(html)


# ============= PAGES D'ERREUR =============


@router.get("/404")
async def error_404(request: Request):
    """Page 404"""
    theme = ThemeManager.get_theme(request)
    html = DefaultPages.error_404_page(theme=theme)
    return HTMLResponse(html)


@router.get("/500")
async def error_500(request: Request):
    """Page 500"""
    theme = ThemeManager.get_theme(request)
    html = DefaultPages.error_500_page(theme=theme)
    return HTMLResponse(html)


@router.get("/maintenance")
async def maintenance(request: Request):
    """Page maintenance"""
    theme = ThemeManager.get_theme(request)
    html = DefaultPages.maintenance_page(theme=theme)
    return HTMLResponse(html)


# ============= CONTACT =============


@router.post("/contact")
async def contact_submit(request: Request):
    """Traitement du formulaire de contact"""
    form_data = await request.form()
    name = form_data.get("name")
    form_data.get("email")
    form_data.get("message")

    return HTMLResponse(
        Alert.render(
            f"Merci {name} ! Nous avons bien reçu votre message.", type="success", dismissible=True
        )
    )


# Configuration de l'app
setup_daisy_ui(app=app, router=router)
app.include_router(router, prefix="/")


# Handler d'erreurs personnalisé
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    theme = ThemeManager.get_theme(request)
    html = DefaultPages.error_404_page(theme=theme)
    return HTMLResponse(html, status_code=404)


@app.exception_handler(500)
async def server_error_handler(request: Request, exc):
    theme = ThemeManager.get_theme(request)
    html = DefaultPages.error_500_page(theme=theme)
    return HTMLResponse(html, status_code=500)


if __name__ == "__main__":
    import uvicorn

    print("🚀 Application démarrée sur http://localhost:8000")
    print("📄 Pages disponibles:")
    print("   - / (Home)")
    print("   - /auth/login")
    print("   - /auth/register")
    print("   - /dashboard")
    print("   - /projects")
    print("   - /kanban")
    print("   - /settings")
    print("   - /about")
    uvicorn.run(app, host="0.0.0.0", port=8000)
