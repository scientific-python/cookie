{%- if cookiecutter.project_type == "flit" -%}
"""
{{ cookiecutter.project_short_description }}
"""

{% endif -%}

{%- if cookiecutter.project_type == "setuptools" or cookiecutter.project_type == "pybind11" -%}
from .version import version as __version__
{%- else -%}
__version__ = "0.1.0"
{%- endif %}

__all__ = ("__version__",)
