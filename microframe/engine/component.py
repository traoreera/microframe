# app/engine/component_extension.py

from pathlib import Path
from typing import Any

import jinja2
from jinja2 import nodes
from jinja2.ext import Extension
from markupsafe import Markup


class ComponentRegistry:
    registry = {}

    @classmethod
    def register(cls, name, template):
        cls.registry[name] = template

    @classmethod
    def get(cls, name):
        return cls.registry.get(name)

    @classmethod
    def clear(cls):
        cls.registry.clear()

    @classmethod
    def delete(cls, name):
        cls.registry.pop(name, None)


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

    def _render(self, name, caller, **props) -> str | Any:
        template = ComponentRegistry.get(name)
        if not template:
            return f"<p class='error'>Component '{name}' not found</p>"

        props["slot"] = Markup(caller())
        try:
            return jinja2.Template(template).render(**props)
        except Exception as e:
            return f"<p class='error'>Error rendering component '{name}': {e}</p>"


def auto_register_components(folder):
    """_summary_

    Args:
        folder (str): path to folder containing components
    """
    folder = Path(folder)
    if not folder.exists():
        return

    for file in folder.glob("*.html"):
        ComponentRegistry.register(file.stem, file.read_text())
