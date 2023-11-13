---
layout: page
title: Task runners
permalink: /guides/tasks/
nav_order: 30
parent: Topical Guides
---

{% include toc.html %}

# Task runners

<!-- [[[cog
from cog_helpers import  code_fence, render_cookie, Matcher
with render_cookie() as package:
    noxfile = Matcher.from_file(package / "noxfile.py")
]]] -->
<!-- [[[end]]] -->

A task runner, like [make][] (fully general), [rake][] (Ruby general),
[invoke][] (Python general), [hatch][] (Python packages), [tox][] (Python
packages), or [nox][] (Python semi-general), is a tool that lets you specify a
set of tasks via a common interface. These have been discouraged by some
community projects in the past, since they can be a crutch, allowing poor
packaging practices to be employed behind a custom script, and they can hide
what is actually happening.

As long as you don't rely on it to hide packaging issues, a great choice for
many packages is [nox][]. Nox has two strong points that help with the above
concerns. First, it is very explicit, and even prints what it is doing as it
operates. Unlike the older tox, it does not have any implicit assumptions
built-in. Second, it has very elegant built-in support for both virtual and
Conda environments. This can greatly reduce new contributor friction with your
codebase.

A daily developer is _not_ expected to use nox for simple tasks, like running
tests or linting. You should _not_ rely on nox to make a task that should be
made simple and standard (like building a package) complicated. You do not need
to use nox for linting on CI, or often even for testing on CI, even if those
tasks are provided for users. Nox is a few seconds slower than running directly
in a custom environment - but for new users, and rarely run tasks, it is _much_
faster than explaining how to get setup or manually messing with virtual
environments. It is also highly reproducible, creating and destroying the
temporary environment each time. And, if you pass `-R` when rerunning it, you
can skip the setup and install steps, making it nearly as fast as directly
running the commands!

{% rr PY007 %} You _should_ use a task runner to make it easy and simple for new
contributors to run things. You _should_ use a task runner to make specialized
developer tasks easy. You _should_ use a task runner to avoid making single-use
virtual environments for docs and other rarely run tasks. Nox is recommended,
but tox and hatch both are also acceptable.

Nox doesn't handle binary builds very well, so for compiled projects, it might
be best left to just specialized tasks.

[hatch]: https://hatch.pypi.io
[nox]: https://nox.thea.codes
[tox]: https://tox.readthedocs.io
[invoke]: https://www.pyinvoke.org
[rake]: https://ruby.github.io/rake/
[make]: https://www.gnu.org/software/make/

## Nox

### Installing

Installing nox should be handled like any other Python _application_. You should
either use a good package manager, like brew on macOS, or you should use pipx;
either permanently (`pipx install nox`) or by running `pipx run nox` instead of
`nox`.

On GitHub Actions or Azure, pipx is available by default, so you should use
`pipx run nox`. To give it access to all Python versions, you can use this
action:

```yaml
- uses: wntrblm/nox@2023.04.22
```

You can now access all current versions of Python from nox. At least in GitHub
Actions, you should add `--forcecolor` to your nox runs to get color output in
your logs, or set `env: FORCE_COLOR: 3`. If you'd like to customise the versions
of Python prepared for you, then use input like this:

```yaml
- uses: wntrblm/nox@2023.04.22
  with:
    python-versions: "3.8, 3.9, 3.10, 3.11, 3.12, pypy-3.9, pypy-3.10"
```

### Introduction

Nox is a tool for running tasks, called "sessions", inside temporary virtual
environments. It is configured through Python and is designed to resemble
pytest. The file it looks for is called `noxfile.py` by default. This is an
example of a simple nox file:

```python
import nox


@nox.session
def tests(session: nox.Session) -> None:
    """
    Run the unit and regular tests.
    """
    session.install(".[test]")
    session.run("pytest", *session.posargs)
```

This will create a session called `tests`. The function receives the "session"
argument, which gives you access to the virtual environment it creates. You can
use `.install()` to install inside the environment, and `.run()` to run inside
the environment. We are also using `session.posargs` to allow extra arguments to
be passed through to pytest. There are
[more useful methods](https://nox.thea.codes/en/stable/config.html#module-nox.sessions)
as well.

You can run this using:

```console
$ nox -s tests
```

You can see all defined sessions (along with the docstrings) using:

```console
$ nox -l
```

It is a good idea to list the sessions you want by default by setting
`nox.options.sessions` near the top of your file:

```python
nox.options.sessions = ["lint", "tests"]
```

This will keep you from running extra things like `docs` by default.

### Parametrizing

You can parametrize sessions. either on Python or on any other item.

```python
# Shortcut to parametrize Python
@nox.session(python=["3.8", "3.9", "3.10", "3.11", "3.12"])
def my_session(session: nox.Session) -> None:
    ...


# General parametrization
@nox.session
@nox.parametrize("letter", ["a", "b"], ids=["a", "b"])
def my_session(session: nox.Session, letter: str) -> None:
    ...
```

The optional `ids=` parameter can give the parametrization nice names, like in
pytest.

If a user does not have a particular version of Python installed, it will be
skipped. You can use a Docker container to run in an environment where all
Python's (3.6+) are available:

```console
$ docker run --rm -itv $PWD:/src -w /src quay.io/pypa/manylinux_2_28_x86_64:latest pipx run nox
```

Another container you can use is `thekevjames/nox:latest`; this has nox
pre-installed (no pipx) and Python 2.7 and 3.5 as well.

### Useful sessions

Things like bumping the versions can be made sessions - since nox handles the
environment for you, you can use any Python dependencies you like, and not have
to worry about installing anything. Here are some commonly useful sessions that
will likely look similar across different projects:

#### Lint

Ideally, all developers should be using pre-commit directly, but this helps new
users.

<!-- [[[cog
with code_fence("python"):
    print(noxfile.get_source("lint"))
]]] -->
<!-- prettier-ignore-start -->
```python
@nox.session
def lint(session: nox.Session) -> None:
    """
    Run the linter.
    """
    session.install("pre-commit")
    session.run(
        "pre-commit", "run", "--all-files", "--show-diff-on-failure", *session.posargs
    )
```
<!-- prettier-ignore-end -->
<!-- [[[end]]] -->

#### Tests

<!-- [[[cog
with code_fence("python"):
    print(noxfile.get_source("tests"))
]]] -->
<!-- prettier-ignore-start -->
```python
@nox.session
def tests(session: nox.Session) -> None:
    """
    Run the unit and regular tests.
    """
    session.install(".[test]")
    session.run("pytest", *session.posargs)
```
<!-- prettier-ignore-end -->
<!-- [[[end]]] -->

#### Docs

<!-- [[[cog
with code_fence("python"):
    print(noxfile.get_source("docs"))
]]] -->
<!-- prettier-ignore-start -->
```python
@nox.session(reuse_venv=True)
def docs(session: nox.Session) -> None:
    """
    Build the docs. Pass "--serve" to serve. Pass "-b linkcheck" to check links.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("--serve", action="store_true", help="Serve after building")
    parser.add_argument(
        "-b", dest="builder", default="html", help="Build target (default: html)"
    )
    args, posargs = parser.parse_known_args(session.posargs)

    if args.builder != "html" and args.serve:
        session.error("Must not specify non-HTML builder with --serve")

    extra_installs = ["sphinx-autobuild"] if args.serve else []

    session.install("-e.[docs]", *extra_installs)
    session.chdir("docs")

    if args.builder == "linkcheck":
        session.run(
            "sphinx-build", "-b", "linkcheck", ".", "_build/linkcheck", *posargs
        )
        return

    shared_args = (
        "-n",  # nitpicky mode
        "-T",  # full tracebacks
        f"-b={args.builder}",
        ".",
        f"_build/{args.builder}",
        *posargs,
    )

    if args.serve:
        session.run("sphinx-autobuild", *shared_args)
    else:
        session.run("sphinx-build", "--keep-going", *shared_args)
```
<!-- prettier-ignore-end -->
<!-- [[[end]]] -->

This supports setting up a quick server as well, run like this:

```console
$ nox -s docs -- --serve
```

#### Build (pure Python)

For pure Python packages, this could be useful:

<!-- [[[cog
with code_fence("python"):
    print("import shutil")
    print("from pathlib import Path")
    print()
    print("DIR = Path(__file__).parent.resolve()")
    print()
    print()
    print(noxfile.get_source("build"))
]]] -->
<!-- prettier-ignore-start -->
```python
import shutil
from pathlib import Path

DIR = Path(__file__).parent.resolve()


@nox.session
def build(session: nox.Session) -> None:
    """
    Build an SDist and wheel.
    """

    build_path = DIR.joinpath("build")
    if build_path.exists():
        shutil.rmtree(build_path)

    session.install("build")
    session.run("python", "-m", "build")
```
<!-- prettier-ignore-end -->
<!-- [[[end]]] -->

### Examples

A standard
[powered by nox](https://github.com/scikit-hep/hist/blob/main/noxfile.py)
package in Pure Python can be found in the Hist project of Scikit-HEP.

A package that happens to use PDM (like Poetry but better) is Scikit-HEP UHI,
which is
[powered by nox](https://github.com/scikit-hep/uhi/blob/main/noxfile.py). Nox
can setup a conda environment with ROOT (slow, but only nox and conda are
required). There also is a version bump session, and does some custom logic too.

The complex testing procedure powering Scientific Python Cookie is
[powered by nox](https://github.com/scientific-python/cookie/blob/main/noxfile.py).
It allows the complex CI jobs that generate projects and lint/test/build them to
be run locally with no other setup.

PyPA's cibuildwheel also is
[powered by nox](https://github.com/pypa/cibuildwheel/blob/main/noxfile.py),
running pip-tools' compile on every Python version to pin dependencies, as well
as providing a standard interface to update Python and project listing update
scripts. The docs job there runs mkdocs instead of Sphinx. Other PyPA projects
using nox include [pip](https://github.com/pypa/pip/blob/main/noxfile.py),
[pipx](https://github.com/pypa/pipx/blob/main/noxfile.py),
[manylinux](https://github.com/pypa/manylinux/blob/main/noxfile.py),
[packaging](https://github.com/pypa/packaging/blob/main/noxfile.py), and
[packaging.python.org](https://github.com/pypa/packaging.python.org/blob/main/noxfile.py).
