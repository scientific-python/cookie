# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

from __future__ import annotations

# Warning: do not change the path here. To use autodoc, you need to install the
# package first.

# -- Project information -----------------------------------------------------

project = "{{ cookiecutter.project_name }}"
copyright = "{{ cookiecutter.year }}, {{ cookiecutter.full_name }}"
author = "{{ cookiecutter.full_name }}"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
{%- if cookiecutter.project_type != "poetry" %}
    "myst_parser",
{%- endif %}
    "sphinx.ext.autodoc",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinx_copybutton",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = []

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "**.ipynb_checkpoints", "Thumbs.db", ".DS_Store", ".env"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_book_theme"

html_title = f"{project}"

html_baseurl = "https://{{ cookiecutter.project_name }}.readthedocs.io/en/latest/"

html_theme_options = {
    "home_page_in_toc": True,
    "repository_url": "{{ cookiecutter.url }}",
    "use_repository_button": True,
    "use_issues_button": True,
    "use_edit_page_button": True,
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path: list[str] = []
