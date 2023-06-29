---
layout: page
title: Writing documentation
permalink: /tutorials/docs/
nav_order: 5
parent: Tutorials
---

{% include toc.html %}

# Writing documentation

## Build the documentation

Scientific Python software documentation can be written in the Markdown syntax,
which looks like this:

````markdown
# My nifty title

- list
- of
- items

Some **bold** or _italicized_ text!

```python
# A code block

1 + 1
```
````

This documentation "source code" is then _built_ into a formats like HTML or PDF
to be displayed to the user.

There are a variety of tools that can do this. In this guide we will present an
approach that is mainstream in the scientific Python community: the [Sphinx][]
documentation generator with the [MyST][] plugin. Refer to the MyST
documentation for more information on the Markdown syntax in general and MyST's
flavor of Markdown in particular.

We'll start with a very basic template. Start by create a `docs/` directory
within your project (i.e. next to `src/`).

```bash
mkdir docs
```

In this directory, we will create a minimal Sphinx configuration file at
`docs/conf.py`.

```py
# content of docs/conf.py

project = "example"
extensions = ["myst_parser"]
source_suffix = [".rst", ".md"]
```

And, at `docs/index.md`, we will create a minimal front page for our
documentation.

```markdown
# Example documentation

Hello world!
```

You should now have something like this.

```bash
example/
├── docs/
│   ├── conf.py
│   ├── index.md
(...)
```

To build HTML from this source, install sphinx and the MyST Markdown parser

```bash
pip install sphinx myst-parser
```

and then run `sphinx-build`, pointing it to your directory of source files and a
target directory for writing rendered (HTML) output files.

```bash
sphinx-build docs/ docs/build/
```

You should see some log message ending in `build succeeded.` This created the
directory `docs/build`. Open `docs/build/index.html` in your web browser to view
the documentation.

## Essential Features of MyST Markdown

We refer you to the [MyST][] documentation for topics including:

- Typography
- Tables
- Images and figures
- Cross-references
- Math and equations
- Including content from other files

## Structure

We began with this structure, having a single documentation page.

```bash
example/
├── docs/
│   ├── conf.py
│   ├── index.md
(...)
```

Suppose we add some tutorials pages in a subdirectory.

```bash
example/
├── docs/
│   ├── conf.py
│   ├── index.md
│   └── tutorials/
│       ├── installation.md
│       ├── first-steps.md
│       └── real-application.md
(...)
```

We can link them from the front page by using the MyST Markdown `{toctree}`
directive.

````markdown
```{toctree}
tutorials/installation.md
tutorials/first-steps.md
tutorials/real-application.md
```
````

For more details see the MyST documentation page on [organizing content][].

## Automatically generate reference documentation

Reference documentation provides comprehensive documentation of the API: all the
inputs and outputs of every public object in the codebase. This should not be
written by hand; that would be tedious and have a high probably of human error
or drifting out of sync over time.

MyST recommends using [sphinx-autodoc2][]. However, we currently recommend using
the built-in sphinx `autodoc` and `autosummary` extensions because they
interoperates well with docstrings written to the numpydoc standard. To invoke
them, we need to employ yet another syntax (reST). Fortunately, you can simply
copy/paste these examples.

In `docs/conf.py`, add to the list of extensions.

```py
extensions = [
    # whatever you already have in here...
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
]
```

(Note that these extensions come with `sphinx`, so there is nothing more to
install.)

You can document a single object (e.g. function), shown inline on the page

````markdown
```{eval-rst}
.. autofunction:: example.refraction.snell
    :noindex:
    :toctree: generated
```
````

Or you can generate a table that links out to documentation for each object.

````markdown
```{eval-rst}
.. autosummary::
    :nosignatures:
    :toctree: generated

    example.refraction.snell
```
````

See the [guide]({% link pages/guides/docs.md %}) for more information on how to
integrate this into a package, and setup for nox.

<!-- prettier-ignore-start -->
[diátaxis]: https://diataxis.fr/
[sphinx]: https://www.sphinx-doc.org/
[myst]: https://myst-parser.readthedocs.io/
[organizing content]: https://myst-parser.readthedocs.io/en/latest/syntax/organising_content.html
[sphinx-autodoc2]: https://sphinx-autodoc2.readthedocs.io/
<!-- prettier-ignore-end -->
