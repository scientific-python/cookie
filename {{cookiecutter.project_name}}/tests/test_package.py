from __future__ import annotations

import importlib.metadata

import {{ cookiecutter.__project_slug }} as m


def test_version() -> None:
    assert importlib.metadata.version("{{ cookiecutter.__project_slug }}") == m.__version__
