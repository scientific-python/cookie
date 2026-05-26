## pyproject.toml: project table

<!-- [[[cog
from cog_helpers import code_fence, render_cookie, TOMLMatcher
with render_cookie(backend="uv") as package:
    pyproject = TOMLMatcher.from_file(package / "pyproject.toml")
]]] -->
<!-- [[[end]]] -->

The metadata is specified in a [standards-based][metadata] format:

<!-- [[[cog
with code_fence("toml"):
    print(pyproject.get_source("project"))
]]] -->
<!-- prettier-ignore-start -->
```toml
[project]
name = "package"
version = "0.1.0"
authors = [
  { name = "My Name", email = "me@email.com" },
]
description = "A great package."
readme = "README.md"
license = "BSD-3-Clause"
license-files = ["LICENSE"]
requires-python = ">=3.10"
classifiers = [
  "Development Status :: 1 - Planning",
  "Intended Audience :: Science/Research",
  "Intended Audience :: Developers",
  "Operating System :: OS Independent",
  "Programming Language :: Python",
  "Programming Language :: Python :: 3",
  "Programming Language :: Python :: 3 :: Only",
  "Programming Language :: Python :: 3.10",
  "Programming Language :: Python :: 3.11",
  "Programming Language :: Python :: 3.12",
  "Programming Language :: Python :: 3.13",
  "Programming Language :: Python :: 3.14",
  "Topic :: Scientific/Engineering",
  "Typing :: Typed",
]
dependencies = []

[project.urls]
Homepage = "https://github.com/org/package"
"Bug Tracker" = "https://github.com/org/package/issues"
Discussions = "https://github.com/org/package/discussions"
Changelog = "https://github.com/org/package/releases"
```
<!-- prettier-ignore-end -->
<!-- [[[end]]] -->

In this example, `"package"` is the name of the thing you are working on. You
can read more about each field, and all allowed fields, in
[packaging.python.org][metadata],
[Flit](https://flit.readthedocs.io/en/latest/pyproject_toml.html#new-style-metadata)
or [Whey](https://whey.readthedocs.io/en/latest/configuration.html). Only the
`name` and `version` fields are strictly required. Note that "Homepage" is
special, and replaces the old url setting.

If you use the above configuration, you need `README.md` and `LICENSE` files,
since they are explicitly specified.

### License

The license can be done one of two ways.

The modern way is to use the `license` field and an [SPDX identifier
expression][spdx]. You can specify a list of files globs in `license-files`. You
need `hatchling>=1.26`, `flit-core>=1.11` (1.12 for complex license statements),
`pdm-backend>=2.4`, `setuptools>=77`, `meson-python>=0.18`, `maturin>=1.9.2`,
`poetry-core>=2.2`, or `scikit-build-core>=0.12` to support this. You can also
specify `license-files` as a list with globs for license files. If you don't,
most backends will discover common license file names by default.

The classic convention uses one or more [Trove Classifiers][] to specify the
license. There also was a `license.file` field, required by `meson-python`, but
other tools often did the wrong thing (such as load the entire file into the
metadata's free-form one line text field that was intended to describe
deviations from the classifier license(s)).

```toml
classifiers = [
  "License :: OSI Approved :: BSD License",
]
```

You should not include the `License ::` classifiers if you use the `license`
field {% rr PP007 %}.

### Extras

Sometimes you want to ship a package with optional dependencies. For example,
you might have extra requirements that are only needed for running a CLI, or for
plotting. Users must opt-in to get these dependencies by adding them to the
package or wheel name when installing, like `package[cli,mpl]`.

Here is an example of a simple extras:

```toml
[project.optional-dependencies]
cli = [
  "click",
]
mpl = [
  "matplotlib >=2.0",
]
```

Self dependencies can be used by using the name of the package, such as
`all = ["package[cli,mpl]"]`, (requires Pip 21.2+).

### Command line

If you want to ship an "app" that a user can run from the command line, you need
to add a `script` entry point. The form is:

```toml
[project.scripts]
cliapp = "package.__main__:main"
```

The format is command line app name as the key, and the value is the path to the
function, followed by a colon, then the function to call. If you use
`__main__.py` as the file, then `python -m` followed by the module will also
work to call the app (`__name__` will be `"__main__"` in that case).

### Development dependencies

The proper way to specify dependencies exclusively used for development tasks
(such as `pytest`, `ruff`, packages for generating documentation, etc.) is to
use dependency-groups. Dependency-groups are recommended over requirement files
because they are formally standardized (i.e. they will be more portable going
forward) and they are more composable. In contrast with extras,
dependency-groups are not available when installing your package via PyPI, but
they are available for local installation (and can be installed separately from
your package); the `dev` group is even installed, by default, when using `uv`'s
high level commands like `uv run` and `uv sync`. {% rr PP0086 %} Here is an
example:

<!-- [[[cog
with code_fence("toml"):
    print(pyproject.get_source("dependency-groups"))
]]] -->
<!-- prettier-ignore-start -->
```toml
[dependency-groups]
test = [
  "pytest >=9",
  "pytest-cov >=7",
]
dev = [
  { include-group = "test" },
]
docs = [
  "sphinx>=7.0",
  "myst_parser>=0.13",
  "sphinx_copybutton",
  "sphinx_autodoc_typehints",
  "furo>=2023.08.17",
]
```
<!-- prettier-ignore-end -->
<!-- [[[end]]] -->

You can include one dependency group in another. Most tools allow you to install
groups using `--group`, like `pip` (25.1+), `uv pip`, and the high level `uv`
interface. It's possible to install a package's dependency group without
installing the package itself, but usually you'll want to instruct your tool to
install both (the high level `uv` interface does this automatically). Nox, Tox,
and cibuildwheel all support groups, too. The `dependency-groups` package also
provides tools to get the dependencies.

[metadata]: https://packaging.python.org/en/latest/specifications/core-metadata/
[trove classifiers]: https://pypi.org/classifiers/
[spdx]: https://spdx.org/licenses
