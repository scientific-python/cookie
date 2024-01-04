---
layout: page
title: Writing documentation
permalink: /guides/docs/
nav_order: 4
parent: Topical Guides
---

{% include toc.html %}

# Writing documentation

Documentation used to require learning reStructuredText (sometimes referred to
as reST / RST), but today we have great choices for documentation in markdown,
the same format used by GitHub, Wikipedia, and others. This guide covers Sphinx,
and uses the modern MyST plugin to get Markdown support.

{: .note-title }

> Other frameworks
>
> There are other frameworks as well; these often are simpler, but are not as
> commonly used, and have somewhat fewer examples and plugins. They are:
>
> - [JupyterBook](https://jupyterbook.org): A powerful system for rendering a
>   collection of notebooks using Sphinx internally. Can also be used for docs,
>   though, see [echopype](https://echopype.readthedocs.io).
> - [MkDocs](https://www.mkdocs.org): a from-scratch new documentation system
>   based on markdown and HTML. Less support for man pages & PDFs than Sphinx,
>   since it doesn't use docutils. Has over
>   [200 plugins](https://github.com/mkdocs/catalog) - they are much easier to
>   write than Sphinx. Examples include [hatch](https://hatch.pypa.io),
>   [PDM](https://pdm.fming.dev),
>   [cibuildwheel](https://cibuildwheel.readthedocs.io),
>   [Textual](https://textual.textualize.io), and
>   [pipx](https://pypa.github.io/pipx/).

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
cross-platform noxfile instead), and uses RST instead of Markdown. Instead, this
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
copyright = "2024, My Name"
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

- [`myst_parser`][myst] is the Markdown parsing engine for Sphinx.
- `sphinx.ext.autodoc` will help us build API docs via reStructuredText and
  dynamic analysis. Also see the package [sphinx-autodoc2][], which supports
  Markdown and uses static analysis; it might not be as battle tested at this
  time, though.
- `sphinx.ext.intersphinx` will cross-link to other documentation.
- `sphinx.ext.mathjax` allows you to include mathematical formulas.
- [`sphinx.ext.napoleon`][] adds support for several common documentation styles
  like numpydoc.
- `sphinx_autodoc_typehints` handles type hints
- `sphinx_copybutton` adds a handle little copy button to code snipits.

We are including both possible file extensions. We are also avoiding some common
file patterns, just in case.

For theme, you have several good options. The clean, light-weight Furo theme is
shown above. Many scientific packages choose the `sphinx-py-data` theme, which
is also a good choice (no dark mode, though).

We are enabling a useful MyST extension: `colon_fence` allows you to use three
colons for directives, which might be highlighted better if the directive
contains text than three backticks. See more built-in extensions in
[MyST's docs](https://myst-parser.readthedocs.io/en/latest/syntax/optional.html).

One key feature of Sphinx is intersphinx, which allows documentation to
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
install the project, rather than being tempted to install only Sphinx and
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

This sets the Read the Docs config version (2 is required) {% rr RTD101 %}.

The `build` table is the modern way to specify a runner. You need an `os` (a
modern Ubuntu should be fine) {% rr RTD102 %}, a `tools` table (we'll use Python
{% rr RTD103 %}, several languages are supported here).

Adding a `sphinx` table tells Read the Docs to enable Sphinx integration. MkDocs
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

This is a more complex Nox job just because it's taking some options (the
ability to build and serve instead of just build, and the ability to select the
builder). The first portion is just setting up argument parsing. Then it does
some conditional installs based on arguments (sphinx-autobuild is only needed if
serving). It does an editable install of your package so that you can skip the
install steps with `-R` and still get updated documentation.

Then there's a dedicated handler for the 'linkcheck' builder, which just checks
links, and doesn't really produce output. Finally, we collect some useful args,
and run either the autobuild (for `--serve`) or regular build. We could have
just added `python -m http.server` pointing at the built documentation, but
autobuild will rebuild if you change a file while serving.

## API docs

To build API docs, you need to add the following Nox job. It will rerun
`sphinx-apidoc` to generate the sphinx autodoc pages for each of your public
modules.

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

Note that your docstrings are still parsed as reStructuredText.

## Notebooks in docs

You can combine notebooks into your docs. The tool for this is `nbsphinx`. If
you want to use it, add `nbsphinx` to your documentation requirements, add
`"nbsphinx"` to your `conf.py`'s `extensions =` list, and add some options for
nbsphinx in `conf.py`:

```python
nbsphinx_execute = "auto"

nbsphinx_execute_arguments = [
    "--InlineBackend.figure_formats={'png2x'}",
    "--InlineBackend.rc=figure.dpi=96",
]

nbsphinx_kernel_name = "python3"
```

You can set `nbsphinx_execute` to `always`, `never`, or `auto` - `auto` will
only execute empty notebooks. The execute arguments shown above will produce
"retina" images from Matplotlib. You can set the kernel name (make sure you can
execute all of your (unexecuted) notebooks).

If you want to use Markdown instead of notebooks, you can use jupytext (see
[here](https://nbsphinx.readthedocs.io/en/0.9.2/a-markdown-file.html)).

<!-- prettier-ignore-start -->
[diátaxis]: https://diataxis.fr/
[sphinx]: https://www.sphinx-doc.org/
[myst]: https://myst-parser.readthedocs.io/
[organizing content]: https://myst-parser.readthedocs.io/en/latest/syntax/organising_content.html
[sphinx-autodoc2]: https://sphinx-autodoc2.readthedocs.io/
[`sphinx.ext.napoleon`]: https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html
<!-- prettier-ignore-end -->
