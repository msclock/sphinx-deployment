from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Any

from loguru import logger
from sphinx.application import Sphinx
from sphinx.config import Config
from sphinx.util.fileutil import copy_asset

from ._version import version


def _copy_custom_files(app: Sphinx, exc: Any) -> None:
    """
    Copy custom files to the Sphinx output directory if the builder format is HTML and no exception occurred.

    Parameters:
        app (Sphinx): The Sphinx application object.
        exc (Any): The exception object.

    Returns:
        None
    """
    if app.builder.format == "html" and not exc:
        dest_static_dir = Path(app.builder.outdir, "_static")
        rc_dir = Path(__file__).parent.resolve()
        _copy_assset_dir_impl(
            dest_asset_dir=dest_static_dir.joinpath("versioning"),
            src_assets_dir=rc_dir.joinpath("versioning"),
        )


def _copy_assset_dir_impl(dest_asset_dir: Path, src_assets_dir: Path) -> None:
    """
    Copy the contents of the source assets directory to the destination assets directory.

    Args:
        dest_asset_dir (Path): The path to the destination assets directory.
        src_assets_dir (Path): The path to the source assets directory.

    Returns:
        None: This function does not return anything.
    """
    if Path(dest_asset_dir).exists():
        shutil.rmtree(dest_asset_dir)
    copy_asset(src_assets_dir, dest_asset_dir)


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
    app.add_css_file("versioning/css/rtd.css", priority=100)
    app.add_js_file("versioning/js/rtd.js")


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
        app.connect("config-inited", _config_inited)
        app.connect("build-finished", _copy_custom_files)

    return {
        "version": version,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
