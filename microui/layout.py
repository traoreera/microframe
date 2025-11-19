"""
Layouts complets pour tous les cas d'usage
"""
from typing import Dict, List, Optional

from markupsafe import Markup
from .daisy_ui_kit import Avatar, Card, DaisyUI, Alert, Input, Button, Badge, Navbar

class Pricing:
    """Composant Pricing - Affichage des plans tarifaires"""
    
    @staticmethod
    def pricing_table(
        plans: List[dict],
        featured_plan: Optional[int] = None,
        currency: str = "€",
        period: str = "/mois",
        classes: str = ""
    ) -> Markup:
        """Tableau de pricing avec plusieurs plans"""
        
        pricing_html = []
        
        for idx, plan in enumerate(plans):
            is_featured = idx == featured_plan
            featured_class = "ring-2 ring-primary scale-105" if is_featured else ""
            featured_badge = '<div class="badge badge-primary absolute -top-3 -right-3">Populaire</div>' if is_featured else ""
            
            features = plan.get("features", [])
            features_html = "\n".join([
                f'<li class="flex items-center gap-2"><span class="text-success">✓</span> {feature}</li>'
                for feature in features
            ])
            
            pricing_html.append(f"""
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
            """)
        
        return Markup(f"""
        <div class="grid grid-cols-1 md:grid-cols-{len(plans)} gap-6 {classes}">
            {''.join(pricing_html)}
        </div>
        """)
    
    @staticmethod
    def pricing_comparison(
        plans: List[dict],
        features: List[dict],
        classes: str = ""
    ) -> Markup:
        """Tableau de comparaison détaillé des plans"""
        
        # En-tête avec les plans
        plans_header = "\n".join([
            f'<th class="text-center font-bold">{plan.get("name", "Plan")}</th>'
            for plan in plans
        ])
        
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
        
        return Markup(f"""
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
        """)
    
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
        classes: str = ""
    ) -> Markup:
        """Carte de prix simple"""
        
        if features is None:
            features = []
        
        features_html = "\n".join([
            f'<li class="flex items-center gap-2"><span class="text-success">✓</span> {feature}</li>'
            for feature in features
        ])
        featured_class = "ring-2 ring-primary" if featured else ""
        featured_badge = '<div class="badge badge-primary">Populaire</div>' if featured else ""
        return Markup(f"""
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
        """)
    
    @staticmethod
    def pricing_page(
        title: str = "Nos tarifs",
        subtitle: str = "Choisissez le plan qui vous convient",
        plans: List[dict] = None,
        featured_plan: Optional[int] = None,
        show_comparison: bool = True,
        comparison_features: List[dict] = None
    ) -> Markup:
        """Page complète de pricing"""
        
        if plans is None:
            plans = [
                {
                    "name": "Starter",
                    "price": "29",
                    "description": "Parfait pour débuter",
                    "features": [
                        "5 projets",
                        "Support email",
                        "1 GB stockage",
                        "Accès API limité"
                    ],
                    "cta_text": "Commencer"
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
                        "Intégrations avancées"
                    ],
                    "cta_text": "Essayer gratuitement"
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
                        "Compte dédié"
                    ],
                    "cta_text": "Nous contacter"
                }
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
                {"name": "Webhooks"}
            ]
        
        pricing_section = Pricing.pricing_table(
            plans=plans,
            featured_plan=featured_plan or 1,
            currency="€",
            period="/mois"
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
        
        return Markup(f"""
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
        """)

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
        classes: str = ""
    ) -> Markup:
        """Formulaire de contact simple"""
        
        
        
        success_html = Alert.render(
            message=success_message,
            type="success",
            dismissible=True
        ) if success_message else ""
        
        error_html = Alert.render(
            message=error_message,
            type="error",
            dismissible=True
        ) if error_message else ""
        
        phone_field = f"""
        {Input.render(
            name="phone",
            type="tel",
            label="Téléphone",
            placeholder="+33 6 12 34 56 78",
            classes="mb-4"
        )}
        """ if include_phone else ""
        
        company_field = f"""
        {Input.render(
            name="company",
            type="text",
            label="Entreprise",
            placeholder="Votre entreprise",
            classes="mb-4"
        )}
        """ if include_company else ""
        
        subject_field = f"""
        {Input.render(
            name="subject",
            type="text",
            label="Sujet",
            placeholder="Décrivez brièvement votre demande",
            required=True,
            classes="mb-4"
        )}
        """ if include_subject else ""
        
        return Markup(f"""
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
        """)
    
    @staticmethod
    def contact_info_card(
        title: str = "Informations de contact",
        phone: Optional[str] = None,
        email: Optional[str] = None,
        address: Optional[str] = None,
        hours: Optional[str] = None,
        social_links: Optional[dict] = None,
        classes: str = ""
    ) -> Markup:
        """Carte d'informations de contact"""
        
        contact_items = []
        
        if phone:
            contact_items.append(f"""
            <div class="flex items-start gap-4 pb-4 border-b border-base-300 last:border-b-0">
                <div class="text-2xl">📞</div>
                <div>
                    <p class="font-semibold">Téléphone</p>
                    <a href="tel:{phone}" class="text-primary hover:underline">{phone}</a>
                </div>
            </div>
            """)
        
        if email:
            contact_items.append(f"""
            <div class="flex items-start gap-4 pb-4 border-b border-base-300 last:border-b-0">
                <div class="text-2xl">📧</div>
                <div>
                    <p class="font-semibold">Email</p>
                    <a href="mailto:{email}" class="text-primary hover:underline">{email}</a>
                </div>
            </div>
            """)
        
        if address:
            contact_items.append(f"""
            <div class="flex items-start gap-4 pb-4 border-b border-base-300 last:border-b-0">
                <div class="text-2xl">📍</div>
                <div>
                    <p class="font-semibold">Adresse</p>
                    <p class="text-base-content/70">{address}</p>
                </div>
            </div>
            """)
        
        if hours:
            contact_items.append(f"""
            <div class="flex items-start gap-4 pb-4 border-b border-base-300 last:border-b-0">
                <div class="text-2xl">🕐</div>
                <div>
                    <p class="font-semibold">Horaires</p>
                    <p class="text-base-content/70">{hours}</p>
                </div>
            </div>
            """)
        
        social_html = ""
        if social_links:
            social_buttons = []
            for platform, url in social_links.items():
                icons = {
                    "facebook": '<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M9 8h-3v4h3v12h5v-12h3.642l.358-4h-4v-1.667c0-.955.192-1.333 1.115-1.333H16V2.169c-.585-.089-1.308-.169-2.227-.169-2.753 0-4.772 1.679-4.772 4.574V8z"/></svg>',
                    "twitter": '<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M23 3a10.9 10.9 0 01-3.14 1.53 4.48 4.48 0 00-7.86 3v1A10.66 10.66 0 013 4s-4 9 5 13a11.64 11.64 0 01-7 2s9 5 20 5a9.5 9.5 0 00-9-5.5c4.75 2.25 7-7 7-7" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>',
                    "linkedin": '<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M16 8a6 6 0 016 6v7h-4v-7a2 2 0 00-2-2 2 2 0 00-2 2v7h-4v-7a6 6 0 016-6zM2 9h4v12H2z"/><circle cx="4" cy="4" r="2"/></svg>',
                    "github": '<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path fill-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.49.5.092.682-.217.682-.482 0-.237-.008-.868-.013-1.703-2.782.603-3.369-1.343-3.369-1.343-.454-1.156-1.11-1.463-1.11-1.463-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.544 2.914 1.19.092-.926.35-1.545.636-1.9-2.22-.253-4.555-1.11-4.555-4.943 0-1.091.39-1.984 1.029-2.683-.103-.253-.446-1.27.098-2.647 0 0 .84-.269 2.75 1.025A9.578 9.578 0 0112 6.846c.85.004 1.705.114 2.504.336 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.203 2.398.1 2.651.64.699 1.028 1.592 1.028 2.683 0 3.842-2.339 4.687-4.566 4.935.359.309.678.919.678 1.852 0 1.336-.012 2.415-.012 2.743 0 .267.18.578.688.48C19.137 20.191 22 16.432 22 12.017 22 6.484 17.522 2 12 2z" fill-rule="evenodd"/></svg>',
                    "instagram": '<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><rect x="2" y="2" width="20" height="20" rx="5" ry="5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M16 11.37A4 4 0 1112.63 8 4 4 0 0116 11.37z" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="17.5" cy="6.5" r="1.5" fill="currentColor"/></svg>'
                }
                
                icon = icons.get(platform, "🔗")
                social_buttons.append(f'''
                <a href="{url}" target="_blank" rel="noopener noreferrer" 
                   class="btn btn-circle btn-sm btn-ghost" title="{platform.capitalize()}">
                    {icon}
                </a>
                ''')
            
            social_html = f"""
            <div class="mt-6 pt-6 border-t border-base-300">
                <p class="font-semibold mb-4">Suivez-nous</p>
                <div class="flex gap-2">
                    {''.join(social_buttons)}
                </div>
            </div>
            """
        
        return Markup(f"""
        <div class="card bg-base-100 shadow-xl {classes}">
            <div class="card-body">
                <h2 class="card-title mb-6">{title}</h2>
                
                <div class="space-y-4">
                    {''.join(contact_items)}
                </div>
                
                {social_html}
            </div>
        </div>
        """)
    
    @staticmethod
    def contact_page(
        title: str = "Nous contacter",
        subtitle: str = "Nous aimerions avoir de vos nouvelles. Envoyez-nous un message !",
        show_map: bool = True,
        locations: Optional[List[dict]] = None,
        social_links: Optional[Dict] = None,
        faq: Optional[List[dict]] = None,
        direct_contact:Optional[Dict] = {},
    ) -> Markup:
        """Page complète de contact"""
        
        if locations is None:
            locations = [
                {
                    "name": "Siège social",
                    "phone": "+33 1 23 45 67 89",
                    "email": "contact@example.com",
                    "address": "123 Avenue des Champs, 75000 Paris, France",
                    "hours": "Lun-Ven: 9h-18h"
                },
                {
                    "name": "Bureau Londres",
                    "phone": "+44 20 7123 4567",
                    "email": "london@example.com",
                    "address": "456 Oxford Street, London W1D 1BS, UK",
                    "hours": "Lun-Ven: 9h-17h"
                }
            ]
        

        if social_links is None:
            social_links = {
                "facebook": "https://www.facebook.com/",
                "twitter": "https://twitter.com/",
                "linkedin": "https://www.linkedin.com/",
                "instagram": "https://www.instagram.com/",
                "youtube": "https://www.youtube.com/",
            }


        locations_html = "\n".join([
            Contact.contact_info_card(
                title=loc.get("name", "Bureau"),
                phone=loc.get("phone"),
                email=loc.get("email"),
                address=loc.get("address"),
                hours=loc.get("hours"),
                social_links=loc.get("social_links")
            )
            for loc in locations
        ])
        
        map_section = ""
        if show_map:
            map_section = """
            <section class="mt-20" id ="map">
                <h2 class="text-3xl font-bold text-center mb-12">Localisation</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                """ + locations_html + """
                </div>
            </section>
            """
        
        if faq is None:
            faq = [
                {
                    "question": "Comment puis-je vous contacter ?",
                    "answer": "Nous vous invitons à nous contacter par email ou par téléphone."
                },
                {
                    "question": "Quelles sont vos heures d'ouverture ?",
                    "answer": "Nous sommes ouverts du lundi au vendredi de 9h00 à 18h00."
                }
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
            """.format(faq_item.get("question"), faq_item.get("answer"))


        faq_section =f"""
        <section class="mt-20" id="faq">
            <h2 class="text-3xl font-bold text-center mb-12">Faq</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                {html_faq}
            </div>
        </section>
        """
        return Markup(f"""
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
                            title=  direct_contact.get("title", "Call To action"), #"call to action",
                            phone=  direct_contact.get("phone", "+33 1 23 45 67 89"), #"+33 1 23 45 67 89",
                            email=  direct_contact.get("email", "contact@example.com"), #"contact@example.com",
                            address=  direct_contact.get("address", "123 Avenue des Champs, 75000 Paris, France"), #"123 Avenue des Champs, 75000 Paris, France",
                            hours=  direct_contact.get("hours", "Lun-Ven: 9h-18h<br/>Sam-Dim: Fermé"), #"Lun-Ven: 9h-18h<br/>Sam-Dim: Fermé",
                            social_links=social_links
                        )}
                    </div>
                </div>
            </section>
            
            {map_section if show_map else ""}
            
            {faq_section}
        </div>
        """)
    
    @staticmethod
    def contact_modal(
        modal_id: str = "contact-modal",
        form_action: str = "/contact/send"
    ) -> Markup:
        """Modal de contact"""
        
        return Markup(f"""
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
        """)

class DashBordLayout:
    def __init__(self,):
        pass

    @staticmethod
    def __render(
            title: str,
            user_name: str,
            user_avatar: Optional[str] = None,
            sidebar_items: List[Dict] = [],
            content: str = "",
            theme: str = "dark",
            notifications_count: int = 0):
        if sidebar_items is None:
            sidebar_items = [
                {"text": "Dashboard", "href": "/dashboard",
                    "icon": "📊", "active": True},
                {"text": "Projets", "href": "/projects", "icon": "📁"},
                {"text": "Équipe", "href": "/team", "icon": "👥"},
                {"text": "Paramètres", "href": "/settings", "icon": "⚙️"},
            ]

        # Build sidebar menu
        sidebar_menu = ""
        for item in sidebar_items:
            active = "active" if item.get("active", False) else ""
            hx_attrs = ""
            if item.get("hx_get"):
                hx_attrs = f'hx-get="{item["hx_get"]}" hx-target="#main-content" hx-swap="innerHTML"'

            submenu = item.get("submenu", [])
            if submenu:
                submenu_items = "".join([
                    f'<li><a href="{sub.get("href", "#")}">{sub.get("text", "")}</a></li>'
                    for sub in submenu
                ])
                sidebar_menu += f"""
                <li>
                    <details>
                        <summary>{item.get('icon', '')} {item.get('text', '')}</summary>
                        <ul>{submenu_items}</ul>
                    </details>
                </li>
                """
            else:
                sidebar_menu += f"""
                <li>
                    <a href="{item.get('href', '#')}" class="{active}" {hx_attrs}>
                        <span class="text-xl">{item.get('icon', '')}</span>
                        {item.get('text', '')}
                    </a>
                </li>
                """

        if user_avatar:
            avatar = Avatar.render(
                src=user_avatar, size="sm", shape="circle", online=True, placeholder=user_name[0])
        else:
            avatar = Avatar.render(src="https://placeimg.com/192/192/people",
                                shape="square", size="sm", online=True, placeholder=user_name[0])

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
                                        {avatar}
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

    @staticmethod
    def render(
        title: str,
        sidebar_items: Markup,
        content: Markup,
        notifications_count: int = 0,
        theme: str = "light",
        avatar: str = "",
        user_name: str = ""
    ) -> Markup:
        return DashBordLayout.__render(title=title, sidebar_items=sidebar_items, content=content, notifications_count=notifications_count, theme=theme, user_avatar=avatar, user_name=user_name)

class LandingPage:

    def __init__(self) -> None:
        pass

    @staticmethod
    def __render(
        title: str,
        hero_title: str,
        hero_subtitle: str,
        cta_text: str = "Commencer",
        cta_link: str = "/auth/register",
        features: List[Dict] = None,
        theme: str = "dark",
        link:list = ["features","pricing" ,"contact", "map", "faq"],
        locations:List[Dict] = None,
        pricing:List[Dict] = None
    ):
        
        if features is None or len(features) == 0:
            features = [{"icon": "⚡", "title": "Rapide", "desc": "Performance optimale","image": "https://picsum.photos/400/300?random=2"},{"icon": "🎨", "title": "Moderne", "desc": "Design élégant","image": "https://picsum.photos/400/300?random=2"},{"icon": "🔒", "title": "Sécurisé", "desc": "Données protégées","image": "https://picsum.photos/400/300?random=2"},]
        
        price_html = ""
        if pricing is None or len(pricing) == 0:
            pricing = [
                {"name":"Free","price":0,"currency":"USD","cta_text":"Commencer","features":["5 projets","Email supporting","1T0 storage","Accès à l'API limité"],"description":"Gratuit pour chaque utilisation", "featured": False},
                {"name":"Starter","price":10,"currency":"USD","cta_text":"Commencer","features":["10 projets","Email supporting","2T0 storage","Accès à l'API limité"],"description":"Gratuit pour chaque utilisation", "featured": True},
                {"name":"Premium","price":20,"currency":"USD","cta_text":"Commencer","features":["20 projets","Email supporting","3T0 storage","Accès à l'API limité"],"description":"Gratuit pour chaque utilisation", "featured": False}
                ]
        
        if locations is None or len(locations) == 0:
            locations = [
                {
                    "name": "Bureau Burkina",
                    "phone": "+226 67 90 58 25",
                    "email": "contact@tangagroupbf.com",
                    "address": "123 Boulevard de la Paix, Tanga, Burkina",
                    "hours": "Lun-Ven: 9h-18h"
                },
                {
                    "name": "Bureau Cote d'Ivoire",
                    "phone": "+225 67 90 58 25",
                    "email": "contact@tangagroupci.com",
                    "address": "456 Rue de la joie, Abidjan, Cote d'Ivoire",
                    "hours": "Lun-Ven: 9h-17h"
                }
            ]



        for price in pricing:
            price_html += Pricing.simple_pricing_card(
                price=price.get("price", 0),
                description=price.get("description", ""),
                features=price.get("features", []),
                name=price.get("name", ""),
                currency=price.get("currency", "USD"),
                cta_text=price.get("cta_text", "Commencer"),
                featured=price.get("featured", False), 
                classes=price.get("classes", "")
            )


        feature_html = ""
        for feature in features:
            feature_html += Card.render(
                title=feature.get("title", ""),
                body=f"""
                        <div class="text-center">
                            <div class="text-4xl mb-4">{feature['icon']}</div>
                            <h3 class="font-bold text-xl mb-2">{feature['title']}</h3>
                            <p>{feature['desc']}</p>
                        </div>
                    """,
                    image=feature.get("image", ""),
                bordered=True,
            )
        return Markup(f"""
<div class="navbar bg-base-100 sticky top-0 z-50 border-b border-base-300">
                <div class="navbar-start">
                    <a class="btn btn-ghost text-xl">🚀 {title}</a>
                </div>
                <div class="navbar-center hidden lg:flex">
                    <ul class="menu menu-horizontal px-1">
                        {" ".join([f'<li><a href="#{link}">{link}</a></li>' for link in link])}
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
                    <h2 class="text-4xl font-bold text-center mb-12">features</h2>
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                        {feature_html}
                    </div>
                </div>
            </section>
            
            <!-- Pricing -->
            <section id="pricing" class="py-20 px-4 bg-base-200">
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
                        {Contact.contact_page(title="We're here to help", locations=locations,)}
                </div>
            </section>
            
            <!-- Footer -->
            <footer class="footer footer-center p-10 bg-base-300 text-base-content">
                <div>
                    <p class="font-bold">{title}</p>
                    <p>© 2024 - all rights reserved by Tanga-Corp</p>
                </div>
            </footer>
""")



    @staticmethod
    def render(
        title: str,
        hero_title: str,
        hero_subtitle: str,
        cta_text: str = "Commencer",
        cta_link: str = "/register",
        features: List[Dict] = None,
        theme: str = "dark"
    )-> Markup:

        return LandingPage.__render(title=title, hero_title=hero_title, hero_subtitle=hero_subtitle, cta_text=cta_text, cta_link=cta_link, features=features, theme=theme)


class  KanbanLayout:


    @staticmethod
    def __render(
        title: str,
        columns: List[Dict],
        theme: str = "dark"
    ) -> Markup:
        """Layout Kanban board"""
        
        kanban_columns = ""
        for column in columns:
            cards = ""
            for task in column.get('tasks', []):
                cards += Card.render(
                    title=task.get('title', ''),
                    body=f"""
                        <p class="text-sm">{task.get('description', '')}</p>
                        <div class="flex gap-2 mt-2 items-center">
                            {Badge.render(task.get('priority', 'Normal'), variant=task.get('priority', 'gost'), size="sm",)}
                            {Avatar.render(task.get('assignee_avatar', ''), size="xs", shape="circle") if task.get('assignee_avatar') else ''}
                        </div>
                    """,
                    compact=True,
                    bordered=True,
                    classes="mb-2 cursor-move hover:shadow-lg transition-shadow"
                )
            
            kanban_columns += f"""
            <div class="flex-1 min-w-80">
                <div class="card bg-base-200">
                    <div class="card-body">
                        <div class="flex justify-between items-center mb-4">
                            <h3 class="card-title">{column.get('title', '')} ({len(column.get('tasks', []))})</h3>
                            {Button.render("+", variant="ghost", size="sm")}
                        </div>
                        <div class="space-y-2">
                            {cards}
                        </div>
                    </div>
                </div>
            </div>
            """
        
        content = f"""
        <div class="flex gap-4 overflow-x-auto pb-4">
            {kanban_columns}
        </div>
        """
        
        return DashBordLayout.render(
            title=title,
            user_name="User",
            content=content,
            theme=theme,
            sidebar_items=[
                {"text": "Board", "href": "/kanban", "icon": "📋", "active": True},
                {"text": "Liste", "href": "/tasks", "icon": "📝"},
                {"text": "Calendrier", "href": "/calendar", "icon": "📅"},
            ]
        )



    @staticmethod
    def render(
        title: str,
        columns: List[Dict],
        theme: str = "dark"
    )-> Markup:

        return KanbanLayout.__render(title=title, columns=columns, theme=theme)


class EcommerceLayout:

    @staticmethod
    def ecommerce_layout(
        title: str,
        content: str,
        cart_count: int = 0,brand:str="🛍️ ma Boutique",
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
        <!DOCTYPE html>
        <html lang="fr" data-theme="{theme}">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title>
            <link href="https://cdn.jsdelivr.net/npm/daisyui@4.12.14/dist/full.min.css" rel="stylesheet" />
            <script src="https://cdn.tailwindcss.com"></script>
            <script src="https://unpkg.com/htmx.org@2.0.3"></script>
        </head>
        <body>
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
                    <a class="link link-hover">Emplois</a>
                </div>
                <div>
                    <span class="footer-title">Légal</span>
                    <a class="link link-hover">CGV</a>
                    <a class="link link-hover">Politique de confidentialité</a>
                    <a class="link link-hover">Cookies</a>
                </div>
            </footer>
        </body>
        </html>
        """)



    def __init__(self,):pass


    @staticmethod
    def __render(
        user: Dict,
        content: str,
    ) -> Markup:
        """Layout profil utilisateur"""
        from microui.daisy_ui_kit import Avatar, Badge, Button, Divider
        
        cover_image = user.get('cover', 'https://picsum.photos/1200/300')
        
        profile_header = f"""
        <div class="relative mb-8">
            <img src="{cover_image}" alt="Cover" class="w-full h-64 object-cover rounded-lg" />
            
            <div class="absolute -bottom-16 left-8">
                {Avatar.render(
                    src=user.get('avatar', ''),
                    size="xl",
                    shape="circle",
                    classes="ring ring-base-100 ring-offset-base-100 ring-offset-2"
                )}
            </div>
        </div>
        
        <div class="ml-8 mt-20 mb-8">
            <div class="flex justify-between items-start flex-wrap gap-4">
                <div>
                    <h1 class="text-3xl font-bold">{user.get('name', 'Utilisateur')}</h1>
                    <p class="text-base-content/70">@{user.get('username', 'user')}</p>
                    <p class="mt-2">{user.get('bio', '')}</p>
                    
                    <div class="flex gap-4 mt-4 flex-wrap">
                        {Badge.render(f"📝 {user.get('posts', 0)} posts", variant="ghost")}
                        {Badge.render(f"👥 {user.get('followers', 0)} followers", variant="ghost")}
                        {Badge.render(f"➡️ {user.get('following', 0)} following", variant="ghost")}
                    </div>
                </div>
                
                <div class="flex gap-2">
                    {Button.render("✏️ Éditer", variant="ghost")}
                    {Button.render("📤 Partager", variant="ghost")}
                </div>
            </div>
        </div>
        
        {Divider.render()}
        """
        
        return Markup(f"""
            {profile_header}
            {content}
        """)
    

    @staticmethod
    def render