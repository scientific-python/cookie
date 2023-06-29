---
layout: page
title: Packaging
permalink: /tutorials/packaging/
nav_order: 3
parent: Tutorials
---

{% include toc.html %}

# Packaging

In the section you will:

- Place your module in an installable package.
- Employ version control.
- Install and use the package.

For more about packaging, see our [packaging guide][].

## Create a minimal installable Python package

Let’s create a Python package that contains this function.

First, create a new directory for your software package, called `example`, and
move into that:

```bash
mkdir example
cd example
```

You should immediately initialize an empty Git repository in this directory; if
you need a refresher on using Git for version control, check out the Software
Carpentry lesson [Version Control with Git][]. You should commit changes
regularly throughout what follows. This tutorial will not explicitly remind you
to commit your work after this point.

```bash
git init
```

Within the package directory `example`, create subdirectories `src` ("source")
for the source code.

```bash
mkdir src
```

Create a file at `src/__init__.py`. This is what identifies the directory as a
"package" to Python. It may remain empty.

```bash
touch src/__init__.py
```

Place `refraction.py`, our code from the previous section, next to it, at
`src/refraction.py`.

The last element your package needs is a `pyproject.toml` file, placed in the
root directory.

```bash
touch pyproject.yaml
```

Fill in the minimally required metadata, which includes the package name,
version, and some options related to how to install it, which you can copy as
is.

```bash
# contents of pyproject.toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "example"
version = "0.1.0"
```

The package name given here, `example`, matches the directory package that
contains our project's code. We have chosen `0.1.0` as the starting version for
this package; you’ll see more in a later section about versioning, and how to
specify this without manually writing it here.

At this point, your package's file structure will look like

```bash
.
├── pyproject.toml
├── src
│   └── example
│       ├── __init__.py
│       └── refraction.py
```

## Install and use your package

Now that your package has the necessary elements, you can install it into your
virtual environment (which should already be active). From the top level of your
project’s directory, enter

```
pip install -e .
```

The `-e` flag tells pip to install in _editable_ mode, meaning that you can
continue developing your package on your computer as you test it without
re-installing it each time.

Then, in a Python shell or Jupyter Notebook, import your package and call the
function.

```py
>>> from example.refraction import snell
>>> import numpy as np
>>> snell(np.pi/4, 1.00, 1.33)
1.2239576240104186
```

The docstring can be viewed with `help()`.

```py
>>> help(snell)
```

Or, in Jupyter or Python, use `?` as a shortcut.

```py
In [1]: snell?
```

For more about packaging, also see our [packaging guide][].

<!-- prettier-ignore-start -->

[version control with git]: https://swcarpentry.github.io/git-novice/
[packaging guide]: {% link pages/guides/packaging_simple.md %}

<!-- prettier-ignore-end -->
