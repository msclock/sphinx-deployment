"""
Make the package executable with `python -m sphinx_deployment`.
"""
from __future__ import annotations

from sphinx_deployment.cli import commands

if __name__ == "__main__":
    commands()
