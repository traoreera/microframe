"""
Full page layouts: Dashboard, Landing, Kanban, Ecommerce
"""
from typing import Dict, List, Optional

from markupsafe import Markup
from .daisy_ui_kit import Avatar, Card, DaisyUI, Alert, Input, Button, Badge, Navbar
from .layout import Pricing, Contact
from .utils import build_menu_items


class DashBordLayout:
    """Dashboard layout with sidebar navigation"""
    
    def __init__(self,):
        pass

    @staticmethod
    def render(
        title: str,
        sidebar_items: List[Dict],
        content: Markup,
        notifications_count: int = 0,
        theme: str = "light",
        avatar: str = "",
        user_name: str = ""
    ) -> Markup:
        """Render complete dashboard layout"""
        if not sidebar_items:
            sidebar_items = [
                {"text": "Dashboard", "href": "/dashboard", "icon": "📊", "active": True},
                {"text": "Projets", "href": "/projects", "icon": "📁"},
                {"text": "Équipe", "href": "/team", "icon": "👥"},
                {"text": "Paramètres", "href": "/settings", "icon": "⚙️"},
            ]

        # Use utility helper for menu
        sidebar_menu = build_menu_items(sidebar_items)

        user_avatar = avatar if avatar else "https://placeimg.com/192/192/people"
        avatar_component = Avatar.render(
            src=user_avatar,
            size="sm",
            shape="circle",
            online=True,
            placeholder=user_name[0] if user_name else "U"
        )

        return Markup(
            f"""
            <div class="drawer lg:drawer-open">
                <input id="sidebar-drawer" type="checkbox" class="drawer-toggle" />
                <!-- Main Content -->
                <div class="drawer-content flex flex-col">
                    <!-- Navbar -->
                    <div class="navbar bg-base-100 border-b border-base-300">
                        <div class="flex-none lg:hidden">
                            <label for="sidebar-drawer" class="btn btn-square btn-ghost">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="inline-block w-6 h-6 stroke-current">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
                                </svg>
                            </label>
                        </div>
                        
                        <div class="flex-1">
                            <h1 class="text-xl font-bold px-4">{title}</h1>
                        </div>
                        
                        <div class="flex-none gap-2">
                            <!-- Notifications -->
                            <button class="btn btn-ghost btn-circle">
                                <div class="indicator">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                                    </svg>
                                    {f'<span class="badge badge-xs badge-primary indicator-item">{notifications_count}</span>' if notifications_count > 0 else ''}
                                </div>
                            </button>
                            
                            <!-- Theme Switcher -->
                            {DaisyUI.theme_switcher(theme)}
                            
                            <!-- User Menu -->
                            <div class="dropdown dropdown-end">
                                <div tabindex="0" role="button" class="btn btn-ghost btn-circle avatar">
                                    <div class="w-10 rounded-full">
                                        {avatar_component}
                                    </div>
                                </div>
                                <ul tabindex="0" class="mt-3 z-[1] p-2 shadow menu menu-sm dropdown-content bg-base-100 rounded-box w-52">
                                    <li class="menu-title">{user_name}</li>
                                    <li><a href="/profile">👤 Profil</a></li>
                                    <li><a href="/settings">⚙️ Paramètres</a></li>
                                    <li><hr class="my-2" /></li>
                                    <li><a href="/auth/logout">🚪 Déconnexion</a></li>
                                </ul>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Page Content -->
                    <div id="main-content" class="p-4 lg:p-8">
                        {content}
                    </div>
                </div>
                
                <!-- Sidebar -->
                <div class="drawer-side z-40">
                    <label for="sidebar-drawer" class="drawer-overlay"></label>
                    <aside class="menu w-64 min-h-screen bg-base-200 text-base-content">
                        <div class="p-4">
                            <h1 class="text-2xl font-bold">🎨 MonApp</h1>
                        </div>
                        <ul class="p-4 space-y-2">
                            {sidebar_menu}
                        </ul>
                        
                        <div class="mt-auto p-4 border-t border-base-300">
                            <div class="text-xs text-gray-500">Version 1.0.0</div>
                        </div>
                    </aside>
                </div>
            </div>
"""
        )


class LandingPage:
    """Landing page layout with hero, features, pricing, contact"""
    
    def __init__(self) -> None:
        pass

    @staticmethod
    def render(
        title: str,
        hero_title: str,
        hero_subtitle: str,
        cta_text: str = "Commencer",
        cta_link: str = "/register",
        features: List[Dict] = None,
        pricing: List[Dict] = None,
        locations: List[Dict] = None,
        theme: str = "dark",
        nav_links: list = ["features", "pricing", "contact", "faq"],
    ) -> Markup:
        """Render complete landing page"""
        
        if not features:
            features = [
                {"icon": "⚡", "title": "Rapide", "desc": "Performance optimale", "image": "https://picsum.photos/400/300?random=1"},
                {"icon": "🎨", "title": "Moderne", "desc": "Design élégant", "image": "https://picsum.photos/400/300?random=2"},
                {"icon": "🔒", "title": "Sécurisé", "desc": "Données protégées", "image": "https://picsum.photos/400/300?random=3"},
            ]
        
        if not pricing:
            pricing = [
                {"name": "Free", "price": 0, "currency": "€", "cta_text": "Commencer", "features": ["5 projets", "Email support", "1GB storage"], "description": "Gratuit pour chaque utilisation", "featured": False},
                {"name": "Starter", "price": 10, "currency": "€", "cta_text": "Commencer", "features": ["10 projets", "Priority support", "10GB storage"], "description": "Pour les équipes", "featured": True},
                {"name": "Premium", "price": 20, "currency": "€", "cta_text": "Commencer", "features": ["Illimité", "24/7 support", "100GB storage"], "description": "Pour les entreprises", "featured": False}
            ]
        
        if not locations:
            locations = [
                {"name": "Bureau Principal", "phone": "+226 67 90 58 25", "email": "contact@example.com", "address": "123 Rue, Ville", "hours": "Lun-Ven: 9h-18h"}
            ]

        # Build feature cards
        feature_html = "".join([
            Card.render(
                title=f.get("title", ""),
                body=f'<div class="text-center"><div class="text-4xl mb-4">{f["icon"]}</div><p>{f["desc"]}</p></div>',
                image=f.get("image"),
                bordered=True
            )
            for f in features
        ])
        
        # Build pricing cards
        price_html = "".join([
            Pricing.simple_pricing_card(**p)
            for p in pricing
        ])

        return Markup(f"""
            <div class="navbar bg-base-100 sticky top-0 z-50 border-b border-base-300">
                <div class="navbar-start">
                    <a class="btn btn-ghost text-xl">🚀 {title}</a>
                </div>
                <div class="navbar-center hidden lg:flex">
                    <ul class="menu menu-horizontal px-1">
                        {" ".join([f'<li><a href="#{link}">{link}</a></li>' for link in nav_links])}
                    </ul>
                </div>
                <div class="navbar-end gap-2">
                    {DaisyUI.theme_switcher(theme)}
                    <a href="/auth/login" class="btn btn-ghost">Login</a>
                    <a href="/auth/register" class="btn btn-primary">Register</a>
                </div>
            </div>
            
            <!-- Hero -->
            <div class="hero min-h-screen bg-gradient-to-br from-primary/20 to-secondary/20">
                <div class="hero-content text-center">
                    <div class="max-w-2xl">
                        <h1 class="text-6xl font-bold mb-4">{hero_title}</h1>
                        <p class="text-xl mb-8">{hero_subtitle}</p>
                        <a href="{cta_link}" class="btn btn-primary btn-lg">{cta_text}</a>
                    </div>
                </div>
            </div>
            
            <!-- Features -->
            <section id="features" class="py-20 px-4 bg-base-200">
                <div class="container mx-auto">
                    <h2 class="text-4xl font-bold text-center mb-12">Features</h2>
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                        {feature_html}
                    </div>
                </div>
            </section>
            
            <!-- Pricing -->
            <section id="pricing" class="py-20 px-4">
                <div class="container mx-auto">
                    <h2 class="text-4xl font-bold text-center mb-12">Pricing</h2>
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                        {price_html}
                    </div>
                </div>
            </section>
            
            <!-- Contact -->
            <section id="contact" class="py-20 px-4 bg-base-200">
                <div class="container mx-auto">
                    {Contact.contact_page(title="Contact Us", locations=locations)}
                </div>
            </section>
            
            <!-- Footer -->
            <footer class="footer footer-center p-10 bg-base-300 text-base-content">
                <div>
                    <p class="font-bold">{title}</p>
                    <p>© 2024 - All rights reserved</p>
                </div>
            </footer>
        """)


class KanbanLayout:
    """Kanban board layout"""
    
    @staticmethod
    def render(
        title: str,
        columns: List[Dict],
        theme: str = "dark"
    ) -> Markup:
        """Layout Kanban board"""
        
        kanban_columns = []
        for column in columns:
            cards = []
            for task in column.get('tasks', []):
                cards.append(Card.render(
                    title=task.get('title', ''),
                    body=f"""
                        <p class="text-sm">{task.get('description', '')}</p>
                        <div class="flex gap-2 mt-2 items-center">
                            {Badge.render(task.get('priority', 'Normal'), variant=task.get('priority_variant', 'neutral'), size="sm")}
                            {Avatar.render(task.get('assignee_avatar', ''), size="xs", shape="circle") if task.get('assignee_avatar') else ''}
                        </div>
                    """,
                    compact=True,
                    bordered=True,
                    classes="mb-2 cursor-move hover:shadow-lg transition-shadow"
                ))
            
            kanban_columns.append(f"""
            <div class="flex-1 min-w-80">
                <div class="card bg-base-200">
                    <div class="card-body">
                        <div class="flex justify-between items-center mb-4">
                            <h3 class="card-title">{column.get('title', '')} ({len(column.get('tasks', []))})</h3>
                            {Button.render("+", variant="ghost", size="sm")}
                        </div>
                        <div class="space-y-2">
                            {''.join(cards)}
                        </div>
                    </div>
                </div>
            </div>
            """)
        
        content = f"""
        <div class="flex gap-4 overflow-x-auto pb-4">
            {''.join(kanban_columns)}
        </div>
        """
        
        return DashBordLayout.render(
            title=title,
            user_name="User",
            content=Markup(content),
            theme=theme,
            sidebar_items=[
                {"text": "Board", "href": "/kanban", "icon": "📋", "active": True},
                {"text": "Liste", "href": "/tasks", "icon": "📝"},
                {"text": "Calendrier", "href": "/calendar", "icon": "📅"},
            ]
        )


class EcommerceLayout:
    """E-commerce layout with cart"""
    
    @staticmethod
    def render(
        title: str,
        content: str,
        cart_count: int = 0,
        brand: str = "🛍️ Ma Boutique",
        theme: str = "dark"
    ) -> Markup:
        """Layout e-commerce avec panier"""
        
        navbar = Navbar.render(
            brand=brand,
            items=[
                {"text": "Accueil", "href": "/"},
                {"text": "Produits", "href": "/products"},
                {"text": "Catégories", "href": "/categories"},
                {"text": "Promo", "href": "/promo"},
            ],
            end_items=f"""
                <div class="form-control">
                    <input type="text" placeholder="Rechercher..." class="input input-bordered w-full md:w-auto" />
                </div>
                
                <div class="indicator">
                    <span class="indicator-item badge badge-primary">{cart_count}</span>
                    <button class="btn btn-ghost btn-circle">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                        </svg>
                    </button>
                </div>
                
                {DaisyUI.theme_switcher(theme)}
            """
        )
        
        return Markup(f"""
        {navbar}
        
        <div class="container mx-auto px-4 py-8">
            {content}
        </div>
        
        <footer class="footer p-10 bg-base-200 text-base-content mt-16">
            <div>
                <span class="footer-title">Services</span>
                <a class="link link-hover">Livraison</a>
                <a class="link link-hover">Retours</a>
                <a class="link link-hover">Garantie</a>
            </div>
            <div>
                <span class="footer-title">Entreprise</span>
                <a class="link link-hover">À propos</a>
                <a class="link link-hover">Contact</a>
            </div>
            <div>
                <span class="footer-title">Légal</span>
                <a class="link link-hover">CGV</a>
                <a class="link link-hover">Politique de confidentialité</a>
            </div>
        </footer>
        """)
