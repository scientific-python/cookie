# Scientific Python: cookie

[![Actions Status][actions-badge]][actions-link]
[![GitHub Discussion][github-discussions-badge]][github-discussions-link]
[![Live ReadTheDocs][rtd-badge]][rtd-link]

[![PyPI version][pypi-version]][pypi-link]
[![PyPI platforms][pypi-platforms]][pypi-link]

A [copier][]/[cookiecutter][] template for new Python projects based on the
Scientific Python Developer Guide. What makes this different from other
templates for Python packages?

- Lives with the [Scientific-Python Development Guide][]: Every decision is
  clearly documented and every tool described, and everything is kept in sync.
- Twelve different backends to choose from for building packages.
- Template generation tested in GitHub Actions using nox.
- Supports generation with [copier][], [cookiecutter][], and [cruft][].
- Includes several compiled backends using [pybind11][], with wheels produced
  for all platforms using [cibuildwheel][].
- Provides [`sp-repo-review`][pypi-link] to evaluate existing repos against the
  guidelines, with a WebAssembly version integrated with the guide. All checks
  cross-linked.
- Follows [PyPA][] best practices and regularly updated.

Be sure you have read the [Scientific-Python Development Guide][] first, and
possibly used them on a project or two. This is _not_ a minimal example or
tutorial. It is a collection of useful tooling for starting a new project using
cookiecutter, or for copying in individual files for an existing project (by
hand, from `{{cookiecutter.project_name}}/`).

During generation you can select from the following backends for your package:

1. [hatch][]: This uses hatchling, a modern builder with nice file inclusion,
   extendable via plugins, and good error messages. **(Recommended for pure
   Python projects)**
2. [flit][]: A modern, lightweight [PEP 621][] build system for pure Python
   projects. Replaces setuptools, no MANIFEST.in, setup.py, or setup.cfg. Low
   learning curve. Easy to bootstrap into new distributions. Difficult to get
   the right files included, little dynamic metadata support.
3. [pdm][]: A modern, less opinionated all-in-one solution to pure Python
   projects supporting standards. Replaces setuptools, venv/pipenv, pip, wheel,
   and twine. Supports [PEP 621][].
4. [trampolim][]: A modern [PEP 621][] builder with support for tasks, allowing
   arbitrary Python to run during the build process if needed.
5. [whey][]: A modern [PEP 621][] builder with some automation options for Trove
   classifiers. Development seems to be stalled, possibly.
6. [poetry][]: An all-in-one solution to pure Python projects. Replaces
   setuptools, venv/pipenv, pip, wheel, and twine. Higher learning curve, but is
   all-in-one. Makes some bad default assumptions for libraries. The only one
   with a non-standard pyproject.toml config.
7. [setuptools621][setuptools]: The classic build system, but with the new
   standardized configuration.
8. [setuptools][]: The classic build system. Most powerful, but high learning
   curve and lots of configuration required.
9. [pybind11][]: This is setuptools but with an C++ extension written in
   [pybind11][] and wheels generated by [cibuildwheel][].
10. [scikit-build][]: A scikit-build (CMake) project also using pybind11, using
    scikit-build-core. **(Recommended for C++ projects)**
11. [meson-python][]: A Meson project also using pybind11.
12. [maturin][]: A [PEP 621][] builder for Rust binary extensions.
    **(Recommended for Rust projects)**

Currently, the best choice is probably hatch for pure Python projects, and
setuptools (such as the pybind11 choice) for binary projects.

#### To use (modern copier version)

Install `copier` and `copier-templates-extensions`. Using [pipx][], that's:

```bash
pipx install copier
pipx inject copier copier-templates-extensions
```

Now, run copier to generate your project:

```bash
copier copy gh:scientific-python/cookie <pkg> --UNSAFE
```

(`<pkg>` is the path to put the new project.)

You will get a much, much nicer CLI experience with helpful descriptions and
answer validation. You will also get a `.copier-answers.yml` file, which will
allow you to perform updates in the future.

> Note: Add `--vcs-ref=HEAD` to get the latest version instead of the last
> tagged version; HEAD always passes tests (and is what cookiecutter uses).

#### To use (classic cookiecutter version)

Install cookiecutter, ideally with `brew install cookiecutter` if you use brew,
otherwise with `pipx install cookiecutter` (or prepend `pipx run` to the command
below, and skip installation). Then run:

```bash
cookiecutter gh:scientific-python/cookie
```

#### To use (classic cruft version)

You can also use [cruft][], which adds the ability update to cookiecutter
projects. Install with `pipx install cruft` (or prepend `pipx run` to the
command below, and skip installation). Then run:

```bash
cruft create gh:scientific-python/cookie
```

#### Post generation

Check the key setup files, `pyproject.toml`, and possibly `setup.cfg` and
`setup.py` (pybind11 example). Update `README.md`. Also update and add docs to
`docs/`.

There are a few example dependencies and a minimum Python version of 3.8, feel
free to change it to whatever you actually need/want. There is also a basic
backports structure with a small typing example.

#### Contained components:

- GitHub Actions runs testing for the generation itself
  - Uses nox so cookie development can be checked locally
- GitHub actions deploy
  - C++ backends include cibuildwheel for wheel builds
  - Uses PyPI trusted publisher deployment
- Dependabot keeps actions up to date periodically, through useful pull requests
- Formatting handled by pre-commit
  - No reason not to be strict on a new project; remove what you don't want.
  - Includes MyPy - static typing
  - Includes Black - standardizing formatting
  - Includes strong Ruff-based linting and autofixes
    - Replaces Flake8, isort, pyupgrade, yesqa, pycln, and dozens of plugins
  - Includes spell checking
- An pylint nox target can be used to run pylint, which integrated GHA
  annotations
- A ReadTheDocs-ready Sphinx docs folder and `[docs]` extra
- A test folder and pytest `[test]` extra
- A noxfile is included with a few common targets

Setuptools only:

- Setuptools controlled by `setup.cfg` and a nominal `setup.py`.
  - Using declarative syntax avoids needless boilerplate that is often wrong
    (like incorrectly handling the encoding when opening a README).
  - Easier to adapt to PEP 621 eventually.
  - Any actual logic can sit in setup.py and be clearly separate from simple
    metadata.
- Versioning handled by `setuptools_scm`
  - You can easily switch to manual versioning, but this avoids duplicating the
    version as git tags and in the source, and versions _every_ commit uniquely,
    sidestepping some caching problems.
- `MANIFEST.in` checked with check-manifest
- `setup.cfg` checked by setup-cfg-fmt

#### For developers:

You can test locally with [nox][]:

```console
# See all commands
nox -l

# Run a specific check
nox -s "lint(setuptools)"

# Run a noxfile command on the project noxfile
nox -s "nox(whey)" -- docs
```

If you don't have `nox` locally, you can use [pipx][], such as `pipx run nox`
instead.

#### Other similar projects

[Hypermodern-Python][hypermodern] is another project worth checking out with
many similarities, like great documentation for each feature and many of the
same tools used. It has a slightly different set of features, and has a stronger
focus on GitHub Actions - most our guide could be adapted to a different CI
system fairly easily if you don't want to use GHA. It also forces the use of
Poetry (instead of having a backend selection), and doesn't support compiled
projects. It currently dumps all development dependencies into a shared
environment, causing long solve times and high chance of conflicts. It also does
not use pre-commit the way it was intended to be used. It also has quite a bit
of custom code.

#### History

A lot of the guide, cookiecutter, and repo-review started out as part of
[Scikit-HEP][]. These projects were merged, generalized, and combined with the
[NSLS-II][] guide during the 2023 Scientific-Python Developers Summit.

<!-- prettier-ignore-start -->

[actions-badge]: https://github.com/scientific-python/cookie/workflows/CI/badge.svg
[actions-link]: https://github.com/scientific-python/cookie/actions
[cibuildwheel]: https://cibuildwheel.readthedocs.io
[cookiecutter]: https://cookiecutter.readthedocs.io
[copier]: https://copier.readthedocs.io
[cruft]: https://cruft.github.io/cruft
[flit]: https://flit.readthedocs.io/en/latest/
[github-discussions-badge]: https://img.shields.io/static/v1?label=Discussions&message=Ask&color=blue&logo=github
[github-discussions-link]: https://github.com/scientific-python/cookie/discussions
[hatch]: https://github.com/ofek/hatch
[hypermodern]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[maturin]: https://maturin.rs
[meson-python]: https://meson-python.readthedocs.io
[nox]: https://nox.thea.codes/en/stable/
[nsls-ii]: https://nsls-ii.github.io/scientific-python-cookiecutter/
[pdm]: https://pdm.fming.dev
[pep 621]: https://www.python.org/dev/peps/pep-0621
[pipx]: https://pypa.github.io/pipx/
[poetry]: https://python-poetry.org
[pybind11]: https://pybind11.readthedocs.io
[pypa]: https://www.pypa.io
[pypi-link]: https://pypi.org/project/sp-repo-review/
[pypi-platforms]: https://img.shields.io/pypi/pyversions/sp-repo-review
[pypi-version]: https://badge.fury.io/py/sp-repo-review.svg
[rtd-badge]: https://readthedocs.org/projects/scientific-python-cookie/badge/?version=latest
[rtd-link]: https://scientific-python-cookie.readthedocs.io/en/latest/?badge=latest
[scientific-python development guide]: https://learn.scientific-python.org/development
[scikit-build]: https://scikit-build.readthedocs.io
[scikit-hep]: https://scikit-hep.org
[setuptools]: https://setuptools.readthedocs.io
[trampolim]: https://trampolim.readthedocs.io
[whey]: https://whey.readthedocs.io

<!-- prettier-ignore-end -->
