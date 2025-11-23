"""
Tests for MicroUI DaisyUI Components
"""
import pytest


class TestDaisyUIKit:
    """Test basic DaisyUI components"""

    def test_button_render(self):
        """Test Button component rendering"""
        from microui import Button

        html = Button.render("Click Me", variant="primary")
        assert "button" in html.lower()
        assert "Click Me" in html
        assert "btn-primary" in html or "primary" in html

    def test_card_render(self):
        """Test Card component rendering"""
        from microui import Card

        html = Card.render(title="Card Title", body="Card body content")
        assert "Card Title" in html
        assert "Card body content" in html
        assert "card" in html.lower()

    def test_alert_render(self):
        """Test Alert component rendering"""
        from microui import Alert

        html = Alert.render("Success message", type="success")
        assert "Success message" in html
        assert "alert" in html.lower()
        assert "success" in html.lower()

    def test_input_render(self):
        """Test Input component rendering"""
        from microui import Input

        html = Input.render(name="username", placeholder="Enter username")
        assert "username" in html
        assert "Enter username" in html
        assert "input" in html.lower()

    def test_button_with_htmx(self):
        """Test Button with HTMX attributes"""
        from microui import Button

        html = Button.render("Load More", hx_get="/api/more", hx_target="#content")
        assert "Load More" in html
        assert "hx-get" in html or "hx_get" in html
        assert "/api/more" in html

    def test_modal_render(self):
        """Test Modal component rendering"""
        from microui import Modal

        html = Modal.render(
            id="test-modal",
            title="Modal Title",
            content="Modal content here"
        )
        assert "test-modal" in html
        assert "Modal Title" in html
        assert "Modal content here" in html
        assert "modal" in html.lower()

    def test_table_render(self):
        """Test Table component rendering"""
        from microui import Table

        headers = ["Name", "Email", "Role"]
        rows = [
            ["John Doe", "john@example.com", "Admin"],
            ["Jane Smith", "jane@example.com", "User"],
        ]
        
        html = Table.render(headers=headers, rows=rows)
        assert "Name" in html
        assert "Email" in html
        assert "John Doe" in html
        assert "jane@example.com" in html
        assert "table" in html.lower()

    def test_badge_render(self):
        """Test Badge component rendering"""
        from microui import Badge

        html = Badge.render("New", variant="success")
        assert "New" in html
        assert "badge" in html.lower()

    def test_navbar_render(self):
        """Test Navbar component rendering"""
        from microui import Navbar

        html = Navbar.render(
            brand="MyApp",
            items=[
                {"text": "Home", "href": "/"},
                {"text": "About", "href": "/about"},
            ]
        )
        assert "MyApp" in html
        assert "Home" in html
        assert "About" in html
        assert "navbar" in html.lower()


class TestAdvancedComponents:
    """Test advanced MicroUI components"""

    def test_sidebar_render(self):
        """Test Sidebar component"""
        from microui import Sidebar

        html = Sidebar.render(
            items=[
                {"label": "Dashboard", "href": "/dashboard",},
                {"label": "Settings", "href": "/settings"},
            ]
        )
        assert "Dashboard" in html
        assert "Settings" in html

    def test_tabs_render(self):
        """Test Tabs component"""
        from microui import Tabs

        html = Tabs.render(
            tabs=[
                {"id": "tab1", "title": "Tab 1", "content": "Content 1"},
                {"id": "tab2", "title": "Tab 2", "content": "Content 2"},
            ]
        )
        assert "tab1" in html
        assert "tab2" in html
        assert "Content 1" in html

    def test_avatar_render(self):
        """Test Avatar component"""
        from microui import Avatar

        html = Avatar.render(src="/user.jpg", alt="User Avatar")
        assert "avatar" in html.lower()
        assert "/user.jpg" in html

    def test_progress_render(self):
        """Test Progress component"""
        from microui import Progress

        html = Progress.render(value=75, max=100)
        assert "progress" in html.lower()
        assert "75" in html

    def test_stats_render(self):
        """Test Stats component"""
        from microui import Stats

        html = Stats.render(
            stats=[
                {"title": "Users", "value": "1,234", "icon": "👥"},
                {"title": "Revenue", "value": "$56K", "icon": "💰"},
            ]
        )
        assert "Users" in html
        assert "1,234" in html
        assert "Revenue" in html


class TestLayoutComponents:
    """Test layout components"""

    def test_pricing_layout(self):
        """Test Pricing layout"""
        from microui.layout import Pricing

        html = Pricing.simple_pricing_card(
            name="Basic",
            price="$9.99",
            currency="$",
            period="/mois",
            description="Lorem ipsum dolor sit amet",
            features=["Feature 1", "Feature 2", "Feature 3"],
            cta_text="Choisir ce plan",
            featured=True
        )

        html+= Pricing.simple_pricing_card(
            name="Pro",
            price="$19.99",
            currency="$",
            period="/mois",
            description="Lorem ipsum dolor sit amet",
            features=["Feature 1", "Feature 2", "Feature 3"],
            cta_text="Choisir ce plan",
            featured=True
        )
        assert "Basic" in html
        assert "Pro" in html
        assert "$9.99" in html
        assert "$19.99" in html

    def test_contact_form(self):
        """Test Contact form layout"""
        from microui.layout import Contact

        html = Contact.contact_form(form_action="/contact",)
        assert "form" in html.lower()
        assert "/contact" in html
        assert "post" in html.lower()
