import re

from jinja2 import nodes
from jinja2.ext import Extension
from markupsafe import Markup

from .registry import ComponentRegistry


class ComponentExtension(Extension):
    """Handles {% component "name" key=value %} ... {% endcomponent %} tags."""

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
            self.call_method("_render_async", [component_name], props), [], [], body
        ).set_lineno(lineno)

    async def _render_async(self, name: str, caller, **props):
        template = ComponentRegistry.get(name)
        if not template:
            return f"<!-- Component '{name}' not found -->"
        try:
            slot_content = await caller()
            slot = Markup(slot_content) if slot_content else Markup("")
            props["slot"] = slot
            props["children"] = slot

            if hasattr(template, "render") and callable(template.render):
                template.props = props
                template.children = slot
                return template.render()

            tpl = self.environment.from_string(template)
            return await tpl.render_async(**props)
        except Exception as e:
            import traceback

            traceback.print_exc()
            return f"<!-- Error rendering component '{name}': {e} -->"


class ComponentExtensions(Extension):
    """Preprocessor: converts <component.X prop="v"> syntax to {% component %} tags."""

    def preprocess(self, source, name, filename=None):
        return self._convert(source)

    def _convert(self, source: str) -> str:
        def parse_props(props_str: str) -> str:
            props = []
            for match in re.findall(
                r'(\w+)=(?:"([^"]*)"|\'([^\']*)\'|(\d+\.?\d*)|(\w+))', props_str
            ):
                key = match[0]
                if match[1]:
                    props.append(
                        f'{key}="{match[1]}"' if "{{" not in match[1] else f"{key}={match[1]}"
                    )
                elif match[2]:
                    props.append(
                        f'{key}="{match[2]}"' if "{{" not in match[2] else f"{key}={match[2]}"
                    )
                elif match[3]:
                    props.append(f"{key}={match[3]}")
                elif match[4]:
                    lower = match[4].lower()
                    props.append(
                        f"{key}={lower if lower in ('true','false','none','null') else match[4]}"
                    )
            return (" " + " ".join(props)) if props else ""

        # Self-closing
        source = re.sub(
            r"<component\.(\w+)([^/]*)/>",
            lambda m: f'{{% component "{m.group(1)}"{parse_props(m.group(2))} %}}{{% endcomponent %}}',
            source,
        )

        # Block components (innermost-first loop)
        pattern = re.compile(
            r"<component\.(\w+)([^>]*)>((?:(?!<component\.).)*?)</component\.\1>", re.DOTALL
        )
        prev = None
        while prev != source:
            prev = source
            source = re.sub(
                pattern,
                lambda m: f'{{% component "{m.group(1)}"{parse_props(m.group(2))} %}}{m.group(3)}{{% endcomponent %}}',
                source,
            )

        return source
