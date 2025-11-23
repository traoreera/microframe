"""
Layouts complets pour tous les cas d'usage
"""

from typing import Dict, List, Optional

from markupsafe import Markup

from .daisy_ui_kit import Alert, Avatar, Badge, Button, Card, DaisyUI, Input, Navbar
from .utils import build_feature_list


class Pricing:
    """Composant Pricing - Affichage des plans tarifaires"""

    @staticmethod
    def pricing_table(
        plans: List[dict],
        featured_plan: Optional[int] = None,
        currency: str = "€",
        period: str = "/mois",
        classes: str = "",
    ) -> Markup:
        """Tableau de pricing avec plusieurs plans"""

        pricing_html = []

        for idx, plan in enumerate(plans):
            is_featured = idx == featured_plan
            featured_class = "ring-2 ring-primary scale-105" if is_featured else ""
            featured_badge = (
                '<div class="badge badge-primary absolute -top-3 -right-3">Populaire</div>'
                if is_featured
                else ""
            )

            # Use utility helper for feature list
            features = plan.get("features", [])
            features_html = build_feature_list(features)

            pricing_html.append(
                f"""
            <div class="relative {featured_class} transition-transform duration-300">
                {featured_badge}
                <div class="card bg-base-100 shadow-xl h-full">
                    <div class="card-body">
                        <h2 class="card-title text-2xl">{plan.get('name', 'Plan')}</h2>
                        
                        <p class="text-base-content/70 text-sm mb-4">
                            {plan.get('description', '')}
                        </p>
                        
                        <div class="my-4">
                            <span class="text-5xl font-bold">{currency}{plan.get('price', '0')}</span>
                            <span class="text-base-content/70 text-sm">{period}</span>
                        </div>
                        
                        <ul class="space-y-3 mb-6 text-sm">
                            {features_html}
                        </ul>
                        
                        <div class="card-actions">
                            <button class="btn btn-{'primary' if is_featured else 'outline'} btn-block">
                                {plan.get('cta_text', 'Choisir ce plan')}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            """
            )

        return Markup(
            f"""
        <div class="grid grid-cols-1 md:grid-cols-{len(plans)} gap-6 {classes}">
            {''.join(pricing_html)}
        </div>
        """
        )

    @staticmethod
    def pricing_comparison(plans: List[dict], features: List[dict], classes: str = "") -> Markup:
        """Tableau de comparaison détaillé des plans"""

        # En-tête avec les plans
        plans_header = "\n".join(
            [f'<th class="text-center font-bold">{plan.get("name", "Plan")}</th>' for plan in plans]
        )

        # Lignes de comparaisonplan_features
        features_html = ""
        for feature in features:
            feature_name = feature.get("name", "")
            cells = []

            for plan in plans:
                plan_features = plan.get("features", [])

                for plan_feature in plan_features:

                    cells.append(f'<td class="text-center">{plan_feature}</td>')

            features_html += f"""
            <tr>
                <td class="font-semibold text-left">{feature_name}</td>
                {''.join(cells)}
            </tr>
            """

        return Markup(
            f"""
        <div class="overflow-x-auto {classes}">
            <table class="table table-zebra w-full">
                <thead>
                    <tr>
                        <th class="text-left">Fonctionnalités</th>
                        {plans_header}
                    </tr>
                </thead>
                <tbody>
                    {features_html}
                </tbody>
            </table>
        </div>
        """
        )

    @staticmethod
    def simple_pricing_card(
        name: str,
        price: str,
        currency: str = "€",
        period: str = "/mois",
        description: str = "",
        features: List[str] = None,
        cta_text: str = "Choisir ce plan",
        featured: bool = False,
        classes: str = "",
    ) -> Markup:
        """Carte de prix simple"""

        if features is None:
            features = []

        features_html = "\n".join(
            [
                f'<li class="flex items-center gap-2"><span class="text-success">✓</span> {feature}</li>'
                for feature in features
            ]
        )
        featured_class = "ring-2 ring-primary" if featured else ""
        featured_badge = '<div class="badge badge-primary">Populaire</div>' if featured else ""
        return Markup(
            f"""
        <div class="card bg-base-100 shadow-xl {featured_class} {classes}">
            <div class="card-body">
                <div class="flex justify-between items-start mb-2">
                    <h2 class="card-title text-2xl">{name}</h2>
                    {featured_badge}
                </div>
                
                <p class="text-base-content/70 text-sm mb-4">{description}</p>
                
                <div class="my-6 border-y border-base-300 py-4">
                    <div class="text-5xl font-bold">{currency}{price}</div>
                    <div class="text-base-content/70 text-sm">{period}</div>
                </div>
                
                <ul class="space-y-3 mb-6 text-sm">
                    {features_html}
                </ul>
                <button class="btn btn-{'primary' if featured else 'outline'} btn-block" hx-get="{name}">
                    {cta_text}
                </button>
            </div>
        </div>
        """
        )

    @staticmethod
    def pricing_page(
        title: str = "Nos tarifs",
        subtitle: str = "Choisissez le plan qui vous convient",
        plans: List[dict] = None,
        featured_plan: Optional[int] = None,
        show_comparison: bool = True,
        comparison_features: List[dict] = None,
    ) -> Markup:
        """Page complète de pricing"""

        if plans is None:
            plans = [
                {
                    "name": "Starter",
                    "price": "29",
                    "description": "Parfait pour débuter",
                    "features": ["5 projets", "Support email", "1 GB stockage", "Accès API limité"],
                    "cta_text": "Commencer",
                },
                {
                    "name": "Professional",
                    "price": "79",
                    "description": "Pour les professionnels",
                    "features": [
                        "Projets illimités",
                        "Support prioritaire",
                        "100 GB stockage",
                        "API illimitée",
                        "Intégrations avancées",
                    ],
                    "cta_text": "Essayer gratuitement",
                },
                {
                    "name": "Enterprise",
                    "price": "Devis",
                    "description": "Solution sur mesure",
                    "features": [
                        "Tout illimité",
                        "Support 24/7",
                        "Stockage illimité",
                        "SLA garanti",
                        "Compte dédié",
                    ],
                    "cta_text": "Nous contacter",
                },
            ]

        if comparison_features is None:
            comparison_features = [
                {"name": "Projets"},
                {"name": "Stockage"},
                {"name": "Support"},
                {"name": "API"},
                {"name": "Intégrations"},
                {"name": "Sécurité avancée"},
                {"name": "Analytics"},
                {"name": "Webhooks"},
            ]

        pricing_section = Pricing.pricing_table(
            plans=plans, featured_plan=featured_plan or 1, currency="€", period="/mois"
        )

        comparison_section = ""
        if show_comparison:
            comparison_section = f"""
            <section class="mt-20">
                <h2 class="text-3xl font-bold text-center mb-12">Comparaison détaillée</h2>
                {Pricing.pricing_comparison(plans=plans, features=comparison_features)}
            </section>
            """

        faq_section = f"""
        <section class="mt-20">
            <h2 class="text-3xl font-bold text-center mb-12">Questions fréquentes</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="card bg-base-100 shadow">
                    <div class="card-body">
                        <h3 class="card-title text-lg">Puis-je changer de plan ?</h3>
                        <p class="text-sm text-base-content/70">
                            Oui, vous pouvez upgrader ou downgrader votre plan à tout moment. 
                            Les changements sont appliqués au prochain cycle de facturation.
                        </p>
                    </div>
                </div>
                <div class="card bg-base-100 shadow">
                    <div class="card-body">
                        <h3 class="card-title text-lg">Y a-t-il une période d'essai ?</h3>
                        <p class="text-sm text-base-content/70">
                            Oui, tous les plans incluent une période d'essai gratuite de 14 jours 
                            sans besoin de carte bancaire.
                        </p>
                    </div>
                </div>
                <div class="card bg-base-100 shadow">
                    <div class="card-body">
                        <h3 class="card-title text-lg">Puis-je annuler mon abonnement ?</h3>
                        <p class="text-sm text-base-content/70">
                            Vous pouvez annuler votre abonnement à tout moment. Votre accès 
                            continuera jusqu'à la fin du cycle de facturation.
                        </p>
                    </div>
                </div>
                <div class="card bg-base-100 shadow">
                    <div class="card-body">
                        <h3 class="card-title text-lg">Proposez-vous des réductions annuelles ?</h3>
                        <p class="text-sm text-base-content/70">
                            Oui ! Les paiements annuels bénéficient d'une réduction de 20% 
                            sur le prix mensuel.
                        </p>
                    </div>
                </div>
            </div>
        </section>
        """

        return Markup(
            f"""
        <div class="min-h-screen bg-gradient-to-b from-base-100 to-base-200">
            <!-- Hero Section -->
            <section class="pt-20 pb-16 px-4">
                <div class="max-w-4xl mx-auto text-center">
                    <h1 class="text-5xl font-bold mb-4">{title}</h1>
                    <p class="text-xl text-base-content/70 mb-4">{subtitle}</p>
                    <div class="flex justify-center gap-2 mb-12">
                        <button class="btn btn-ghost">Facturation mensuelle</button>
                        <button class="btn btn-ghost">Facturation annuelle (-20%)</button>
                    </div>
                </div>
            </section>
            
            <!-- Pricing Cards -->
            <section class="px-4 pb-20">
                <div class="max-w-6xl mx-auto">
                    {pricing_section}
                </div>
            </section>
            
            {comparison_section}
            
            {faq_section}
            
            <!-- CTA Section -->
            <section class="py-20 px-4 bg-primary text-primary-content">
                <div class="max-w-2xl mx-auto text-center">
                    <h2 class="text-4xl font-bold mb-4">Prêt à commencer ?</h2>
                    <p class="text-lg mb-8 opacity-90">
                        Inscrivez-vous maintenant et obtenez 14 jours d'essai gratuit.
                    </p>
                    <button class="btn btn-lg btn-secondary">
                        Essayer maintenant
                    </button>
                </div>
            </section>
        </div>
        """
        )


class Contact:
    """Composant Contact - Formulaires et pages de contact"""

    @staticmethod
    def contact_form(
        form_action: str = "/contact/send",
        include_subject: bool = True,
        include_phone: bool = True,
        include_company: bool = False,
        success_message: Optional[str] = None,
        error_message: Optional[str] = None,
        classes: str = "",
    ) -> Markup:
        """Formulaire de contact simple"""

        success_html = (
            Alert.render(message=success_message, type="success", dismissible=True)
            if success_message
            else ""
        )

        error_html = (
            Alert.render(message=error_message, type="error", dismissible=True)
            if error_message
            else ""
        )

        phone_field = (
            f"""
        {Input.render(
            name="phone",
            type="tel",
            label="Téléphone",
            placeholder="+33 6 12 34 56 78",
            classes="mb-4"
        )}
        """
            if include_phone
            else ""
        )

        company_field = (
            f"""
        {Input.render(
            name="company",
            type="text",
            label="Entreprise",
            placeholder="Votre entreprise",
            classes="mb-4"
        )}
        """
            if include_company
            else ""
        )

        subject_field = (
            f"""
        {Input.render(
            name="subject",
            type="text",
            label="Sujet",
            placeholder="Décrivez brièvement votre demande",
            required=True,
            classes="mb-4"
        )}
        """
            if include_subject
            else ""
        )

        return Markup(
            f"""
        <div class="card bg-base-100 shadow-xl {classes}">
            <div class="card-body">
                <h2 class="card-title mb-6">Nous contacter</h2>
                
                {success_html}
                {error_html}
                
                <form method="POST" action="{form_action}" class="space-y-4">
                    {Input.render(
            name="full_name",
            type="text",
            label="Nom complet",
            placeholder="Jean Dupont",
            required=True,
            classes="mb-4"
        )}
                    
                    {Input.render(
            name="email",
            type="email",
            label="Email",
            placeholder="votre@email.com",
            required=True,
            classes="mb-4"
        )}
                    
                    {phone_field}
                    {company_field}
                    {subject_field}
                    
                    <div class="form-control mb-6">
                        <label class="label">
                            <span class="label-text">Message</span>
                        </label>
                        <textarea 
                            class="textarea textarea-bordered" 
                            name="message" 
                            rows="5" 
                            placeholder="Votre message..."
                            required></textarea>
                    </div>
                    
                    {Button.render(
            text="Envoyer le message",
            variant="primary",
            block=True
        )}
                </form>
            </div>
        </div>
        """
        )

    @staticmethod
    def contact_info_card(
        title: str = "Informations de contact",
        phone: Optional[str] = None,
        email: Optional[str] = None,
        address: Optional[str] = None,
        hours: Optional[str] = None,
        social_links: Optional[dict] = None,
        classes: str = "",
    ) -> Markup:
        """Carte d'informations de contact"""

        contact_items = []

        if phone:
            contact_items.append(
                f"""
            <div class="flex items-start gap-4 pb-4 border-b border-base-300 last:border-b-0">
                <div class="text-2xl">📞</div>
                <div>
                    <p class="font-semibold">Téléphone</p>
                    <a href="tel:{phone}" class="text-primary hover:underline">{phone}</a>
                </div>
            </div>
            """
            )

        if email:
            contact_items.append(
                f"""
            <div class="flex items-start gap-4 pb-4 border-b border-base-300 last:border-b-0">
                <div class="text-2xl">📧</div>
                <div>
                    <p class="font-semibold">Email</p>
                    <a href="mailto:{email}" class="text-primary hover:underline">{email}</a>
                </div>
            </div>
            """
            )

        if address:
            contact_items.append(
                f"""
            <div class="flex items-start gap-4 pb-4 border-b border-base-300 last:border-b-0">
                <div class="text-2xl">📍</div>
                <div>
                    <p class="font-semibold">Adresse</p>
                    <p class="text-base-content/70">{address}</p>
                </div>
            </div>
            """
            )

        if hours:
            contact_items.append(
                f"""
            <div class="flex items-start gap-4 pb-4 border-b border-base-300 last:border-b-0">
                <div class="text-2xl">🕐</div>
                <div>
                    <p class="font-semibold">Horaires</p>
                    <p class="text-base-content/70">{hours}</p>
                </div>
            </div>
            """
            )

        social_html = ""
        if social_links:
            social_buttons = []
            for platform, url in social_links.items():
                icons = {
                    "facebook": '<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M9 8h-3v4h3v12h5v-12h3.642l.358-4h-4v-1.667c0-.955.192-1.333 1.115-1.333H16V2.169c-.585-.089-1.308-.169-2.227-.169-2.753 0-4.772 1.679-4.772 4.574V8z"/></svg>',
                    "twitter": '<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M23 3a10.9 10.9 0 01-3.14 1.53 4.48 4.48 0 00-7.86 3v1A10.66 10.66 0 013 4s-4 9 5 13a11.64 11.64 0 01-7 2s9 5 20 5a9.5 9.5 0 00-9-5.5c4.75 2.25 7-7 7-7" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>',
                    "linkedin": '<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M16 8a6 6 0 016 6v7h-4v-7a2 2 0 00-2-2 2 2 0 00-2 2v7h-4v-7a6 6 0 016-6zM2 9h4v12H2z"/><circle cx="4" cy="4" r="2"/></svg>',
                    "github": '<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path fill-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.49.5.092.682-.217.682-.482 0-.237-.008-.868-.013-1.703-2.782.603-3.369-1.343-3.369-1.343-.454-1.156-1.11-1.463-1.11-1.463-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.544 2.914 1.19.092-.926.35-1.545.636-1.9-2.22-.253-4.555-1.11-4.555-4.943 0-1.091.39-1.984 1.029-2.683-.103-.253-.446-1.27.098-2.647 0 0 .84-.269 2.75 1.025A9.578 9.578 0 0112 6.846c.85.004 1.705.114 2.504.336 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.203 2.398.1 2.651.64.699 1.028 1.592 1.028 2.683 0 3.842-2.339 4.687-4.566 4.935.359.309.678.919.678 1.852 0 1.336-.012 2.415-.012 2.743 0 .267.18.578.688.48C19.137 20.191 22 16.432 22 12.017 22 6.484 17.522 2 12 2z" fill-rule="evenodd"/></svg>',
                    "instagram": '<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><rect x="2" y="2" width="20" height="20" rx="5" ry="5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M16 11.37A4 4 0 1112.63 8 4 4 0 0116 11.37z" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="17.5" cy="6.5" r="1.5" fill="currentColor"/></svg>',
                }

                icon = icons.get(platform, "🔗")
                social_buttons.append(
                    f"""
                <a href="{url}" target="_blank" rel="noopener noreferrer" 
                   class="btn btn-circle btn-sm btn-ghost" title="{platform.capitalize()}">
                    {icon}
                </a>
                """
                )

            social_html = f"""
            <div class="mt-6 pt-6 border-t border-base-300">
                <p class="font-semibold mb-4">Suivez-nous</p>
                <div class="flex gap-2">
                    {''.join(social_buttons)}
                </div>
            </div>
            """

        return Markup(
            f"""
        <div class="card bg-base-100 shadow-xl {classes}">
            <div class="card-body">
                <h2 class="card-title mb-6">{title}</h2>
                
                <div class="space-y-4">
                    {''.join(contact_items)}
                </div>
                
                {social_html}
            </div>
        </div>
        """
        )

    @staticmethod
    def contact_page(
        title: str = "Nous contacter",
        subtitle: str = "Nous aimerions avoir de vos nouvelles. Envoyez-nous un message !",
        show_map: bool = True,
        locations: Optional[List[dict]] = None,
        social_links: Optional[Dict] = None,
        faq: Optional[List[dict]] = None,
        direct_contact: Optional[Dict] = {},
    ) -> Markup:
        """Page complète de contact"""

        if locations is None:
            locations = [
                {
                    "name": "Siège social",
                    "phone": "+33 1 23 45 67 89",
                    "email": "contact@example.com",
                    "address": "123 Avenue des Champs, 75000 Paris, France",
                    "hours": "Lun-Ven: 9h-18h",
                },
                {
                    "name": "Bureau Londres",
                    "phone": "+44 20 7123 4567",
                    "email": "london@example.com",
                    "address": "456 Oxford Street, London W1D 1BS, UK",
                    "hours": "Lun-Ven: 9h-17h",
                },
            ]

        if social_links is None:
            social_links = {
                "facebook": "https://www.facebook.com/",
                "twitter": "https://twitter.com/",
                "linkedin": "https://www.linkedin.com/",
                "instagram": "https://www.instagram.com/",
                "youtube": "https://www.youtube.com/",
            }

        locations_html = "\n".join(
            [
                Contact.contact_info_card(
                    title=loc.get("name", "Bureau"),
                    phone=loc.get("phone"),
                    email=loc.get("email"),
                    address=loc.get("address"),
                    hours=loc.get("hours"),
                    social_links=loc.get("social_links"),
                )
                for loc in locations
            ]
        )

        map_section = ""
        if show_map:
            map_section = (
                """
            <section class="mt-20" id ="map">
                <h2 class="text-3xl font-bold text-center mb-12">Localisation</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                """
                + locations_html
                + """
                </div>
            </section>
            """
            )

        if faq is None:
            faq = [
                {
                    "question": "Comment puis-je vous contacter ?",
                    "answer": "Nous vous invitons à nous contacter par email ou par téléphone.",
                },
                {
                    "question": "Quelles sont vos heures d'ouverture ?",
                    "answer": "Nous sommes ouverts du lundi au vendredi de 9h00 à 18h00.",
                },
            ]

        html_faq = ""
        for faq_item in faq:
            html_faq += """
            <div class="card bg-base-100 shadow">
                <div class="card-body">
                    <h3 class="card-title text-lg">{}</h3>
                    <p class="text-sm text-base-content/70">{}</p>
                </div>
            </div>
            """.format(
                faq_item.get("question"), faq_item.get("answer")
            )

        faq_section = f"""
        <section class="mt-20" id="faq">
            <h2 class="text-3xl font-bold text-center mb-12">Faq</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                {html_faq}
            </div>
        </section>
        """
        return Markup(
            f"""
        <div class="min-h-screen bg-gradient-to-b from-base-100 to-base-200">
            <!-- Hero Section -->
            <section class="py-20 px-4 text-center">
                <div class="max-w-2xl mx-auto">
                    <h1 class="text-5xl font-bold mb-4">{title}</h1>
                    <p class="text-xl text-base-content/70">{subtitle}</p>
                </div>
            </section>
            
            <!-- Contact Form & Info -->
            <section class="px-4 pb-20">
                <div class="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-8">
                    {Contact.contact_form()}
                    
                    <div class="space-y-6">
                        {Contact.contact_info_card(
            title=direct_contact.get(
                "title", "Call To action"),  # "call to action",
            # "+33 1 23 45 67 89",
            phone=direct_contact.get("phone", "+33 1 23 45 67 89"),
            # "contact@example.com",
            email=direct_contact.get("email", "contact@example.com"),
            # "123 Avenue des Champs, 75000 Paris, France",
            address=direct_contact.get(
                "address", "123 Avenue des Champs, 75000 Paris, France"),
            # "Lun-Ven: 9h-18h<br/>Sam-Dim: Fermé",
            hours=direct_contact.get(
                "hours", "Lun-Ven: 9h-18h<br/>Sam-Dim: Fermé"),
            social_links=social_links
        )}
                    </div>
                </div>
            </section>
            
            {map_section if show_map else ""}
            
            {faq_section}
        </div>
        """
        )

    @staticmethod
    def contact_modal(
        modal_id: str = "contact-modal", form_action: str = "/contact/send"
    ) -> Markup:
        """Modal de contact"""

        return Markup(
            f"""
        <dialog id="{modal_id}" class="modal">
            <div class="modal-box w-full max-w-md">
                <h3 class="font-bold text-lg mb-6">Nous contacter</h3>
                
                <form method="dialog">
                    <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">✕</button>
                </form>
                
                <form method="POST" action="{form_action}" class="space-y-4">
                    <div class="form-control">
                        <label class="label">
                            <span class="label-text">Nom</span>
                        </label>
                        <input type="text" name="full_name" placeholder="Votre nom" 
                               class="input input-bordered" required />
                    </div>
                    
                    <div class="form-control">
                        <label class="label">
                            <span class="label-text">Email</span>
                        </label>
                        <input type="email" name="email" placeholder="votre@email.com" 
                               class="input input-bordered" required />
                    </div>
                    
                    <div class="form-control">
                        <label class="label">
                            <span class="label-text">Message</span>
                        </label>
                        <textarea name="message" placeholder="Votre message..." 
                                  class="textarea textarea-bordered" rows="4" required></textarea>
                    </div>
                    
                    <div class="modal-action">
                        <button type="button" class="btn" onclick="{modal_id}.close()">
                            Annuler
                        </button>
                        <button type="submit" class="btn btn-primary">
                            Envoyer
                        </button>
                    </div>
                </form>
            </div>
            
            <form method="dialog" class="modal-backdrop">
                <button>close</button>
            </form>
        </dialog>
        """
        )
