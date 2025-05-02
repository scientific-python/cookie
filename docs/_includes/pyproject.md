## pyproject.toml: project table

The metadata is specified in a [standards-based][metadata] format:

```toml
[project]
name = "package"
description = "A great package."
readme = "README.md"
license = "BSD-3-Clause"
license-files = ["LICENSE"]
authors = [
  { name = "My Name", email = "me@email.com" },
]
maintainers = [
  { name = "My Organization", email = "myemail@email.com" },
]
requires-python = ">=3.9"

dependencies = [
  "typing_extensions",
]

classifiers = [
  "Development Status :: 4 - Beta",
  "Programming Language :: Python :: 3 :: Only",
  "Programming Language :: Python :: 3.9",
  "Programming Language :: Python :: 3.10",
  "Programming Language :: Python :: 3.11",
  "Programming Language :: Python :: 3.12",
  "Programming Language :: Python :: 3.13",
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

### License

The license can be done one of two ways.

The modern way is to use the `license` field and an [SPDX identifier
expression][spdx]. You can specify a list of files globs in `license-files`.
Currently, `hatchling>=1.26`, `flit-core>=1.11`, `pdm-backend>=2.4`,
`setuptools>=77`, and `scikit-build-core>=0.12` support this. Only `maturin`,
`meson-python`, and `flit-core` do not support this yet.

The classic convention uses one or more [Trove Classifiers][] to specify the
license. There also was a `license.file` field, required by `meson-python`, but
other tools often did the wrong thing (such as load the entire file into the
metadata's free-form one line text field that was intended to describe
deviations from the classifier license(s)).

```
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

It is recommended to use dependency-groups instead of making requirement files.
This allows you to specify dependencies that are only needed for development;
unlike extras, they are not available when installing via PyPI, but they are
available for local installation, and the `dev` group is even installed by
default when using `uv`.

Here is an example:

```toml
[dependency-groups]
test = [
  "pytest >=6.0",
]
dev = [
  { include-group = "test" },
]
```

You can include one dependency group in another. Most tools allow you to install
groups using `--group`, like `pip` (25.1+), `uv pip`, and the high level `uv`
interface. You do not need to install the package, though usually you do (the
high level `uv` interface does). Nox, Tox, and cibuildwheel all support groups
too. The `dependency-groups` package provides tools to get the dependencies,
too.

[metadata]: https://packaging.python.org/en/latest/specifications/core-metadata/
[trove classifiers]: https://pypi.org/classifiers/
[spdx]: https://spdx.org/licenses
