import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

import jinja2
from markupsafe import Markup

from ..cache import CacheManager
from ..components import ComponentExtension, ComponentExtensions, auto_register_components
from ..filters import (
    filter_currency,
    filter_json_pretty,
    filter_slugify,
    filter_timeago,
    filter_truncate,
)
from ..globals import breadcrumbs, generate_csrf_token, paginate
from ..mfe import MFEClient

logger = logging.getLogger(__name__)


def build_environment(
    directory: str,
    debug: bool,
    bytecode_cache: bool,
    mfe_client: MFEClient,
    asset_versions: Dict[str, str],
) -> jinja2.Environment:
    """Create and configure a Jinja2 Environment."""

    cache_dir = Path(".jinja_cache")
    cache_dir.mkdir(exist_ok=True)

    auto_register_components(f"{directory}/components")

    options: Dict[str, Any] = dict(
        loader=jinja2.FileSystemLoader(directory),
        auto_reload=debug,
        enable_async=True,
        trim_blocks=True,
        lstrip_blocks=True,
        autoescape=jinja2.select_autoescape(["html", "xml"]),
    )
    if bytecode_cache:
        options["bytecode_cache"] = jinja2.FileSystemBytecodeCache(str(cache_dir))

    env = jinja2.Environment(**options)  # type: ignore
    env.add_extension(ComponentExtension)
    env.add_extension(ComponentExtensions)

    def static_url(path: str) -> str:
        version = asset_versions.get(path, "")
        return f"/static/{path}?v={version}" if version else f"/static/{path}"

    def build_url(name: str, **params) -> str:
        url = f"/{name}"
        if params:
            url += "?" + "&".join(f"{k}={v}" for k, v in params.items())
        return url

    env.globals.update(
        {
            "static": static_url,
            "url": build_url,
            "render_mfe": mfe_client.fetch,
            "csrf_token": generate_csrf_token,
            "paginate": paginate,
            "breadcrumbs": breadcrumbs,
            "now": datetime.now,
        }
    )

    env.filters.update(
        {
            "json": lambda obj: Markup(json.dumps(obj, ensure_ascii=False)),
            "json_pretty": filter_json_pretty,
            "truncate": filter_truncate,
            "slugify": filter_slugify,
            "currency": filter_currency,
            "timeago": filter_timeago,
        }
    )

    return env
