# {{ cookiecutter.project_name }}

[![Actions Status][actions-badge]][actions-link]
[![Documentation Status][rtd-badge]][rtd-link]

[![PyPI version][pypi-version]][pypi-link]
[![Conda-Forge][conda-badge]][conda-link]
[![PyPI platforms][pypi-platforms]][pypi-link]

[![GitHub Discussion][github-discussions-badge]][github-discussions-link]
{%- if cookiecutter.org | lower == "scikit-hep" %}
[![Scikit-HEP][sk-badge]](https://scikit-hep.org/)
{%- endif %}

<!-- SPHINX-START -->

<!-- prettier-ignore-start -->
[actions-badge]:            {{cookiecutter.url}}/workflows/CI/badge.svg
[actions-link]:             {{cookiecutter.url}}/actions
[conda-badge]:              https://img.shields.io/conda/vn/conda-forge/{{cookiecutter.project_name}}
[conda-link]:               https://github.com/conda-forge/{{cookiecutter.project_name}}-feedstock
[github-discussions-badge]: https://img.shields.io/static/v1?label=Discussions&message=Ask&color=blue&logo=github
[github-discussions-link]:  {{cookiecutter.url}}/discussions
[pypi-link]:                https://pypi.org/project/{{cookiecutter.project_name}}/
[pypi-platforms]:           https://img.shields.io/pypi/pyversions/{{cookiecutter.project_name}}
[pypi-version]:             https://img.shields.io/pypi/v/{{cookiecutter.project_name}}
[rtd-badge]:                https://readthedocs.org/projects/{{cookiecutter.project_name}}/badge/?version=latest
[rtd-link]:                 https://{{cookiecutter.project_name}}.readthedocs.io/en/latest/?badge=latest
{%- if cookiecutter.org | lower == "scikit-hep" %}
[sk-badge]:                 https://scikit-hep.org/assets/images/Scikit--HEP-Project-blue.svg
{%- endif %}

<!-- prettier-ignore-end -->
