from markupsafe import Markup # type: ignore
from microui.core.extension import Component





class Card(Component):

    def render(self):
        
        title = self.props.get("title")
        image = self.props.get("img", "https://picsum.photos/500/300?random=3")
        bordered = self.props.get("bordered")
        size = self.props.get("size", "sm")

        css_class = ['card', 'bg-base-100']
        css_class.extend(
            f"card-{key}"
            for key, _ in self.props.items()
            if key in ["compact", "side"]
        
        )
        if bordered: css_class.append("card-bordered")
        print(self.children)
        return Markup(f"""
            <div class="{' '.join(css_class)}">
                <figure>
                    <img src="{image}" alt="Shoes" />
                </figure>
                <div class="card-body">
                    <h2 class="card-title">{title}</h2>
                    {self.children}
                </div>
            </div>
        """)
