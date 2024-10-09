"""
Copyright (c) {{ cookiecutter.__year }} {{ cookiecutter.full_name }}. All rights reserved.

{{ cookiecutter.project_name }}: {{ cookiecutter.project_short_description }}
"""

from __future__ import annotations

{%- if cookiecutter.backend in ["pybind11", "hatch", "skbuild", "setuptools", "flit"] and cookiecutter.vcs %}

from ._version import version as __version__

{%- elif cookiecutter.backend == "pdm" and cookiecutter.vcs %}

import importlib.metadata

__version__ = importlib.metadata.version("{{ cookiecutter.__project_slug }}")

{%- elif cookiecutter.backend == "poetry" and cookiecutter.vcs %}

__version__ = "0.0.0"

{%- else %}

__version__ = "0.1.0"

{%- endif %}

__all__ = ["__version__"]
