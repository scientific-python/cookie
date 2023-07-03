---
layout: page
title: Classic packaging
permalink: /guides/packaging-classic/
nav_order: 7
parent: Topical Guides
---

{% include toc.html %}

# Classic packaging

The libraries in the scientific Python ecosytem have a variety of different
packaging styles, but this document is intended to outline a recommended style
that new packages should follow, and existing packages should slowly adopt. The
reasoning for each decision is outlined as well.

There are currently several popular packaging systems. This guide covers
[Setuptools][], which is currently the only system that supports compiled
extensions. If you are not planning on writing C/C++ code, other systems like
[Hatch][] are drastically simpler - most of this page is unneeded for those
systems.

Also see the [Python packaging guide][], especially the [Python packaging
tutorial][].

{: .note }

> Raw source lives in git and has a `setup.py`. You _can_ install directly from
> git via pip, but normally users install from distributions hosted on PyPI.
> There are three options: **A)** A source package, called an SDist and has a
> name that ends in `.tar.gz`. This is a copy of the GitHub repository, stripped
> of a few specifics like CI files, and possibly with submodules included (if
> there are any). **B)** A pure python wheel, which ends in `.whl`; this is only
> possible if there are no compiled extensions in the library. This does _not_
> contain a setup.py, but rather a `PKG_INFO` file that is rendered from
> setup.py (or from another build system). **C)** If not pure Python, a
> collection of wheels for every binary platform, generally one per supported
> Python version and OS as well.
>
> Developer requirements (users of A or git) are generally higher than the
> requirements to use B or C. Poetry and optionally flit create SDists that
> include a `setup.py`, and all alternate packing systems produce "normal"
> wheels.

## Package structure (medium priority)

All packages _should_ have a `src` folder, with the package code residing inside
it, such as `src/<package>/`. This may seem like extra hassle; after all, you
can type "`python`" in the main directory and avoid installing it if you don't
have a `src` folder! However, this is a bad practice, and it causes several
common bugs, such as running `pytest` and getting the local version instead of
the installed version - this obviously tends to break if you build parts of the
library or if you access package metadata.

## PEP 517/518 support (high priority)

Packages should provide a `pyproject.toml` file that _at least_ looks like this:

```toml
[build-system]
requires = ["setuptools>=42"]
build-backend = "setuptools.build_meta"
```

This completely changes your build process if you have Pip 10 or later (you can
disable it with `--no-build-isolation` in special cases, like when writing
custom conda-forge recipes). When this file is present, Pip creates a virtual
environment, installs exactly what it sees here, then builds a wheel (as
described in PEP 518). It then discards that environment, and installs the
wheel. This **a)** makes the build process reproducible and **b)** makes local
developer installs match the standard install procedure. Also, **c)** the build
requirements do not leak into the dev or install environments -- you do not need
to have `wheel` installed in your dev environment, for example - setuptools
declares it needs it via PEP 517 (and only when building wheels!). It also
**d)** allows complete specification of the environment that `setup.py` runs in,
so you can add packages that can be imported in `setup.py`. You should _not_ be
using `setup_requires`; it does not work properly and is deprecated. If you want
to have source builds that work in Pip 9 or earlier (not common), you should
have dev instructions on how to install requirements needed to run `setup.py`.

You can also use this to select your entire build system; we use setuptools
above but you can also use others, such as [Flit][] or [Poetry][]. This is
possible due to the `build-backend` selection, as described in PEP 517.
Scientific Python packages don't often use these since they usually do not allow
binary packages to be created and a few common developer needs, like editable
installs, look slightly different (a way to include editable installs in PEP 517
is being worked on). Usage of these "[hypermodern][]" packaging tools are
generally not found in scientific Python packages, but not discouraged; all
tools build the same wheels (and they often build setuptools compliant SDists,
as well).

{% rr PP003 %} Note that `"wheel"` is never required; it is injected
automatically by setuptools only when needed.

### Special additions: NumPy

You may want to build against NumPy (mostly for Cython packages, pybind11 does
not need to access the NumPy headers). This is the recommendation for scientific
Python packages:

```toml
requires = [
    "oldest-supported-numpy",
```

This ensures the wheels built work with all versions of NumPy supported by your
package. Whether you build the wheel locally or on CI, you can transfer it to
someone else and it will work on any supported NumPy. The
`oldest-supported-numpy` package is a SciPy metapackage from the NumPy
developers that tracks the
[correct version of NumPy to build wheels against for each version of Python and for each OS/implementation](https://github.com/scipy/oldest-supported-numpy/blob/master/setup.cfg).
Otherwise, you would have to list the earliest version of NumPy that had support
for each Python version here.

## Versioning (medium/high priority)

Scientific Python packages should use one of the following systems:

### Git tags: official PyPA method

One more section is very useful in your `pyproject.toml` file:

```toml
requires = [
    "setuptools>=42",
    "setuptools_scm[toml]>=3.4",
    # ...
]

[tool.setuptools_scm]
write_to = "src/<package>/_version.py"
```

This will write a version file when you build from the GitHub repository. You
get the following benefits:

- No manual file to change with the version number - always in sync with Git
  - Simpler release procedure
  - No more mistakes / confusion
  - You can force a version with an environment variable
    `SETUPTOOLS_SCM_PRETEND_VERSION` without source code changes.
- A new version every commit (both commits since last tag and git hash encoded)
  - Binaries no longer incorrectly "cache" when installing from pip directly
    from git
  - You can always tell the exact commit of every sdist/wheel/install
  - If your working directory is "dirty" (changes/new files that are not
    ignored), you will get a version that indicates this.
- SDists and wheels contain the version file/number just like normal
  - Note that reading the version number for the SDist requires `setuptools_scm`
    and `toml` unless you add a workaround to `setup.py`. This is not required
    for wheels (`setup.py` is not even part of a wheel).

If you want to set a template, you can control the details of this file if
needed for historical compatibility, but it is better for new/young projects to
use the default layout and include this in your `__init__.py`:

```python
from ._version import version as __version__
```

In docs, there are a few minor tweaks necessary to make sure the version is
picked up correctly; just make sure you install the package and access it from
there.

The one place where the pep518 requirements do not get picked up is when you
manually run `setup.py`, such as when doing `python setup.py sdist` [^1]. If you
are missing `setuptools_scm` or possibly the `toml` dependency on old versions
of `setuptools_scm`, you will silently get version 0.0.0. To make this a much
more helpful error, add this to your `setup.py`:

```python
import setuptools_scm  # noqa: F401
```

If you want to create artifacts for use in-between versions, then you should
disable shallow checkouts in your CI, since a non-tagged version cannot be
computed correctly from a checkout that is too shallow. For GitHub Actions, use
`actions/checkout@v2` and `with: fetch-depth: 0`.

For GitHub actions, you can add a few lines that will enable you to manually
trigger builds with custom versions:

{% raw %}

```yaml
on:
  workflow_dispatch:
    inputs:
      overrideVersion:
        description: Manually force a version
env:
  SETUPTOOLS_SCM_PRETEND_VERSION: ${{ github.event.inputs.overrideVersion }}
```

{% endraw %}

If you fill in the override version setting when triggering a manual workflow
run, that version will be forced, otherwise, it works as normal.

{: .note }

> Make sure you have a good gitignore, probably starting from
> [GitHub's Python one](https://github.com/github/gitignore/blob/main/Python.gitignore)
> or using a [generator site](https://www.toptal.com/developers/gitignore).

You should also add these two files:

`.git_archival.txt`:

```text
node: $Format:%H$
node-date: $Format:%cI$
describe-name: $Format:%(describe:tags=true,match=*[0-9]*)$
ref-names: $Format:%D$
```

And `.gitattributes` (or add this line if you are already using this file):

```text
.git_archival.txt  export-subst
```

This will allow git archives (including the ones generated from GitHub) to also
support versioning. This will only work with `setuptools_scm>=7` (though adding
the files won't hurt older versions).

### Classic in-source versioning

Recent versions of `setuptools` have improved in-source versioning. If you have
a simple file that includes a line with a simple PEP 440 style version, like
`version = "2.3.4.beta1"`, then you can use a line like this in your
`setup.cfg`:

```ini
[metadata]
version = attr: package._version.version
```

Setuptools will look in the AST of `_verison.py` for a simple assignment; if
that works, it will not actually import your package during the setup phase
(which is bad). Older versions of setuptools or complex version files will
import your package; if it is not importable with the pyproject.toml
requirements only, this will fail.

Flit will always look for `package.__version__`, and so will always import your
package; you just have to deal with that if you use Flit.

## Setup configuration (medium priority)

You should put as much as possible in your `setup.cfg`, and leave `setup.py` for
_only_ parts that need custom logic or binary building. This keeps your
`setup.py` cleaner, and many things that normally require a bit of custom code
can be written without it, such as importing version and descriptions. [The
official docs are excellent for setup.cfg][setuptools cfg]. Here's a practical
example:

```ini
[metadata]
name = package
description = A great package.
long_description = file: README.md
long_description_content_type = text/markdown
url = https://github.com/organization/package
author = My Name
author_email = me@email.com
maintainer = My Organization
maintainer_email = organization@email.com
license = BSD-3-Clause
license_files = LICENSE
classifiers =
    Development Status :: 4 - Beta
    Intended Audience :: Developers
    Intended Audience :: Information Technology
    Intended Audience :: Science/Research
    License :: OSI Approved :: BSD License
    Operating System :: MacOS
    Operating System :: Microsoft :: Windows
    Operating System :: POSIX
    Operating System :: Unix
    Programming Language :: C++
    Programming Language :: Python
    Programming Language :: Python :: 3 :: Only
    Programming Language :: Python :: 3.8
    Programming Language :: Python :: 3.9
    Programming Language :: Python :: 3.10
    Programming Language :: Python :: 3.11
    Programming Language :: Python :: 3.12
    Topic :: Scientific/Engineering
    Topic :: Scientific/Engineering :: Information Analysis
    Topic :: Scientific/Engineering :: Mathematics
    Topic :: Scientific/Engineering :: Physics
    Topic :: Software Development
    Topic :: Utilities
project_urls =
    Documentation = https://package.readthedocs.io/
    Bug Tracker = https://github.com/organization/package/issues
    Discussions = https://github.com/organization/package/discussions
    Changelog = https://package.readthedocs.io/en/latest/changelog.html


[options]
packages = find:
install_requires =
    numpy>=1.13.3
python_requires = >=3.8
include_package_data = True
package_dir =
    =src
zip_safe = False

[options.packages.find]
where = src
# Not needed unless not following the src layout
# exclude =
#     tests
#     extern
```

And, a possible `setup.py`; though in recent versions of pip, there no longer is
a need to include a legacy `setup.py` file, even for editable installs, unless
you are building extensions.

```python
#!/usr/bin/env python
# Copyright (c) 2020, My Name
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/organization/package for details.

from setuptools import setup

setup()
```

Note that we do not recommend overriding or changing the behavior of
`python setup.py test` or `python setup.py pytest`; the test command through
`setup.py` is deprecated and discouraged - anything that directly calls
`setup.py` assumes a `setup.py` is present, which is not true for [Flit][]
packages and other systems.[^2] Instead, assume users call `pytest` directly, or
use `nox`.

If you need to have custom package data, such as data stored in one place in the
SDist structure that shows up in another place in the package, then replace
`include_package_data` with an `options.package_data` section and a mapping.

With the exception of flake8, all package configuration should be possible via
`pyproject.toml`, such as pytest (6+):

```toml
[tool.pytest]
junit_family = "xunit2"
testpaths = ["tests"]
```

## Extras (low/medium priority)

It is recommended to use extras instead of or in addition to making requirement
files. These extras a) correctly interact with install requires and other
built-in tools, b) are available directly when installing via PyPI, and c) are
allowed in `requirements.txt`, `install_requires`, `pyproject.toml`, and most
other places requirements are passed.

Here is an example of a simple extras, placed in `setup.cfg` for a package
called `package`:

```ini
[options.extras_require]
test =
  pytest >=6.0
mpl =
  matplotlib >=2.0
```

And a complex one, that does some logic (like combining the requirements into an
"all" extra), placed in `setup.py`:

```python
extras = {
    "test": ["pytest"],
    "docs": [
        "Sphinx>=2.0.0",
        "recommonmark>=0.5.0",
        "sphinx_rtd_theme",
        "nbsphinx",
        "sphinx_copybutton",
    ],
    "examples": ["matplotlib", "numba"],
    "dev": ["pytest-sugar", "ipykernel"],
}
extras["all"] = sum(extras.values(), [])

setup(extras_require=extras)
```

Self dependencies can be placed in `setup.cfg` using the name of the package,
such as `dev = package[test,examples]`, but this requires Pip 21.2 or newer. We
recommend providing at least `test`, `docs`, and `dev`.

## Including/excluding files in the SDist

Python packaging goes through a 3-stage procedure if you have the above
recommended `pyproject.toml` file. If you type `pip install .`, then

1. Source is processed to make an SDist (in a virtual environment mandated by
   pyproject.toml).
2. SDist is processed to make a wheel (same virtual environment).
3. The wheel is installed.

The wheel does _not_ contain `setup.*`, `pyproject.toml`, or other build code.
It simply is a `.tar.gz` file that is named `.whl` and has a simple mapping of
directories to installation paths and a generic metadata format. "Installing"
really is just copying files around, and pip also pre-compiles some bytecode for
you while doing so.

If you don't have a `MANIFEST.in`, the "legacy" build procedure will skip the
SDist step, making it possible for a development build to work while a published
PyPI SDist could fail. Also, development mode (`-e`) is not covered by this
procedure, so you should have at least one CI run that does not include the `-e`
(pip 21.3+ required for non-setuptools editable installs).

The files that go into the SDist are controlled by [MANIFEST.in][], which
generally should be specified. If you use `setuptools_scm`, the [default should
be all of git][setuptools_scm file]; if you do not, the default is a few common
files, like any `.py` files and standard tooling. Here is a useful default,
though be sure to update it to include any files that need to be included:

```
graft src
graft tests

include LICENSE README.md pyproject.toml setup.py setup.cfg
global-exclude __pycache__ *.py[cod] .venv
```

## Command line

If you want to ship an "app" that a user can run from the command line, you need
to add a `console_scripts` entry point. The form is:

```ini
[options.entry_points]
console_scripts =
    cliapp = packakge.__main__:main
```

The format is command line app name as the key, and the value is the path to the
function, followed by a colon, then the function to call. If you use
`__main__.py` as the file, then `python -m` + the module will also work to call
the app.

[^1]:
    You shouldn't ever have to run commands like this, they are implementation
    details of setuptools. For this command, you should use `python -m build -s`
    instead (and `pip install build`).

[^2]:
    Actually, Flit produces a backward-compatible `setup.py` by default when
    making an SDist - it's only "missing" from the GitHub repository. This
    default behavior is changing, though, as there's much less reason today to
    have a legacy `setup.py`.

<!-- prettier-ignore-start -->

[flit]: https://flit.readthedocs.io
[poetry]: https://python-poetry.org
[hatch]: https://hatch.pypa.io
[hypermodern]: https://cjolowicz.github.io/posts/hypermodern-python-01-setup/
[setuptools_scm file]: https://github.com/pypa/setuptools_scm/#file-finders-hook-makes-most-of-manifestin-unnecessary
[manifest.in]: https://packaging.python.org/guides/using-manifest-in/
[setuptools]: https://setuptools.readthedocs.io/en/latest/userguide/index.html
[setuptools cfg]: https://setuptools.readthedocs.io/en/latest/userguide/declarative_config.html
[python packaging guide]: https://packaging.python.org
[python packaging tutorial]: https://packaging.python.org/tutorials/packaging-projects/

<!-- prettier-ignore-end -->
