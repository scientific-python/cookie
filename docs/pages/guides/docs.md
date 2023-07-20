---
layout: page
title: Writing documentation
permalink: /guides/docs/
nav_order: 4
parent: Topical Guides
---

{% include toc.html %}

# Writing documentation

Documentation used to require learning RestructureText (sometimes referred to as
ReST / RST), but today we have great choices for documentation in markdown, the
same format used by GitHub, Wikipedia, and others. There are two two major
documentation toolchains, sphinx and mkdocs. This guide covers Sphinx, and uses
the modern MyST plugin to get markdown support.

## What to include

Ideally, software documentation should include:

- Introductory **tutorials**, to help new users (or potential users) understand
  what the software can do and take their first steps.
- Task-oriented **guides**, examples that address specific uses.
- **Reference**, specifying the detailed inputs and outputs of every public
  object in the codebase.
- **Explanations** to convey deeper understanding of why and how the software
  operates the way it does.

{: .note-title }

> The Diátaxis framework
>
> This overall framework has a name, [Diátaxis][], and you can read more about
> it if you are interested.

<!-- [[[cog
from cog_helpers import code_fence, render_cookie, Matcher
with render_cookie() as package:
    docs_conf_py = package.joinpath("docs/conf.py").read_text(encoding="utf-8").strip()
    docs_index_md = package.joinpath("docs/index.md").read_text(encoding="utf-8").strip()
    readthedocs_yaml = package.joinpath(".readthedocs.yml").read_text(encoding="utf-8").strip()
    noxfile = Matcher.from_file(package / "noxfile.py")
]]] -->
<!-- [[[end]]] -->

## Hand-written docs

Create `docs/` directory within your project (i.e. next to `src/`). There is a
sphinx-quickstart tool, but unnecessary files (make/bat, we recommend a
cross-platform noxfile instead), and uses rst instead of markdown. Instead, this
is our recommended starting point for `conf.py`:

### conf.py

<!-- [[[cog
with code_fence("python"):
    print(docs_conf_py)
]]] -->
<!-- prettier-ignore-start -->
```python
from __future__ import annotations

import importlib.metadata

project = "package"
copyright = "2023, My Name"
author = "My Name"
version = release = importlib.metadata.version("package")

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "sphinx_copybutton",
]

source_suffix = [".rst", ".md"]
exclude_patterns = [
    "_build",
    "**.ipynb_checkpoints",
    "Thumbs.db",
    ".DS_Store",
    ".env",
    ".venv",
]

html_theme = "furo"

myst_enable_extensions = [
    "colon_fence",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

nitpick_ignore = [
    ("py:class", "_io.StringIO"),
    ("py:class", "_io.BytesIO"),
]

always_document_param_types = True
```
<!-- prettier-ignore-end -->
<!-- [[[end]]] -->

We start by setting some configuration values, but most notably we are getting
the package version from the installed version of your package. We are listing
several good extensions:

- [`myst_parser`][myst] is the markdown parsing engine for sphinx.
- `sphinx.ext.autodoc` will help us build API docs via Restructured Text and
  dynamic analysis. Also see the package [sphinx-autodoc2][], which supports
  markdown and uses static analysis; it might not be as battle tested at this
  time, though.
- `sphinx.ext.intersphinx` will cross-link to other documentation.
- `sphinx.ext.mathjax` allows you to include mathematical formulas.
- [`sphinx.ext.napoleon`][] adds support for several common documentation styles
  like numpydoc.
- `sphinx_autodoc_typehints` handles type hints
- `sphinx_copybutton` adds a handle little copy button to code snipits.

We are including both possible file extensions. We are also avoiding some common
file patterns, just in case.

For theme, you have several good options. The clean, light-weight `furo` theme
is shown above; a related theme from the same author is being used for the
CPython documentation in CPython 3.13. Many scientific packages choose the
`sphinx-py-data` theme, which is also a good choice (no dark mode, though).

We are enabling a useful MyST extension: `colon_fence` allows you to use three
colons for directives, which might be highlighted better if the directive
contains text than three backticks. See more built-in extensions in
[MyST's docs](https://myst-parser.readthedocs.io/en/latest/syntax/optional.html).

One key feature of Sphinx is interphinx, which allows documentation to
cross-reference each other. You can list other projects you are using, but a
good minimum is to at least link to the CPython docs. You need to provide the
path to the `objects.inv` file, usually at the main documentation URL.

We are going to be enabling nitpick mode, and when we do, there's a chance some
classes will complain if they don't link with intersphinx. A couple of common
examples are listed here (StringIO/BytesIO don't point at the right thing) -
feel free to add/remove as needed.

Finally, when we have static types, we'll want them always listed in the
docstrings, even if the parameter isn't documented yet. Feel free to check
[sphinx-autodoc-typehints](https://github.com/tox-dev/sphinx-autodoc-typehints)
for more options.

### index.md

Your `index.md` file can start out like this:

<!-- [[[cog
with code_fence("md", width=4):
    print(docs_index_md)
]]] -->
<!-- prettier-ignore-start -->
````md
# package

```{toctree}
:maxdepth: 2
:hidden:

```

```{include} ../README.md
:start-after: <!-- SPHINX-START -->
```

## Indices and tables

- {ref}`genindex`
- {ref}`modindex`
- {ref}`search`
````
<!-- prettier-ignore-end -->
<!-- [[[end]]] -->

You can put your project name in as the title. The `toctree` directive houses
your table of contents; you'll list each new page you add inside that directive.

If you want to inject a readme, you can use the `include` directive shown above.
You don't want to add the README's title (and probably your badges) to your
docs, so you can add a expression to your README (`<!-- SPHINX-START -->` above)
to mark where you want the docs portion to start.

You can add the standard indices and tables at the end.

### pyproject.toml additions

Setting a `docs` extra looks like this:

```toml
[project.optional-dependencies]
docs = [
  "furo",
  "myst_parser >=0.13",
  "sphinx >=4.0",
  "sphinx-copybutton",
  "sphinx-autodoc-typehints",
]
```

While there are other ways to specify docs, and you don't have to make the docs
requirements an extra, this is a good idea as it forces docs building to always
install the project, rather than being tempted to install only sphinx and
plugins and try to build against an uninstalled version of your project.

### .readthedocs.yaml

In order to use <https://readthedocs.org> to build, host, and preview your
documentation, you must have a `.reathedocs.yml` file {% rr RTD100 %} like this:

<!-- [[[cog
with code_fence("yaml"):
    print(readthedocs_yaml)
]]] -->
<!-- prettier-ignore-start -->
```yaml
# Read the Docs configuration file
# See https://docs.readthedocs.io/en/stable/config-file/v2.html for details

version: 2

build:
  os: ubuntu-22.04
  tools:
    python: "3.11"
sphinx:
  configuration: docs/conf.py

python:
  install:
    - method: pip
      path: .
      extra_requirements:
        - docs
```
<!-- prettier-ignore-end -->
<!-- [[[end]]] -->

This sets the readthedocs config version (2 is required) {% rr RTD101 %}.

The `build` table is the modern way to specify a runner. You need an `os` (a
modern ubuntu should be fine) {% rr RTD102 %}, a `tools` table (we'll use Python
{% rr RTD103 %}, several languages are supported here).

Adding a `sphinx` table tells readthedocs to enable Sphinx integration. MkDocs
is supported too.

Finally, we have a `python` table with an `install` key to describe how to
install our project. This will enable our "docs" extra.

### noxfile.py additions

Add a session to your `noxfile.py` to generate docs:

<!-- [[[cog
with code_fence("python"):
    print(noxfile.get_source("docs"))
]]] -->
<!-- prettier-ignore-start -->
```python
@nox.session(reuse_venv=True)
def docs(session: nox.Session) -> None:
    """
    Build the docs. Pass "--serve" to serve.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("--serve", action="store_true", help="Serve after building")
    parser.add_argument(
        "-b", dest="builder", default="html", help="Build target (default: html)"
    )
    args, posargs = parser.parse_known_args(session.posargs)

    if args.builder != "html" and args.serve:
        session.error("Must not specify non-HTML builder with --serve")

    session.install(".[docs]")
    session.chdir("docs")

    if args.builder == "linkcheck":
        session.run(
            "sphinx-build", "-b", "linkcheck", ".", "_build/linkcheck", *posargs
        )
        return

    session.run(
        "sphinx-build",
        "-n",  # nitpicky mode
        "-T",  # full tracebacks
        "-W",  # Warnings as errors
        "--keep-going",  # See all errors
        "-b",
        args.builder,
        ".",
        f"_build/{args.builder}",
        *posargs,
    )

    if args.serve:
        session.log("Launching docs at http://localhost:8000/ - use Ctrl-C to quit")
        session.run("python", "-m", "http.server", "8000", "-d", "_build/html")
```
<!-- prettier-ignore-end -->
<!-- [[[end]]] -->

## API docs

To build API docs, you need to add the following nox job:

### noxfile.py additions

<!-- [[[cog
with code_fence("python"):
    txt = noxfile.get_source("build_api_docs")
    print(txt.replace("package", "<package-name-here>"))
]]] -->
<!-- prettier-ignore-start -->
```python
@nox.session
def build_api_docs(session: nox.Session) -> None:
    """
    Build (regenerate) API docs.
    """

    session.install("sphinx")
    session.chdir("docs")
    session.run(
        "sphinx-apidoc",
        "-o",
        "api/",
        "--module-first",
        "--no-toc",
        "--force",
        "../src/<package-name-here>",
    )
```
<!-- prettier-ignore-end -->
<!-- [[[end]]] -->

And you'll need this added to your `docs/index.md`:

````md
```{toctree}
:maxdepth: 2
:hidden:
:caption: API

api/<package-name-here>
```
````

Note that your docstrings are still parsed as Restructured Text.

<!-- prettier-ignore-start -->
[diátaxis]: https://diataxis.fr/
[sphinx]: https://www.sphinx-doc.org/
[myst]: https://myst-parser.readthedocs.io/
[organizing content]: https://myst-parser.readthedocs.io/en/latest/syntax/organising_content.html
[sphinx-autodoc2]: https://sphinx-autodoc2.readthedocs.io/
[`sphinx.ext.napoleon`]: https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html
<!-- prettier-ignore-end -->
