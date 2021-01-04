# {{ cookiecutter.project_name }}

[![Actions Status][actions-badge]][actions-link]
[![Documentation Status][rtd-badge]][rtd-link]
[![Code style: black][black-badge]][black-link]

[![PyPI version][pypi-version]][pypi-link]
[![Conda-Forge][conda-badge]][conda-link]
[![PyPI platforms][pypi-platforms]][pypi-link]

[![GitHub Discussion][github-discussions-badge]][github-discussions-link]
[![Gitter][gitter-badge]][gitter-link]
{% if cookiecutter.org == "Scikit-HEP" -%}
[![Scikit-HEP][sk-badge]](https://scikit-hep.org/)
{%- endif %}



[actions-badge]:            {{cookiecutter.url}}/workflows/CI/badge.svg
[actions-link]:             {{cookiecutter.url}}actions
[black-badge]:              https://img.shields.io/badge/code%20style-black-000000.svg
[black-link]:               https://github.com/psf/black
[conda-badge]:              https://img.shields.io/conda/vn/conda-forge/{{cookiecutter.project_name}}
[conda-link]:               https://github.com/conda-forge/{{cookiecutter.project_name}}-feedstock
[github-discussions-badge]: https://img.shields.io/static/v1?label=Discussions&message=Ask&color=blue&logo=github
[github-discussions-link]:  {{cookiecutter.url}}/discussions
[gitter-badge]:             https://badges.gitter.im/{{cookiecutter.url}}/community.svg
[gitter-link]:              https://gitter.im/{{cookiecutter.url}}/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge
[pypi-link]:                https://pypi.org/project/{{cookiecutter.project_name}}/
[pypi-platforms]:           https://img.shields.io/pypi/pyversions/{{cookiecutter.project_name}}
[pypi-version]:             https://badge.fury.io/py/{{cookiecutter.project_name}}.svg
[rtd-badge]:                https://readthedocs.org/projects/{{cookiecutter.project_name}}/badge/?version=latest
[rtd-link]:                 https://{{cookiecutter.project_name}}.readthedocs.io/en/latest/?badge=latest
[sk-badge]:                 https://scikit-hep.org/assets/images/Scikit--HEP-Project-blue.svg
