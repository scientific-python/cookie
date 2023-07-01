---
layout: page
title: Simple packaging
permalink: /guides/packaging-simple/
nav_order: 5
parent: Topical Guides
---

{% include toc.html %}

# Simple packaging

Python packages without binary extensions and fairly simple builds can use a
modern build system instead of the classic but verbose setuptools and
`setup.py`. The one you select doesn't really matter that much; they all use a
[standard configuration language][metadata] introduced in [PEP 621][]. The
PyPA's Flit is a great option. [scikit-build-core][] and [meson-python][] are
being developed to support this sort of configuration, enabling binary extension
packages to benefit too. These [PEP 621][] tools currently include [Hatch][],
[PDM][], [Flit][], [Trampolim][], [Whey][], and [Setuptools][]. [Poetry][] will
eventually gain support in 2.0.

Binaries mostly are unsupported in existing PEP 621 tools, though better support
is coming.

{: .note-title }

> Classic files
>
> These systems do not use or require `setup.py`, `setup.cfg`, or `MANIFEST.in`.
> Those are for setuptools. Unless you are using setuptools, of course, which
> still uses `MANIFEST.in`. You can convert the old files using
> `pipx run hatch new --init` or with
> [ini2toml](https://ini2toml.readthedocs.io/en/latest/).

{: .highlight-title }

> Selecting a backend
>
> Backends handle metadata the same way, so the choice comes down to how you
> specify what files go into an SDist and extra features, like getting a version
> from VCS. If you don't have an existing preference, hatchling is an excellent
> choice, balancing speed, configurability, and extendability.

## pyproject.toml: build-system

{% include rr.html id="PY001" %} Packages must have a `pyproject.toml` file
{% include rr.html id="PP001" %} that selects the backend:

{% tabs %} {% tab hatch Hatchling %}

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

{% endtab %} {% tab flit Flit-core %}

```toml
[build-system]
requires = ["flit_core>=3.3"]
build-backend = "flit_core.buildapi"
```

{% endtab %} {% tab pdm PDM-backend %}

```toml
[build-system]
requires = ["pdm-backend"]
build-backend = "pdm.backend"
```

{% endtab %} {% tab setuptools Setuptools %}

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"
```

{% endtab %} {% endtabs %}

## pyproject.toml: project

The metadata is specified in a [standards-based][metadata] format:

```toml
[project]
name = "package"
description = "A great package."
readme = "README.md"
authors = [
  { name = "My Name", email = "me@email.com" },
]
maintainers = [
  { name = "My Organization", email = "myemail@email.com" },
]
requires-python = ">=3.8"

dependencies = [
  "numpy>=1.13.3",
]

classifiers = [
  "Development Status :: 4 - Beta",
  "License :: OSI Approved :: BSD License",
  "Programming Language :: Python :: 3 :: Only",
  "Programming Language :: Python :: 3.8",
  "Programming Language :: Python :: 3.9",
  "Programming Language :: Python :: 3.10",
  "Programming Language :: Python :: 3.11",
  "Programming Language :: Python :: 3.12",
  "Topic :: Scientific/Engineering :: Physics",
]

[project.urls]
Homepage = "https://github.com/organization/package"
Documentation = "https://package.readthedocs.io/"
"Bug Tracker" = "https://github.com/organization/package/issues"
Discussions = "https://github.com/organization/package/discussions"
Changelog = "https://package.readthedocs.io/en/latest/changelog.html"
```

You can read more about each field, and all allowed fields, in
[packaging.python.org][metadata],
[Flit](https://flit.readthedocs.io/en/latest/pyproject_toml.html#new-style-metadata)
or [Whey](https://whey.readthedocs.io/en/latest/configuration.html). Note that
"Homepage" is special, and replaces the old url setting.

## Package structure

All packages _should_ have a `src` folder, with the package code residing inside
it, such as `src/<package>/`. This may seem like extra hassle; after all, you
can type "`python`" in the main directory and avoid installing it if you don't
have a `src` folder! However, this is a bad practice, and it causes several
common bugs, such as running `pytest` and getting the local version instead of
the installed version - this obviously tends to break if you build parts of the
library or if you access package metadata.

This sadly is not part of the standard metadata in `[project]`, so it depends on
what backend you you use. Hatchling, Flit, PDM, and setuptools use automatic
detection, while Trampolim and whey do not, requiring a `tool` setting.

If you don't match your package name and import name (which you should except
for very special cases), you will likely need extra configuration here.

You should have a `README` {% include rr.html id="PY002" %} and a `LICENSE` {%
include rr.html id="PY003" %} file. You should have a `docs/` folder {% include
rr.html id="PY003" %}. You should have a `/tests` folder (recommended) and/or a
`src/<package>/tests` folder.

## Versioning

You can specify the version manually (as shown in the example), but the backends
usually provide some automatic features to help you avoid this. Flit will pull
this from a file if you ask it to. Hatchling and PDM can be instructed to look
in a file or use git.

You will always need to specify that the version will be supplied dynamically
with:

```toml
dynamic = ["version"]
```

Then you'll configure your backend to compute the version.

{% details Hatchling dynamic versioning %}

You can tell hatchling to get the version from VCS. Add `hatch-vcs` to your
`build-backend.requires`, then add the following configuration:

```toml
[tool.hatch]
version.source = "vcs"
build.hooks.vcs.version-file = "src/<package>/version.py"
```

Or you can tell it to look for it in a file (see docs for arbitrary regex's):

```toml
[tool.hatch]
version.path = "src/<package>/__init__.py"
```

(replace `<package>` with the package path).

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
support versioning.

{% enddetails %}

## Including/excluding files in the SDist

This is tool specific.

- [Hatchling info here](https://hatch.pypa.io/latest/config/build/#file-selection).
  Hatchling uses your VCS ignore file by default, so make sure it is accurate
  (which is a good idea anyway).
- [Flit info here](https://flit.readthedocs.io/en/latest/pyproject_toml.html#sdist-section).
  Flit requires manual inclusion/exclusion in many cases, like using a dirty
  working directory.
- [PDM info here](https://pdm.fming.dev/pyproject/tool-pdm/#include-and-exclude-package-files).
- Setuptools still uses `MANIFEST.in`.

{: .warning }

> Flit will not use VCS (like git) to populate the SDist if you use standard
> tooling, even if it can do that using its own tooling. So make sure you list
> explicit include/exclude rules, and test the contents:
>
> ```bash
> # Show SDist contents
> tar -tvf dist/*.tar.gz
> # Show wheel contents
> unzip -l dist/*.whl
> ```

## Extras

It is recommended to use extras instead of or in addition to making requirement
files. These extras a) correctly interact with install requires and other
built-in tools, b) are available directly when installing via PyPI, and c) are
allowed in `requirements.txt`, `install_requires`, `pyproject.toml`, and most
other places requirements are passed.

Here is an example of a simple extras:

```toml
[project.optional-dependencies]
test = [
  "pytest >=6.0",
]
mpl = [
  "matplotlib >=2.0",
]
```

Self dependencies can be used by using the name of the package, such as
`dev = ["package[test,examples]"]`, but this requires Pip 21.2 or newer. We
recommend providing at least `test` and `docs`.

## Command line

If you want to ship an "app" that a user can run from the command line, you need
to add a `script` entry point. The form is:

```toml
[project.scripts]
cliapp = "packakge.__main__:main"
```

The format is command line app name as the key, and the value is the path to the
function, followed by a colon, then the function to call. If you use
`__main__.py` as the file, then `python -m` + the module will also work to call
the app.

[flit]: https://flit.readthedocs.io
[poetry]: https://python-poetry.org
[pdm]: https://pdm.fming.dev
[trampolim]: https://github.com/FFY00/trampolim
[whey]: https://whey.readthedocs.io
[hatch]: https://hatch.pypa.io/latest
[setuptools]: https://setuptools.readthedocs.io
[pep 621]: https://www.python.org/dev/peps/pep-0621
[metadata]: https://packaging.python.org/en/latest/specifications/core-metadata/
[scikit-build-core]: https://scikit-build-core.readthedocs.io
[meson-python]: https://meson-python.readthedocs.io

<script src="{% link assets/js/tabs.js %}"></script>
