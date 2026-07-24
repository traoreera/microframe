import re

from jinja2.ext import Extension


def _parse_attrs(attrs_str: str) -> str:
    """Convert HTML-style attributes to Jinja2 keyword arguments."""
    result = []
    for m in re.finditer(r'(\w+)=(?:"([^"]*)"|\'([^\']*)\'|(\d+\.?\d*)|(\w+))', attrs_str):
        key = m.group(1)
        if m.group(2):
            val = m.group(2)
            result.append(f'{key}="{val}"' if "{{" not in val else f"{key}={val}")
        elif m.group(3):
            val = m.group(3)
            result.append(f'{key}="{val}"' if "{{" not in val else f"{key}={val}")
        elif m.group(4):
            result.append(f"{key}={m.group(4)}")
        elif m.group(5):
            lower = m.group(5).lower()
            result.append(key + ("=" + lower if lower in ("true", "false", "none", "null") else f'="{m.group(5)}"'))
    return " " + " ".join(result) if result else ""


class HtmlRemoteActionExtension(Extension):
    """Preprocessor: converts <remote> and <action> HTML tags to Jinja2 syntax.

    <remote name="x.y" key="val"> → {% remote "x.y" key="val" %}{% endremote %}
    <remote name="x.y">body</remote> → {% remote "x.y" %}body{% endremote %}
    <action name="x.y">body</action> → {% action "x.y" %}body{% endaction %}
    <action name="x.y" /> → {% action "x.y" %}{% endaction %}
    """

    def preprocess(self, source, name, filename=None):
        return self._convert(source)

    def _convert(self, source: str) -> str:
        source = self._convert_self_closing(source)
        source = self._convert_block(source)
        return source

    @staticmethod
    def _convert_self_closing(source: str) -> str:
        """<remote name="x" /> → {% remote "x" %}{% endremote %}"""
        source = re.sub(
            r"<remote\s+name=(\"[^\"]*\"|'[^']*')([^>]*?)\s*/>",
            lambda m: '{% remote ' + m.group(1) + _parse_attrs(m.group(2)) + ' %}{% endremote %}',
            source,
        )
        source = re.sub(
            r"<action\s+name=(\"[^\"]*\"|'[^']*')([^>]*?)\s*/>",
            lambda m: '{% action ' + m.group(1) + _parse_attrs(m.group(2)) + ' %}{% endaction %}',
            source,
        )
        return source

    @staticmethod
    def _convert_block(source: str) -> str:
        """<remote name="x">body</remote> → {% remote "x" %}body{% endremote %}"""

        for tag_name in ("remote", "action"):
            pattern = re.compile(
                rf"<{tag_name}\s+name=(\"[^\"]*\"|'[^']*')([^>]*)>(.*?)</{tag_name}>",
                re.DOTALL,
            )
            prev = None
            while prev != source:
                prev = source
                source = re.sub(
                    pattern,
                    lambda m, t=tag_name: '{% ' + t + ' ' + m.group(1) + _parse_attrs(m.group(2))
                    + ' %}' + m.group(3) + '{% end' + t + ' %}',
                    source,
                )
        return source
