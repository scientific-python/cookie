---
layout: page
title: Intro to development
permalink: /tutorials/dev-environment/
nav_order: 1
parent: Tutorials
---

{% include toc.html %}

It is generally advisable for packages in the scientific Python ecosystem to try to
follow best practices in the community for development and deployment. The following
outlines the basics for setting up a development environment. It is recommended as a
basis for `CONTRIBUTING.md` or `.github/CONTRIBUTING.md` in the packages.

<details><summary>CONTRIBUTING.md template (click to expand)</summary>
<pre>
See the [Scientific Python Developer introduction][scientific-python-dev-intro] for a
detailed description of best practices for developing Scientific Python packages.

[scientific-python-dev-intro]: https://scientific-python.org/developer/intro

# Setting up a development environment

You can set up a development environment by running:

```bash
python3 -m venv .env
source ./.env/bin/activate
pip install -v -e .[dev]
```

# Post setup

You should prepare pre-commit, which will help you by checking that commits
pass required checks:

```bash
pip install pre-commit # or brew install pre-commit on macOS
pre-commit install # Will install a pre-commit hook into the git repo
```

You can also/alternatively run `pre-commit run` (changes only) or
`pre-commit run --all-files` to check even without installing the hook.

# Testing

Use pytest to run the unit checks:

```bash
pytest
```

</pre>
</details>

## Development environment: Pip

If you want to work on Python software, you should _always_ have a virtual
environment. A user may not always have one, but a developer always should.
You do not want to risk breaking your main system environment, you want full
control over versions of libraries, and you want to avoid "leaking" your main
environment in, causing you to not notice when you have extra dependencies.
Virtual environments are disposable, while it is very hard to cleanup or update
a main system environment.

Any common modern system to create environments should be fine. Here is the
most basic one, `venv`, that comes by default with Python 3:

```bash
python3 -m venv .env
```

This creates a new virtual environment in a local folder, named `.env`. There
are a few options, but usually they are not necessary. If you don't mind a
(very common) dependency, you can use the `virtualenv` package, which has the
same syntax, is a little faster, and works in Python 2 as well.

To activate the virtual environment, type:

```bash
. .env/bin/activate
```

The `.` is short for `source`, which runs the script `activate` in your current
shell. If you like a different shell, like fish, there are several activate
scripts; the default one expects a bash-like shell. You need to run this
command any time you want to use the development environment. The activation
script installs a function `deactivate`; type that at any time to leave the
environment (or just close your shell). It also adds a bit of text to your
prompt so you don't forget that you are in an environment.

Finally, you need to install the package. Most packages support several extra
options when installing; for development, you may want `[test]`, `[dev]`, or
`[all]` or `[complete]` (packages use different conventions, check). Here is an
example:

```bash
pip install -e .[dev]
```

The `-e` installs the package in "editable" mode, meaning the files are not copied to
your site-packages folder, so you can edit and work with the package locally. You need
to rerun `pip install -e .` if there are binary components and you edit those.

Never edit your `PATH` or `PYTHONPATH` manually, or depend on the current
directory for library development.

> <h4 style="no_toc">Warning:</h4>
>
> _Always_ use pip to install, do not call `python setup.py` directly for
> building or installing. Pip inserts shims into setup.py to fix common issues
> and enable features like PEP 517/518 builds. The only time you directly call
> setup.py is when making sdists, and even then there are hacks involved.
>
> Remember a "normal" user will always use pip. You need to simulate that in
> development.

## Development environment: Conda

You can also develop in Conda. For some packages, such as those that work with ROOT,
you need to be using Conda, and it is a great way to have control over the version
of Python you are using. If so, then the creation of an environment looks like this:

```bash
conda create -n env_name python=3.8
```

You can use `-n name` or `-p path` to specify the environment by name or
location. The following assume you used a name, but just replace names with
paths if you choose a path.

Some packages provide an environment file, either for CI or developer use. If they
do, you can use `conda env create -f filename.yml` to create (or `update` to update)
the provided environment. You can override name or location as above. And if the file
is called `environment.yml`, you can leave off the `-f filename` entirely.

To activate an environment:

```bash
conda activate env_name
```

To deactivate, use `conda deactivate`, or leave your shell.

> <h4 style="no_toc">Warning:</h4>
>
> Building binary components for conda packages takes some care. In general, if
> there are any binary components, you must use conda-forge's build system to
> provide binaries to users.

## Using an IDE

IDE's can provide useful additions, such as extended type checking, type aware
completions, and more. We currently do not provide IDE files in our
repositories, but PyCharm community edition is suggested by some of our members
for developers looking for an IDE. It includes an extension, IdeaVIM, for VIM
emulation for users used to that editor. Setting up an IDE takes extra time
but often provides tools (like smart renaming) that are useful, and if you use
type hints, will probably pay for the setup time quite quickly when developing.

You can instruct PyCharm to use the virtual environment (regular or Conda) that you
set up, or it can follow the environment.yml or requirements to make one for you.
