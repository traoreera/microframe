# microframe — Agent guide

## Quick start

```bash
make install
# or: poetry install
```

## Dev commands

```bash
poetry run pytest                    # all tests (asyncio_mode=auto)
poetry run pytest tests/test_microframe_risks.py  # single file
poetry run black --check .           # format check (line-length=100)
poetry run isort --check .           # import sort
poetry run flake8 microframe/        # lint
poetry run mypy microframe/          # type check (python_version=3.9 in config)
```

## Architecture

Single-package Python library (`microframe`, v2.0.0). Public API exported from `microframe/__init__.py`:

- `TemplateEngine` — main entrypoint (`microframe/engine/core/renderer.py`)
- `CacheManager` / `CacheBackend` — in-memory TTL cache
- `ComponentRegistry` — component registration (`{% component %}` tags)
- `MFEClient` — async micro-frontend HTTP fetcher (`microframe/engine/mfe/client.py`)
- `UIComponent` / `ui_register` / `render_microui` — Python class-based UI component system (`microframe/engine/ui/`)

All rendering is async (`await engine.render(...)`).

### CLI

Available as `microframe` after install (`microframe.cli:main`). Commands: `render`, `build`, `scaffold`.

### UI components (`microframe/engine/ui/`)

Python class-based component system extracted from microui. Components are classes decorated with `@ui_register` that implement a `render()` method. Available in templates via `{{ render_microui("name", **props) }}` when `TemplateEngine(..., enable_ui=True)`.

```python
from microframe import UIComponent, ui_register

@ui_register
class Alert(UIComponent):
    def render(self):
        return f'<div class="alert">{self.props.get("text", "")}</div>'
```

```html
<!-- template.html -->
{{ render_microui("alert", text="Hello") }}
```

## Known issues

- **CI is broken** — `.github/workflows/pyproject.yml` runs `pip install -e .[dev]` but this project uses Poetry (needs `poetry install` or `pip install poetry`)
- **Discrepancies**: `pyproject.toml` requires `python = "^3.13"` but `mypy.python_version = "3.9"` is stale; `uv.lock` says `requires-python = ">=3.14"`
- **Both `poetry.lock` and `uv.lock`** are tracked — prefer Poetry unless uv is explicitly requested

## Key files

- `FEATURES.md` — roadmap of planned features (context processors, i18n, SSG, etc.) — not yet implemented
- `microframe/engine/core/environment.py` — Jinja2 environment setup (filters, globals, components)

## Style

- Formatter: black (line-length=100)
- Import sort: isort
- Linter: flake8
- Type checker: mypy (disallow_untyped_defs=false)
