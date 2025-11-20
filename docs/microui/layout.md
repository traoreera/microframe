# Layout Components

Documentation for layout components from `microui/layout.py`.

## Pricing Component

Pricing tables and cards for displaying subscription plans and pricing information.

### Pricing.pricing_table()

Display multiple pricing plans in a grid layout.

**Parameters:**
- `plans` (List[dict]): List of pricing plans
  - Each plan: `{"name": str, "price": str, "description": str, "features": List[str], "cta_text": str}`
- `featured_plan` (Optional[int]): Index of featured plan (highlighted)
- `currency` (str, default="€"): Currency symbol
- `period` (str, default="/mois"): Billing period
- `classes` (str, default=""): Additional CSS classes

**Returns:** `Markup` - Rendered HTML

**Example:**
```python
from microui import Pricing

pricing = Pricing.pricing_table(
    plans=[
        {
            "name": "Free",
            "price": "0",
            "description": "For individuals",
            "features": ["5 projects", "Email support", "1GB storage"],
            "cta_text": "Get Started"
        },
        {
            "name": "Pro",
            "price": "29",
            "description": "For professionals",
            "features": ["Unlimited projects", "Priority support", "100GB storage"],
            "cta_text": "Upgrade Now"
        },
        {
            "name": "Enterprise",
            "price": "99",
            "description": "For teams",
            "features": ["Everything in Pro", "24/7 support", "Unlimited storage"],
            "cta_text": "Contact Sales"
        }
    ],
    featured_plan=1,  # Highlight Pro plan
    currency="$",
    period="/month"
)
```

### Pricing.pricing_comparison()

Detailed comparison table of pricing plans.

**Parameters:**
- `plans` (List[dict]): Pricing plans
- `features` (List[dict]): Features to compare
  - Each feature: `{"name": str}`
- `classes` (str, default=""): Additional CSS classes

**Returns:** `Markup` - Rendered HTML

**Example:**
```python
comparison = Pricing.pricing_comparison(
    plans=[...],
    features=[
        {"name": "Projects"},
        {"name": "Storage"},
        {"name": "Support"},
        {"name": "API Access"}
    ]
)
```

### Pricing.simple_pricing_card()

Single pricing card component.

**Parameters:**
- `name` (str): Plan name
- `price` (str): Price
- `currency` (str, default="€"): Currency symbol
- `period` (str, default="/mois"): Billing period
- `description` (str, default=""): Plan description
- `features` (List[str], default=None): List of features
- `cta_text` (str, default="Choisir ce plan"): Call-to-action text
- `featured` (bool, default=False): Highlight as featured
- `classes` (str, default=""): Additional CSS classes

**Returns:** `Markup` - Rendered HTML

**Example:**
```python
card = Pricing.simple_pricing_card(
    name="Starter",
    price="9",
    currency="$",
    period="/month",
    description="Perfect for getting started",
    features=[
        "10 projects",
        "Email support",
        "10GB storage",
        "API access"
    ],
    cta_text="Start Free Trial",
    featured=True
)
```

### Pricing.pricing_page()

Complete pricing page with plans, comparison, and FAQ.

**Parameters:**
- `title` (str, default="Nos tarifs"): Page title
- `subtitle` (str, default="Choisissez le plan qui vous convient"): Page subtitle
- `plans` (List[dict], default=None): Pricing plans
- `featured_plan` (Optional[int]): Featured plan index
- `show_comparison` (bool, default=True): Show comparison table
- `comparison_features` (List[dict], default=None): Features for comparison

**Returns:** `Markup` - Complete pricing page HTML

**Example:**
```python
page = Pricing.pricing_page(
    title="Choose Your Plan",
    subtitle="Find the perfect plan for your needs",
    plans=[...],
    featured_plan=1,
    show_comparison=True
)
```

---

## Contact Component

Contact forms and pages for user communication.

### Contact.contact_form()

Contact form with customizable fields.

**Parameters:**
- `form_action` (str, default="/contact/send"): Form submission URL
- `include_subject` (bool, default=True): Include subject field
- `include_phone` (bool, default=True): Include phone field
- `include_company` (bool, default=False): Include company field
- `success_message` (Optional[str]): Success message to display
- `error_message` (Optional[str]): Error message to display
- `classes` (str, default=""): Additional CSS classes

**Returns:** `Markup` - Rendered HTML

**Example:**
```python
from microui import Contact

form = Contact.contact_form(
    form_action="/api/contact",
    include_subject=True,
    include_phone=True,
    include_company=True
)

# With messages
form_with_message = Contact.contact_form(
    success_message="Thank you! We'll get back to you soon.",
    error_message="Please fill in all required fields."
)
```

### Contact.contact_info_card()

Contact information display card.

**Parameters:**
- `title` (str, default="Informations de contact"): Card title
- `phone` (Optional[str]): Phone number
- `email` (Optional[str]): Email address
- `address` (Optional[str]): Physical address
- `hours` (Optional[str]): Business hours
- `social_links` (Optional[dict]): Social media links
  - Supported: facebook, twitter, linkedin, github, instagram
- `classes` (str, default=""): Additional CSS classes

**Returns:** `Markup` - Rendered HTML

**Example:**
```python
info_card = Contact.contact_info_card(
    title="Get in Touch",
    phone="+1 234 567 8900",
    email="hello@example.com",
    address="123 Main Street, City, Country",
    hours="Mon-Fri: 9AM-5PM",
    social_links={
        "facebook": "https://facebook.com/mycompany",
        "twitter": "https://twitter.com/mycompany",
        "linkedin": "https://linkedin.com/company/mycompany"
    }
)
```

### Contact.contact_page()

Complete contact page with form, info, map, and FAQ.

**Parameters:**
- `title` (str, default="Nous contacter"): Page title
- `subtitle` (str, default="Nous aimerions avoir de vos nouvelles..."): Page subtitle
- `show_map` (bool, default=True): Show location section
- `locations` (Optional[List[dict]]): Office locations
  - Each location: `{"name": str, "phone": str, "email": str, "address": str, "hours": str}`
- `social_links` (Optional[Dict]): Social media links
- `faq` (Optional[List[dict]]): FAQ items
  - Each FAQ: `{"question": str, "answer": str}`
- `direct_contact` (Optional[Dict], default={}): Direct contact info for main card

**Returns:** `Markup` - Complete contact page HTML

**Example:**
```python
page = Contact.contact_page(
    title="Contact Us",
    subtitle="We'd love to hear from you",
    show_map=True,
    locations=[
        {
            "name": "Main Office",
            "phone": "+1 234 567 8900",
            "email": "contact@example.com",
            "address": "123 Main St, City, Country",
            "hours": "Mon-Fri: 9AM-5PM"
        },
        {
            "name": "Support Office",
            "phone": "+1 234 567 8901",
            "email": "support@example.com",
            "address": "456 Support Ave, City, Country",
            "hours": "Mon-Fri: 8AM-6PM"
        }
    ],
    social_links={
        "facebook": "https://facebook.com/company",
        "twitter": "https://twitter.com/company"
    },
    faq=[
        {
            "question": "How can I contact support?",
            "answer": "You can reach us via email or phone during business hours."
        },
        {
            "question": "What are your business hours?",
            "answer": "We're open Monday to Friday, 9AM to 5PM."
        }
    ]
)
```

### Contact.contact_modal()

Contact form in a modal dialog.

**Parameters:**
- `modal_id` (str, default="contact-modal"): Modal ID
- `form_action` (str, default="/contact/send"): Form submission URL

**Returns:** `Markup` - Rendered HTML

**Example:**
```python
modal = Contact.contact_modal(
    modal_id="contact-modal",
    form_action="/api/contact"
)

# Open with: <button onclick="contact_modal.showModal()">Contact</button>
```

---

📚 **[Back to MicroUI Documentation](README.md)**
