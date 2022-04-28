# Scikit-HEP: cookie

[![Actions Status][actions-badge]][actions-link]
[![Code style: black][black-badge]][black-link]

[![GitHub Discussion][github-discussions-badge]][github-discussions-link]
[![Gitter][gitter-badge]][gitter-link]
[![Scikit-HEP][sk-badge]](https://scikit-hep.org/)

A cookiecutter template for new Python projects, either targeting Scikit-HEP
inclusion, or for general software packages - the only Scikit-HEP specific
parts are in the defaults. What makes this different from other cookie cutter
templates for Python packages?

* Designed from the [Scikit-HEP developer guidelines][]: Every decision is
  clearly documented and every tool described.
* Template generation tested in GitHub Actions using nox.
* Eleven different backends to choose from for building packages.
* Includes a backend for C++ bindings using pybind11, with wheels produced for
  all platforms using cibuildwheel.
* Follows PyPA best practices.

Be sure you have read the [Scikit-HEP developer guidelines][] first, and
possibly used them on a project or two. This is _not_ a minimal example
or tutorial. It is a collection of useful tooling for starting a new project
using cookiecutter, or for copying in individual files for an existing project
(by hand, from `{{cookiecutter.project_name}}/`).

During generation you can select from the following backends for your package:

1. [setuptools][]: The classic build system. Most powerful, but high learning curve
   and lots of configuration required.
2. [setuptools621][setuptools]: The classic build system, but with the new standardized
   configuration. EXPERIMENTAL.
3. [pybind11][]: This is setuptools but with an C++ extension written in [pybind11][]
   and wheels generated by [cibuildwheel][].
4. [scikit-build][]: A scikit-build (CMake) project also using pybind11, wraps
   setuptools currently.
5. [poetry][]: An all-in-one solution to pure Python projects. Replaces
   setuptools, venv/pipenv, pip, wheel, and twine. Higher learning curve, but
   is all-in-one. Makes some bad default assumptions for libraries.
6. [flit][]: A modern, lightweight [PEP 621][] build system for pure Python
   projects. Replaces setuptools, no MANIFEST.in, setup.py, or setup.cfg. Low
   learning curve. Easy to bootstrap into new distributions.
7. [pdm][]: A modern, less opinionated all-in-one solution to pure Python
   projects supporting standards. Replaces setuptools, venv/pipenv, pip, wheel,
   and twine. Supports [PEP 621][], and also the unaccepted [PEP 582][].
8. [trampolim][]: A modern [PEP 621][] builder with support for tasks, allowing
   arbitrary Python to run during the build process if needed.
9. [whey][]: A modern [PEP 621][] builder with some automation options for Trove
   classifiers. Development seems to be stalled, possibly.
10. [maturin][]: A [PEP 621][] builder for Rust binary extensions. 
11. [hatch][]: A package manager similar to Poetry/PDM. Hatchling (the backend) is
   a modern builder with nice error messages.
   
Currently, the best choices are probably flit, PDM, or hatch for pure Python projects,
and setuptools (such as the pybind11 choice) for binary projects.

#### To use:

Install cookiecutter, ideally with `brew install cookiecutter` if you use brew,
otherwise with `pipx install cookiecutter` (or prepend `pipx run` to the
command below, and skip installation). Then run:


```bash
cookiecutter gh:scikit-hep/cookie
```

Answer all the questions. If you are not making a Scikit-HEP repo, just enter a
different org name. (You can also use `pipx run cookiecutter` without installing).

Check the key setup files, `pyproject.toml`, and possibly `setup.cfg` and
`setup.py` (pybind11 example). Update README.md. Also update and add docs to
`docs/`.

There are a few example dependencies and a minimum Python version of 3.7,
feel free to change it to whatever you actually need/want.

#### Contained components:

* GitHub Actions runs testing for the generation itself
    - Uses nox so cookie development can be checked locally
* GitHub actions deploy
    - Be sure to add a token
    - C++ backend uses cibuildwheel for wheel builds
* Dependabot keeps actions up to date periodically, through useful pull requests
* Formatting handled by pre-commit
    - No reason not to be strict on a new project; remove what you don't want.
    - Includes MyPy - static typing
    - Includes strong Flake8 checking
    - Includes auto fixes for common flake8 problems
    - Includes Black - standardizing formatting
    - Includes isort for nice import sorting/grouping
    - Includes PyUpgrade - keeps old Python syntax out
    - Includes spell checking
* An pylint nox target can be used to run pylint, which integrated GHA annotations
* A ReadTheDocs-ready Sphinx docs folder and `[docs]` extra
* A test folder and pytest `[test]` extra
* A noxfile is included with a few common targets

Setuptools only:

* Setuptools controlled by `setup.cfg` and a nominal `setup.py`.
    - Using declarative syntax avoids needless boilerplate that is often wrong
      (like incorrectly handling the encoding when opening a README).
    - Easier to adapt to PEP 621 eventually.
    - Any actual logic can sit in setup.py and be clearly separate from simple
      metadata.
* Versioning handled by `setuptools_scm`
    - You can easily switch to manual versioning, but this avoids duplicating
      the version as git tags and in the source, and versions _every_ commit
      uniquely, sidestepping some caching problems.
* `MANIFEST.in` checked with check-manifest
* `setup.cfg` checked by setup-cfg-fmt


#### For developers:

You can test locally with [nox][]:

```console
# See all commands
nox -l

# Run all tests and checks (takes several minutes)
nox

# Run a specific check
nox -s "lint(setuptools)"

# Run a noxfile command on the project noxfile
nox -s "nox(whey)" -- docs
```

If you don't have `nox` locally, you can use [pipx][], such as `pipx run nox` instead.

#### Other similar projects

[Hypermodern-Python][hypermodern] is another project worth checking out
with many similarities, like great documentation for each feature and
many of the same tools used. It has a slightly different set of features,
and has a stronger focus on GitHub Actions - most of Scikit-HEP cookie
could be adapted to a different CI system fairly easily if you don't want
to use GHA. It also forces the use of Poetry (instead of having a backend
selection), and doesn't support compiled projects. It currently dumps all
development depndenices into a shared environment, causing long solve times
and high chance of conflicts. It also does not use pre-commit properly. It
also has quite a bit of custom code.

[actions-badge]:            https://github.com/scikit-hep/cookie/workflows/CI/badge.svg
[actions-link]:             https://github.com/scikit-hep/cookie/actions
[black-badge]:              https://img.shields.io/badge/code%20style-black-000000.svg
[black-link]:               https://github.com/psf/black
[conda-badge]:              https://img.shields.io/conda/vn/conda-forge/cookie
[conda-link]:               https://github.com/conda-forge/cookie-feedstock
[github-discussions-badge]: https://img.shields.io/static/v1?label=Discussions&message=Ask&color=blue&logo=github
[github-discussions-link]:  https://github.com/scikit-hep/cookie/discussions
[gitter-badge]:             https://badges.gitter.im/Scikit-HEP/community.svg
[gitter-link]:              https://gitter.im/Scikit-HEP/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge
[sk-badge]:                 https://scikit-hep.org/assets/images/Scikit--HEP-Project-blue.svg

[Scikit-HEP developer guidelines]: https://scikit-hep.org/developer

[cibuildwheel]: https://cibuildwheel.readthedocs.io/en/stable/
[scikit-build]: https://scikit-build.readthedocs.io/en/latest/
[flit]:         https://flit.readthedocs.io/en/latest/
[nox]:          https://nox.thea.codes/en/stable/
[pdm]:          https://pdm.fming.dev
[poetry]:       https://python-poetry.org
[pybind11]:     https://pybind11.readthedocs.io/en/stable/
[setuptools]:   https://setuptools.readthedocs.io/en/latest/
[trampolim]:    https://trampolim.readthedocs.io/en/latest/
[pipx]:         https://pypa.github.io/pipx/
[whey]:         https://whey.readthedocs.io/en/latest/
[maturin]:      https://maturin.rs
[hypermodern]:  https://github.com/cjolowicz/cookiecutter-hypermodern-python
[hatch]:        https://github.com/ofek/hatch

[PEP 582]: https://www.python.org/dev/peps/pep-0582
[PEP 621]: https://www.python.org/dev/peps/pep-0621
