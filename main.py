from starlette.responses import HTMLResponse, RedirectResponse

from microframe import AppConfig, Application, Request, Router, Depends
from microframe.ui import TemplateEngine
from microframe.ui.cookies import CookieResponse, get_cookie_response

from authx import create_access_token, create_refresh_token, AuthConfig, decode_token


from microui import ( Alert, Button, Modal, ThemeManager, register_components, setup_daisy_ui,)
from microui.auth_pages import AuthPages
from microui.layout import DashBordLayout, LandingPage, KanbanLayout, EcommerceLayout, Pricing

appConf = AppConfig(title="DaisyUI Kit", version="0.0.1", debug=True)

app = Application(configuration=appConf)
router = Router(tags=["Demo UI"])
auth_router = Router("/auth", tags=["Auth"])


auth_page = AuthPages()

auth_configure = AuthConfig(secret_key="mysecretkey", algorithm="HS256", access_token_expire_minutes=30, refresh_token_expire_days=7)


# 1️⃣ Initialiser DaisyUI + Routes Thèmes
setup_daisy_ui(app=app, router=router)


# 2️⃣ Créer un composant Modal réutilisable
modal_html = Modal.render(
    id="my_modal",
    title="Confirmation",
    content="<p>Êtes-vous sûr de vouloir continuer ?</p>",
    actions=f"""
        {Button.render("Annuler", variant="ghost", onclick="my_modal.close()")}
        {Button.render("Confirmer", variant="primary", onclick="my_modal.close()")}
    """,
)


# 3️⃣ Inject UI components au state global
app.state.ui = register_components()
app.state.modal_html = modal_html


# 4️⃣ Init moteur de templates
template = TemplateEngine(cache=False, debug=True).instance()


@auth_router.get("/login")
async def auth_login(request: Request, curent_user:CookieResponse=Depends(get_cookie_response)):

    cookise = curent_user.cookies_response(request)

    if user_id := cookise.get("token_refrech"):
        return RedirectResponse("/", status_code=303)
    

    return await template.render(
        "pages/login.html",
        {"title": "Connexion", "content": auth_page.login_page(form_action="/auth/login")},
        request,
    )


@auth_router.post("/login")
async def auth_login_submit(request: Request, cookies:CookieResponse=Depends(get_cookie_response)):
    form_data = await request.form()
    user = form_data.get("email")
    password = form_data.get("password")
    remember = form_data.get("remember")
    
    
    if user == "traoreera@gmail.com" and password == "123456":
        
        redirec_script = """
        <script>
            window.location.href = "/Econ";
        </script>
        """
        response = HTMLResponse(content=redirec_script, status_code=200)


        access_token = create_access_token(user, auth_configure)
        refresh_token = create_refresh_token(user, auth_configure)
        response.set_cookie(
            key="token_refrech",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=auth_configure.refresh_token_expire_days * 24 * 60 * 60,
        )
        return response

    
    return HTMLResponse(content=Alert.render("Invalid credentials", type="error"))
    


@auth_router.get("/register")
async def register(request: Request):
    return await template.render(
        "pages/register.html",
        {"title": "Inscription", "content": auth_page.register_page(form_action="/auth/register")},
        request,
    )


@auth_router.get("/forgot-password")
async def forgot_password(request: Request):
    return await template.render(
        "pages/forgot-password.html",
        {
            "title": "Mot de passe oublié",
            "content": auth_page.forgot_password_page(form_action="/auth/forgot-password"),
        },
        request,
    )


@auth_router.post("/forgot-password")
async def forgot_password_submit(request: Request):
    form_data = await request.form()
    email = form_data.get("email")
    return (
        RedirectResponse("/forgot-password", status_code=303)
        if email != "traoreera@gmail.com"
        else RedirectResponse("/auth/login", status_code=303)
    )


@router.get("/apptest")
async def apptest(request: Request):

    return await template.render(
        "pages/apptest.html",
        {
            "content": DashBordLayout.render(
                title="Dashboard",
                sidebar_items=[
                    {"text": "Dashboard", "href": "/dashboard", "icon": "📊", "active": True},
                    {"text": "Projets", "href": "/projects", "icon": "📁"},
                    {"text": "Équipe", "href": "/team", "icon": "👥"},
                    {"text": "Paramètres", "href": "/settings", "icon": "⚙️"},
                ],
                content="",
                theme=ThemeManager.get_theme(request),
                user_name="Traore",
                avatar="https://placeimg.com/192/192/people",
            )
        },
        request,
    )


@app.get("/")
async def langing(request: Request):

    return await template.render(
        "pages/apptest.html",
        {
            "content": LandingPage.render(
                title="DaisyUI Kit",
                hero_title="DaisyUI Kit",
                hero_subtitle="DaisyUI Kit",
                theme=ThemeManager.get_theme(request),cta_link="/auth/register  ",
            )
        },
        request,
    )


@router.get("/kanban")
async def apptest(request: Request):

    return await template.render(
        "pages/apptest.html",
        {
            "content": KanbanLayout.render(title="Kanban", 
            columns=[
                {
                    "title": "To Do", 
                    "tasks": [
                        {"title": "Task 1", "description": "Description for all and more custom templatings", "assignee_avatar": "https://picsum.photos/400/300?random=1", "priority": "warning"},
                        {"title": "Task 2", "description": "Description for all and more custom templatings", "assignee_avatar": "https://picsum.photos/400/300?random=2"},
                        {"title": "Task 3", "description": "Description for all and more custom templatings", "assignee_avatar": "https://picsum.photos/400/300?random=1", "priority": "error"},
                        {"title": "Task 4", "description": "Description for all and more custom templatings", "assignee_avatar": "https://picsum.photos/400/300?random=2"},
                        {"title": "Task 5", "description": "Description for all and more custom templatings", "assignee_avatar": "https://picsum.photos/400/300?random=1", "priority": "accent"},
                        {"title": "Task 6", "description": "Description for all and more custom templatings", "assignee_avatar": "https://picsum.photos/400/300?random=2"},
                        {"title": "Task 7", "description": "Description for all and more custom templatings", "assignee_avatar": "https://picsum.photos/400/300?random=1", "priority": "info"},
                        {"title": "Task 8", "description": "Description for all and more custom templatings", "assignee_avatar": "https://picsum.photos/400/300?random=2"},
                        {"title": "Task 9", "description": "Description for all and more custom templatings", "assignee_avatar": "https://picsum.photos/400/300?random=1", "priority": "warning"},
                        {"title": "Task 10", "description": "Description 2", "assignee_avatar": "https://picsum.photos/400/300?random=2"},

                ]
            },
            ],)
        },
        request,
    )




@app.get("/Econ")
async def langing(request: Request, cookies:CookieResponse = Depends(get_cookie_response)):
    cookie = cookies.cookies_response(request)
    if user:=cookie.get("token_refrech", None):
        data = decode_token(user, auth_configure,"refresh")
        username = data.get("sub", None)
        if username:username = username.split("@")[0]

    return await template.render(
        "pages/apptest.html",
        {
            "title": username if username else "Ecommerce",
            "content": EcommerceLayout.ecommerce_layout,
            "username": username if username else None,
            "ecom_layout":f""" 
                <h1 class="text-3xl font-bold">{username}</h1>
                <p class="text-lg">DaisyUI Kit</p>
                {Pricing.pricing_table(
                    plans=[
                        {"name": "Starter", "price": "29", "description": "Parfait pour débuter", "features": ["5 projets", "Support email", "1 GB stockage", "Accès API limité"]},
                        {"name": "Professional", "price": "79", "description": "Pour les professionnels", "features": ["20 projets", "Support email", "2 GB stockage", "Accès API limité"]},
                        {"name": "Business", "price": "149", "description": "Pour les entreprises", "features": ["50 projets", "Support email", "5 GB stockage", "Accès API limité"]},
                        {"name": "Enterprise", "price": "249", "description": "Pour les grandes entreprises", "features": ["100 projets", "Support email", "10 GB stockage", "Accès API limité"]},
                        {"name": "Free", "price": "0", "description": "Pour debute", "features": ["1 projets", "10 GB stockage", "Accès API limité"]},
                    ]
                )}
            """
        },
        request,
    )



# 5️⃣ Register router
app.include_router(router)
app.include_router(auth_router)
