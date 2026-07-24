import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Union

import jinja2
from markupsafe import Markup

from ..cache import CacheManager
from ..components import (ComponentExtension, ComponentExtensions,
                          auto_register_components)
from ..filters import (filter_currency, filter_json_pretty, filter_slugify,
                       filter_timeago, filter_truncate)
from ..globals import breadcrumbs, generate_csrf_token, paginate
from ..mfe import MFEClient
from ..remote import (ActionExtension, HtmlRemoteActionExtension,
                      RemoteExtension)
from ..ui import setup_microui

logger = logging.getLogger(__name__)


def build_environment(
    directory: Union[str, Sequence[str]],
    debug: bool,
    bytecode_cache: bool,
    mfe_client: MFEClient,
    asset_versions: Dict[str, str],
    enable_ui: bool = False,
    remote_caller: Optional[Callable] = None,
    action_resolver: Optional[Callable] = None,
    csrf_token: str = "",
    namespaces: Optional[Dict[str, str]] = None,
) -> jinja2.Environment:
    """Create and configure a Jinja2 Environment.

    `directory` is the shared search path (single path or list) for common
    templates like `base.html` — every namespace can `{% extends %}` from it.

    `namespaces` lets several plugins each own a template directory without
    filename collisions: `{"blog": "plugins/blog/templates", "crm": "..."}`
    exposes each plugin's templates under `blog/index.html`, `crm/index.html`,
    etc. (jinja2.PrefixLoader), while `directory` stays unprefixed for the
    shared layout. Without `namespaces`, a list `directory` still works as a
    flat search path, but same-named templates in different plugin dirs will
    silently shadow each other — use `namespaces` once you have more than one
    plugin contributing templates.
    """

    cache_dir = Path(".jinja_cache")
    cache_dir.mkdir(exist_ok=True)

    directories: List[str] = [directory] if isinstance(directory, str) else list(directory)
    for d in directories:
        auto_register_components(f"{d}/components")

    loader: jinja2.BaseLoader = jinja2.FileSystemLoader(directories)
    if namespaces:
        for name, ns_dir in namespaces.items():
            auto_register_components(f"{ns_dir}/components")
        loader = jinja2.ChoiceLoader(
            [
                loader,
                jinja2.PrefixLoader(
                    {name: jinja2.FileSystemLoader(ns_dir) for name, ns_dir in namespaces.items()}
                ),
            ]
        )

    options: Dict[str, Any] = dict(
        loader=loader,
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
    env.add_extension(RemoteExtension)
    env.add_extension(ActionExtension)
    env.add_extension(HtmlRemoteActionExtension)

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
            "csrf_token": lambda: csrf_token or generate_csrf_token(),
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

    if enable_ui:
        setup_microui(env)

    if remote_caller:
        env.globals["_remote_caller"] = remote_caller
    if action_resolver:
        env.globals["_action_resolver"] = action_resolver

    return env
