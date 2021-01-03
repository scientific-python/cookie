# Scikit-HEP: template-py

[![Actions Status][actions-badge]][actions-link]
[![Documentation Status][rtd-badge]][rtd-link]
[![Code style: black][black-badge]][black-link]

[![PyPI version][pypi-version]][pypi-link]
[![Conda-Forge][conda-badge]][conda-link]
[![PyPI platforms][pypi-platforms]][pypi-link]

[![GitHub Discussion][github-discussions-badge]][github-discussions-link]
[![Gitter][gitter-badge]][gitter-link]
[![Scikit-HEP][sk-badge]](https://scikit-hep.org/)


Be sure you have read the Scikit-HEP developer guidelines first, and possibly used them on a project or two first. This is _not_ a minimal example or tutorial. It is a collection of useful tooling for starting a new project. You may want to remove some parts after duplicating the template. That's okay.

This is a pure python template project, using setuptools. If you are using flit or poetry, those have their own initialization tools; you can just copy the extra tooling in from this template repo. Do not fork this repo unless you want to propose a change to the template; instead use the large "template" button GitHub provides to make a new repo based on this one.

#### To use:

Clone with the GUI or use:


```bash
gh repo create my-project --template scikit-hep/template-py
```

Search and replace `template-py` and `template_py` with your project name. Rename the `src/template_py` folder as well.

Update the lines in `setup.cfg` and LICENSE with your information.

Replace README.md or update it significantly. Also update and add docs to `docs/`.

#### Contained components:

* Setuptools controlled by setup.cfg and a nominal setup.py.
    - Using declarative syntax avoids needless boilerplate that is often wrong (like incorrectly handling the encoding when opening a README).
    - Easier to adapt to PEP 621 eventually.
    - Any actually logic can sit in setup.py and be clearly separate from simple metadata.
* GitHub actions runs testing
    - Not using Tox because native testing is faster
* GitHub actions deploy
    - Be sure to add a token
* Dependabot keeps actions up to date periodically, through useful pull requests
* Versioning handled by `setuptools_scm`
    - You can easily switch to manual versioning, but this avoids duplicating the version as git tags and in the source, and versions _every_ commit uniquely, sidestepping some caching problems.
* Formatting handled by pre-commit
    - No reason not to be strict on a new project
    - Includes MyPy - static typing
    - Includes strong Flake8 checking
    - Includes auto fixes for most flake8 problems
    - Includes Black
* A rough version of ReadTheDocs Sphinx docs provided

[actions-badge]:            https://github.com/scikit-hep/template-py/workflows/CI/badge.svg
[actions-link]:             https://github.com/scikit-hep/template-py/actions
[black-badge]:              https://img.shields.io/badge/code%20style-black-000000.svg
[black-link]:               https://github.com/psf/black
[conda-badge]:              https://img.shields.io/conda/vn/conda-forge/template-py
[conda-link]:               https://github.com/conda-forge/template-py-feedstock
[github-discussions-badge]: https://img.shields.io/static/v1?label=Discussions&message=Ask&color=blue&logo=github
[github-discussions-link]:  https://github.com/scikit-hep/template-py/discussions
[gitter-badge]:             https://badges.gitter.im/Scikit-HEP/community.svg
[gitter-link]:              https://gitter.im/Scikit-HEP/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge
[pypi-link]:                https://pypi.org/project/template-py/
[pypi-platforms]:           https://img.shields.io/pypi/pyversions/template-py
[pypi-version]:             https://badge.fury.io/py/template-py.svg
[rtd-badge]:                https://readthedocs.org/projects/template-py/badge/?version=latest
[rtd-link]:                 https://template-py.readthedocs.io/en/latest/?badge=latest
[sk-badge]:                 https://scikit-hep.org/assets/images/Scikit--HEP-Project-blue.svg

