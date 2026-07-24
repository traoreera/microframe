"""MicroFrame CLI — render, build, and scaffold templates."""

import argparse
import asyncio
import json
import sys
from pathlib import Path

from microframe import TemplateEngine


def _load_ctx(path: str) -> dict:
    if path == "-":
        return json.load(sys.stdin)
    with open(path) as f:
        return json.load(f)


async def _cmd_render(args):
    ctx = {}
    if args.ctx:
        ctx = _load_ctx(args.ctx)

    engine = TemplateEngine(directory=args.dir, debug=False, enable_minify=not args.no_minify)
    html = await engine.render(args.template, ctx)

    if args.out:
        Path(args.out).write_text(html)
    else:
        sys.stdout.write(html)


async def _cmd_build(args):
    ctx = {}
    if args.ctx:
        ctx = _load_ctx(args.ctx)

    templates_dir = args.dir
    out_dir = args.out
    engine = TemplateEngine(
        directory=templates_dir,
        debug=False,
        enable_minify=not args.no_minify,
    )

    templates = engine.list_templates()
    if not templates:
        print(f"No templates found in {templates_dir}", file=sys.stderr)
        return

    for name in templates:
        if not name.endswith((".html", ".htm", ".xml", ".svg")):
            continue
        html = await engine.render(name, ctx)
        dest = Path(out_dir) / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html)
        print(f"  built  {name}  ->  {dest}")


def _cmd_scaffold(args):
    if args.ctype == "html":
        _scaffold_html_component(args.name, args.dir)
    else:
        _scaffold_py_component(args.name, args.dir)


def _scaffold_html_component(name: str, templates_dir: str):
    dest = Path(templates_dir) / "components" / f"{name}.html"
    dest.parent.mkdir(parents=True, exist_ok=True)

    if dest.exists():
        print(f"exists  {dest}", file=sys.stderr)
        return

    content = f"""<div class="{name}">
  {{{{ slot }}}}
</div>
"""
    dest.write_text(content)
    print(f"created  {dest}")


def _scaffold_py_component(name: str, templates_dir: str):
    dest = Path(templates_dir) / f"{name}.py"
    if dest.exists():
        print(f"exists  {dest}", file=sys.stderr)
        return

    class_name = "".join(word.capitalize() for word in name.replace("-", "_").split("_"))
    content = f"""from microframe import UIComponent, ui_register


@ui_register
class {class_name}(UIComponent):
    def render(self):
        return f'<div class="{name}">{{{{ self.props.get("slot", "") }}}}</div>'
"""
    dest.write_text(content)
    print(f"created  {dest}")


def main():
    parser = argparse.ArgumentParser(
        prog="microframe", description="MicroFrame template engine CLI"
    )

    sub = parser.add_subparsers(dest="command", required=True)

    # render
    r = sub.add_parser("render", help="Render a single template")
    r.add_argument("template", help="Template name (e.g. index.html)")
    r.add_argument("--dir", default="templates", help="Templates directory (default: templates)")
    r.add_argument("--ctx", help="Context JSON file or '-' for stdin")
    r.add_argument("--out", help="Output file (default: stdout)")
    r.add_argument("--no-minify", action="store_true", help="Disable HTML minification")

    # build
    b = sub.add_parser("build", help="Render all templates to a directory")
    b.add_argument("--dir", default="templates", help="Templates directory (default: templates)")
    b.add_argument("--out", default="dist", help="Output directory (default: dist)")
    b.add_argument("--ctx", help="Context JSON file")
    b.add_argument("--no-minify", action="store_true", help="Disable HTML minification")

    # scaffold
    s = sub.add_parser("scaffold", help="Scaffold a component")
    s.add_argument("type", choices=["component"], help="Scaffold type")
    s.add_argument("name", help="Component name")
    s.add_argument(
        "--type",
        dest="ctype",
        choices=["html", "py"],
        default="html",
        help="Component type: html or py (default: html)",
    )
    s.add_argument("--dir", default="templates", help="Templates directory (default: templates)")

    args = parser.parse_args()

    if args.command == "scaffold":
        _cmd_scaffold(args)
    elif args.command == "render":
        asyncio.run(_cmd_render(args))
    else:
        asyncio.run(_cmd_build(args))


if __name__ == "__main__":
    main()
