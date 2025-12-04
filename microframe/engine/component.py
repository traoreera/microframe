# app/engine/component_extension.py - Version avec support async complet

import logging
import re
from pathlib import Path
from typing import Any

import jinja2
from jinja2 import nodes
from jinja2.ext import Extension
from markupsafe import Markup

logger = logging.getLogger(__name__)


class ComponentRegistry:
    """Registry for storing component templates."""
    registry = {}

    @classmethod
    def register(cls, name, template):
        cls.registry[name] = template
        logger.info(f"✓ Registered component: {name}")

    @classmethod
    def get(cls, name):
        return cls.registry.get(name)

    @classmethod
    def clear(cls):
        cls.registry.clear()

    @classmethod
    def delete(cls, name):
        cls.registry.pop(name, None)
    
    @classmethod
    def list_components(cls):
        return sorted(cls.registry.keys())


class ComponentTag(Extension):
    """Extension that handles {% component %} tags with async support."""
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

        # ✅ Use _render_async for async support
        return nodes.CallBlock(
            self.call_method("_render_async", [component_name], props), 
            [], 
            [], 
            body
        ).set_lineno(lineno)

    async def _render_async(self, name, caller, **props):
        """Async version of render that properly awaits caller()."""
        template = ComponentRegistry.get(name)
        if not template:
            logger.warning(f"Component '{name}' not found")
            return f"<!-- Component '{name}' not found -->"

        try:
            # ✅ Await the caller coroutine
            slot_content = await caller()
            props["slot"] = Markup(slot_content) if slot_content else Markup("")
        except Exception as e:
            logger.error(f"Error getting slot content: {e}")
            props["slot"] = Markup("")

        try:
            # Use self.environment and render async
            if hasattr(template, "render"):
                slot_content = await caller()
                props["children"] = slot_content
                template.props = props
                template.children = slot_content
                return template.render(self:=template)


            template_obj = self.environment.from_string(template)
            return await template_obj.render_async(**props)
        except Exception as e:
            logger.exception(f"Error rendering component '{name}'")
            return f"<!-- Error rendering component '{name}': {e} -->"


class ComponentExtensions(Extension):
    """Preprocessor for <component.X> syntax."""

    def preprocess(self, source, name, filename=None):
        """Convert <component.X> to {% component %} tags."""
        return self._convert_components(source)

    def _convert_components(self, source: str) -> str:
        """Convert <component.X> syntax to {% component %} syntax."""
        
        def parse_props(props_str: str) -> str:
            """Parse HTML-like attributes to Jinja2 kwargs."""
            if not props_str.strip():
                return ""
            
            props = []
            pattern = r'(\w+)=(?:"([^"]*)"|\'([^\']*)\'|(\d+\.?\d*)|(\w+))'
            matches = re.findall(pattern, props_str)
            
            for match in matches:
                key = match[0]
                if match[1]:  # Double quotes
                    if '{{' in match[1] or '{%' in match[1]:
                        props.append(f'{key}={match[1]}')
                    else:
                        props.append(f'{key}="{match[1]}"')
                elif match[2]:  # Single quotes
                    if '{{' in match[2] or '{%' in match[2]:
                        props.append(f'{key}={match[2]}')
                    else:
                        props.append(f'{key}="{match[2]}"')
                elif match[3]:  # Numbers
                    props.append(f'{key}={match[3]}')
                elif match[4]:  # Boolean or bare words
                    lower = match[4].lower()
                    if lower in ('true', 'false', 'none', 'null'):
                        props.append(f'{key}={lower}')
                    else:
                        props.append(f'{key}={match[4]}')
            
            return " " + " ".join(props) if props else ""

        # Block components
        block_pattern = re.compile(
            r'<component\.(\w+)([^>]*)>(.*?)</component\.\1>',
            re.DOTALL
        )
        
        def replace_block(match):
            name, props_str, slot_content = match.groups()
            props = parse_props(props_str)
            return f'{{% component "{name}"{props} %}}{slot_content}{{% endcomponent %}}'
        
        source = re.sub(block_pattern, replace_block, source)
        
        # Self-closing components
        self_closing_pattern = re.compile(r'<component\.(\w+)([^/]*)/>')
        
        def replace_self_closing(match):
            name, props_str = match.groups()
            props = parse_props(props_str)
            return f'{{% component "{name}"{props} %}}{{% endcomponent %}}'
        
        source = re.sub(self_closing_pattern, replace_self_closing, source)
        
        return source


def auto_register_components(folder):
    """Auto-register components from folder.
    
    Args:
        folder (str): path to folder containing components
    """
    folder = Path(folder)
    if not folder.exists():
        raise NotADirectoryError(f"Folder not found: {folder}")
    
    for file in folder.glob("*.html"):
        try:
            ComponentRegistry.register(file.stem, file.read_text(encoding="utf-8"))
        except Exception as e:
            raise e from e