from __future__ import annotations

import importlib.metadata

import sphinx_deployment as m


def test_version():
    assert importlib.metadata.version("sphinx_deployment") == m.__version__
