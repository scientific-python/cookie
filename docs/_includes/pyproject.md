## pyproject.toml: project table

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
  "typing_extensions",
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

### Extras

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

### Command line

If you want to ship an "app" that a user can run from the command line, you need
to add a `script` entry point. The form is:

```toml
[project.scripts]
cliapp = "packakge.__main__:main"
```

The format is command line app name as the key, and the value is the path to the
function, followed by a colon, then the function to call. If you use
`__main__.py` as the file, then `python -m` followed by the module will also
work to call the app (`__name__` will be `"__main__"` in that case).

[metadata]: https://packaging.python.org/en/latest/specifications/core-metadata/
