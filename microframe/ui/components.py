from pathlib import Path

import jinja2
from jinja2 import nodes
from jinja2.ext import Extension
from markupsafe import Markup


class ComponentRegistry:
    _registry = {}

    @classmethod
    def register(cls, name: str, template):
        cls._registry[name] = template

    @classmethod
    def get(cls, name: str):
        return cls._registry.get(name)


class ComponentExtension(Extension):
    tags = {"component"}

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        component_name = parser.parse_expression()

        props = []
        while parser.stream.current.type != "block_end":
            key = parser.parse_assign_target()
            parser.stream.expect("assign")
            value = parser.parse_expression()
            props.append(nodes.Keyword(key.name, value))

        body = parser.parse_statements(("name:endcomponent",), drop_needle=True)

        return nodes.CallBlock(
            self.call_method("_render", [component_name], props), [], [], body
        ).set_lineno(lineno)

    def _render(self, name, caller, **props):
        template = ComponentRegistry.get(name)
        if not template:
            return f"<!-- component '{name}' not found -->"

        props["slot"] = Markup(caller())
        return jinja2.Template(template).render(**props)


def auto_register_components(folder="templates/components"):
    folder = Path(folder)
    for file in folder.glob("*.html"):
        ComponentRegistry.register(file.stem, file.read_text())
        print(f"Registered component: {file.stem}")
