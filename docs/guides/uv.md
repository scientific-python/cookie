---
short_title: Using uv
---

# Using uv for development

[uv][] can manage Python installations, project environments, dependencies,
and lockfiles, as well as run commands and build packages. This page focuses on
using uv to work on an existing Python package. With regards to setting it up, see the [packaging guide][] for
project metadata and build-system configuration, the [pytest guide][] for
testing, the [style guide][] for linting and formatting, the [documentation
guide][] for building docs, and the [task runner guide][] for repeatable or
specialized tasks.


## Install uv

Follow the [official installation instructions][uv installation] to install uv
with the standalone installer or a system package manager. Afterwards, check the installation with:

```console
uv --version
```

## Run common development tasks

After cloning a project that contains a `pyproject.toml`, you can immediately
run the development commands you need using `uv run`:

```console
# Run the full test suite
uv run pytest

# Run one test and pass normal arguments to pytest
uv run pytest tests/test_example.py::test_example -vv

# Run a module or project command
uv run python -m example
uv run example-cli --help
```

There is no need for a separate setup step.
`uv run` automatically creates a virtual environment in `.venv` if necessary, installs
the package and its dependencies, and then runs the command.  You normally do not
need to activate the environment by hand.

If a command belongs to a dependency group that is not enabled by default,
include the group for that invocation:

```console
uv run --group docs sphinx-build -M html docs docs/_build
```

Refer to the relevant page in this guide for the command itself. For
example, the [pytest guide][] covers test selection and debugging, while the
[documentation guide][] covers Sphinx, MkDocs, and Zensical.

## Prepare the project environment

One side effect of `uv run` is that it keeps the project environment up to date. However, sometimes you want to prepare the environment explicitly.
Common reasons include:

- Preparing `.venv` for an editor, notebook, or interactive shell.
- Installing several dependency groups up front.
- Restoring an exact environment by removing packages that are not in the
  lockfile. `uv run` keeps such extra packages by default.
- Separating environment installation from command execution in CI.
- Updating the lockfile after changing `pyproject.toml`.

To prepare the project environment with the default dependency groups, run:

```console
uv sync
```

This creates or updates `.venv` and `uv.lock`. The `dev` dependency group is included by
default. To prepare an environment containing every dependency group, including
groups such as `docs`, use:

```console
uv sync --all-groups
```

Configure your editor to use the Python interpreter in `.venv`. Note that `.venv` is a regular virtual environment, so you can also activate it manually using the standard commands.


## Manage Python versions

uv can download and manage Python as well as packages:

```console
# Install a Python version
uv python install 3.12

# Select the default version for this checkout
uv python pin 3.12

# Run once in a temporary environment with another version
uv run --isolated --python 3.14 pytest
```

`uv python pin` writes a `.python-version` file. This chooses the interpreter
used for local development; it does not change the range of Python versions
supported by the package. That range belongs in `project.requires-python`, as
described in the [packaging guide][].

The `--isolated` flag keeps this one-off run separate from the project's
persistent `.venv`.

## Add and remove dependencies

Add runtime dependencies to `project.dependencies` with:

```console
uv add numpy
uv remove numpy
```

Development-only packages belong in a dependency group:

```console
uv add --group test pytest
uv add --group docs sphinx
uv remove --group docs sphinx
```

These commands update `pyproject.toml`, `uv.lock`, and `.venv` together. You can
also edit `pyproject.toml` by hand and then run `uv lock` or `uv sync`.


## Build the package

Build a source distribution and wheel with:

```console
uv build
```

The artifacts are written to `dist/`. uv invokes the backend selected in
`[build-system]`; backend-specific file inclusion and build settings still come
from that backend. See the [packaging guide][] for selecting and configuring a
backend, and the CI guides for publishing releases.

[documentation guide]: guides/docs
[packaging guide]: guides/packaging-simple
[pytest guide]: guides/pytest
[style guide]: guides/style
[task runner guide]: guides/tasks
[uv]: https://docs.astral.sh/uv/
[uv installation]: https://docs.astral.sh/uv/getting-started/installation/
