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
as reST / rST), but today we have great choices for documentation in markdown,
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
>   write than Sphinx. Example sites include [hatch](https://hatch.pypa.io),
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
    readthedocs_yaml = package.joinpath(".readthedocs.yaml").read_text(encoding="utf-8").strip()
    noxfile = Matcher.from_file(package / "noxfile.py")
]]] -->
<!-- [[[end]]] -->

## Hand-written docs

Create `docs/` directory within your project (i.e. next to `src/`). There is a
sphinx-quickstart tool, but it creates unnecessary files (make/bat, we recommend
a cross-platform noxfile instead), and uses rST instead of Markdown. Instead,
this is our recommended starting point for `conf.py`:

### conf.py

<!-- [[[cog
with code_fence("python"):
    print(docs_conf_py)
]]] -->
<!-- prettier-ignore-start -->
```python
from __future__ import annotations

import importlib.metadata
from typing import Any

project = "package"
copyright = "2025, My Name"
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

html_theme_options: dict[str, Any] = {
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/org/package",
            "html": """
                <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"></path>
                </svg>
            """,
            "class": "",
        },
    ],
    "source_repository": "https://github.com/org/package",
    "source_branch": "main",
    "source_directory": "docs/",
}

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

For theme, many scientific packages choose the
[pydata-sphinx-theme](https://pydata-sphinx-theme.readthedocs.io/). The
[Furo theme](https://pradyunsg.me/furo/) is another popular choice. The site
[sphinx-themes.org](https://sphinx-themes.org/) can be used to compare options.

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
documentation, you must have a `.readthedocs.yaml` file {% rr RTD100 %} like
this:

{% tabs %} {% tab uv-sphinx uv + Sphinx %}

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
  os: ubuntu-24.04
  tools:
    python: "3.13"
  commands:
    - asdf plugin add uv
    - asdf install uv latest
    - asdf global uv latest
    - uv sync --group docs
    - uv run python -m sphinx -T -b html -d docs/_build/doctrees -D language=en
      docs $READTHEDOCS_OUTPUT/html
```
<!-- prettier-ignore-end -->
<!-- [[[end]]] -->

{% endtab %} {% tab pip-sphinx pip + Sphinx %}

```yaml
# Read the Docs configuration file
# See https://docs.readthedocs.io/en/stable/config-file/v2.html for details

version: 2

build:
  os: ubuntu-22.04
  tools:
    python: "3.12"
sphinx:
  configuration: docs/conf.py

python:
  install:
    - method: pip
      path: .
      extra_requirements:
        - docs
```

{% endtab %} {% endtabs %}

This sets the Read the Docs config version (2 is required) {% rr RTD101 %}.

The `build` table is the modern way to specify a runner. You need an `os` (a
modern Ubuntu should be fine) {% rr RTD102 %}, a `tools` table (we'll use Python
{% rr RTD103 %}, several languages are supported here).

Adding a `sphinx` table tells Read the Docs to enable Sphinx integration. MkDocs
is supported too. You must include one of these unless you use build commands
{% rr RTD104 %}.

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
@nox.session(reuse_venv=True, default=False)
def docs(session: nox.Session) -> None:
    """
    Build the docs. Pass --non-interactive to avoid serving. First positional argument is the target directory.
    """

    doc_deps = nox.project.dependency_groups(PROJECT, "docs")
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-b", dest="builder", default="html", help="Build target (default: html)"
    )
    parser.add_argument("output", nargs="?", help="Output directory")
    args, posargs = parser.parse_known_args(session.posargs)
    serve = args.builder == "html" and session.interactive

    session.install("-e.", *doc_deps, "sphinx-autobuild")

    shared_args = (
        "-n",  # nitpicky mode
        "-T",  # full tracebacks
        f"-b={args.builder}",
        "docs",
        args.output or f"docs/_build/{args.builder}",
        *posargs,
    )

    if serve:
        session.run("sphinx-autobuild", "--open-browser", *shared_args)
    else:
        session.run("sphinx-build", "--keep-going", *shared_args)
```
<!-- prettier-ignore-end -->
<!-- [[[end]]] -->

This is a more complex Nox job just because it's taking some options (the
ability to build and serve instead of just build). The first portion is just
setting up argument parsing so we can serve if building `html`. Then it does
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
@nox.session(default=False)
def build_api_docs(session: nox.Session) -> None:
    """
    Build (regenerate) API docs.
    """

    session.install("sphinx")
    session.run(
        "sphinx-apidoc",
        "-o",
        "docs/api/",
        "--module-first",
        "--no-toc",
        "--force",
        "src/<package-name-here>",
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
you want to use it, add `nbsphinx` and `ipykernel` to your documentation
requirements, add `"nbsphinx"` to your `conf.py`'s `extensions =` list, and add
some options for nbsphinx in `conf.py`:

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

Note that you will also need the `pandoc` command line tool installed locally
for this to work. CI services like readthedocs usually have it installed.

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

<script src="{% link assets/js/tabs.js %}"></script>
