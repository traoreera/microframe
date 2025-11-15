from markupsafe import Markup


class UI:
    """Composants UI Tailwind + HTMX"""

    @staticmethod
    def button(label, variant="primary", **attrs):
        variants = {
            "primary": "bg-blue-600 hover:bg-blue-700 text-white",
            "secondary": "bg-gray-200 hover:bg-gray-300 text-gray-900",
            "danger": "bg-red-600 hover:bg-red-700 text-white",
        }

        htmx = " ".join([f'hx-{k.replace("_", "-")}="{v}"' for k, v in attrs.items()])
        html = f"""
        <button 
            class="px-4 py-2 rounded-lg font-medium {variants.get(variant)}"
            {htmx}
        >
            {label}
        </button>
        """
        return Markup(html.strip())

    @staticmethod
    def badge(label, color="blue"):
        html = f"""
        <span class="px-2 py-1 text-sm bg-{color}-100 text-{color}-800 rounded">
            {label}
        </span>
        """
        return Markup(html.strip())
