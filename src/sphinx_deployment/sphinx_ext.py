from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Any

from jinja2 import Template
from loguru import logger
from sphinx.application import Sphinx
from sphinx.config import Config
from sphinx.util.fileutil import copy_asset

from ._version import version


def _generate_deployment_assets(app: Sphinx, exc: Any) -> None:
    """
    Generate the deployment assets to the Sphinx output directory
    if the builder format is HTML and no exception occurred.

    Parameters:
        app (Sphinx): The Sphinx application object.
        exc (Any): The exception object.

    Returns:
        None
    """
    if app.builder.format == "html" and not exc:
        dst_static_dir = Path(app.builder.outdir, "_static")
        src_static_dir = Path(__file__).parent.resolve().joinpath("_static")
        dst_theme_dir = dst_static_dir.joinpath("theme", "rtd")
        src_theme_dir = src_static_dir.joinpath("theme", "rtd")

        if dst_theme_dir.exists():
            shutil.rmtree(dst_theme_dir)

        customized_tpl = src_static_dir.joinpath("templates", "rtd.html")
        with customized_tpl.open("r", encoding="utf-8") as f:
            t = Template(f.read(), autoescape=True, keep_trailing_newline=True)
            rdr = t.render(sphinx_deployment_dll=app.config.sphinx_deployment_dll)
            copy_asset(
                src_theme_dir,
                dst_theme_dir,
                context={"customizedItems": rdr},
                onerror=lambda file, e: logger.error(f"Failed to copy {file}: {e}"),
            )


def _html_page_context(
    app: Sphinx,
    pagename: str,
    templatename: str,
    context: dict[str, Any],
    doctree: object,
) -> None:
    """
    A description of the entire function, its parameters, and its return types.

    Parameters:
        app (sphinx.application.Sphinx): The app to set up.
        pagename (str): The name of the page.
        templatename (str): The name of the template.
        context (typing.Dict[str, typing.Any]): The context to set up.
        doctree (object): The doctree to set up.

    Returns:
        None
    """
    _ = (pagename, templatename, context, doctree)

    # Get the path to the versions.json file
    context["versions_file"] = str(
        Path(context["content_root"]) / ".." / "versions.json"
    )

    # Register css and js files
    app.add_js_file(
        None,
        body="var sphinx_deployment_versions_file = '"
        + context["versions_file"]
        + "';",
        priority=0,
    )

    app.add_css_file("theme/rtd/rtd.css", priority=600)
    app.add_js_file("theme/rtd/rtd.js", priority=600)


def _config_inited(app: Sphinx, config: Config) -> None:
    """
    A description of the entire function, its parameters, and its return types.

    Parameters:
        app (sphinx.application.Sphinx): The app to set up.
        config (sphinx.config.Config): The config to set up.

    Returns:
        None
    """
    _ = (app, config)
    app.connect("html-page-context", _html_page_context)


def setup(app: Sphinx) -> dict[str, str | bool]:
    """
    Register the extension with Sphinx.

    Parameters:
        app (sphinx.application.Sphinx): The app to set up.

    Returns:
        dict[str, str | bool]: A dictionary metadata about the extension.
    """

    if os.environ.get("SPHINX_DEPLOYMENT_VERSION", None):
        logger.info(f"sphinx_deployment deploys docs {version} from {app.confdir}")
        app.add_config_value("sphinx_deployment_dll", {}, "html")
        app.connect("config-inited", _config_inited)
        app.connect("build-finished", _generate_deployment_assets)

    return {
        "version": version,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
