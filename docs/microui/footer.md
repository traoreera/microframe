# Footer Component

Documentation for the `Footer` component from `microui/components/footer.py`.

The footer is a crucial part of any website, providing essential links, copyright information, and contact details.

## Footer.render()

**Parameters:**
- `sections` (List[Dict]): A list of sections to display in the footer. Each section is a dictionary with a `title` and a list of `links`.
- `social_links` (Dict[str, str]): A dictionary of social media links, where the key is the name of the social media platform and the value is the URL.
- `copyright_text` (str): The copyright text to display.
- `classes` (str): Additional CSS classes to apply to the footer.

**Example:**
```python
from microui.components import Footer

footer_content = Footer.render(
    sections=[
        {"title": "Services", "links": [
            {"text": "Branding", "href": "#"},
            {"text": "Design", "href": "#"},
            {"text": "Marketing", "href": "#"},
            {"text": "Advertisement", "href": "#"},
        ]},
        {"title": "Company", "links": [
            {"text": "About us", "href": "/about"},
            {"text": "Contact", "href": "/contact"},
            {"text": "Jobs", "href": "/jobs"},
            {"text": "Press kit", "href": "/press"},
        ]},
        {"title": "Legal", "links": [
            {"text": "Terms of use", "href": "/terms"},
            {"text": "Privacy policy", "href": "/privacy"},
            {"text": "Cookie policy", "href": "/cookies"},
        ]},
    ],
    social_links={
        "twitter": "https://twitter.com/mycompany",
        "youtube": "https://youtube.com/mycompany",
        "facebook": "https://facebook.com/mycompany",
    },
    copyright_text="© 2025 My Company, Inc. All rights reserved."
)
```
