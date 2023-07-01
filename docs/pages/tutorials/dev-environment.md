---
layout: page
title: Intro to development
permalink: /tutorials/dev-environment/
nav_order: 1
parent: Tutorials
---

{% include toc.html %}

# Intro to development

In this section you will:

- Create an isolated software area ("virtual environment") to work in.
- Open a code editor.

## Development environment

If you want to work on Python software, you should _always_ have a virtual
environment, an area to install the software that is isolated from other
programs running on your system. A user may not always have one, but a developer
always should.

Why? You do not want to risk interfering with your main system environment, you
want full control over versions of libraries, and you want to avoid letting your
main environment "leak" in, causing you to not notice when you have extra
dependencies. Virtual environments are disposable---it's no big deal to just
delete one and start over---while it is very hard to clean up or update a main
system environment.

There are many (arguably _too_ many) ways to do this in Python. Any modern tool
should be fine, but here we recommend two options popular in the scientific
Python community. If you already use a different way, that's fine, use that.

### Option 1: Using pip

The most basic option is to use `venv`, which comes by default with Python.

```bash
python3 -m venv .venv
```

This creates a new virtual environment in a local folder, named `.venv`. You
only need to do this step once, per project, per machine you work on. Later, if
something about your software installation breaks and you want to start fresh,
you can simply delete this directory to remove all trace of the virtual
environment.

To activate the virtual environment, type:

{% tabs %} {% tab unix Linux/macOS %}

```bash
. .venv/bin/activate
```

{% endtab %} {% tab windows Windows %}

```bat
.venv\bin\Activate.bat
```

{% endtab %} {% endtabs %}

You need to do this step every time you open a new shell (i.e. Terminal, Command
Prompt) to work on your project. The `.` is short for `source`, which runs the
script `activate` in your current shell. This causes `pip` and `python` to work
within this new environment, isolated from system-wide packages. It adds a bit
of text to your prompt so you don't forget that you are in an environment.

The activation script installs a function `deactivate`; type that at any time to
leave the environment (or just close your shell).

{: .note-title }

> Optional Alternative
>
> Alternatively, you can use the `virtualenv` package, which has the same syntax
> as `venv` and is a little faster. Unlike `venv`, it is not built in to Python;
> it has to be installed as `pip install virtualenv`.

{: .highlight-title }

> For Advanced Users Using Custom Shells
>
> If you like a different shell, like fish, there are several `activate`
> scripts; the default one expects a bash-like shell.

### Option 2: Using conda

You can also develop in conda. This is an especially good option if:

- You want an easy way to choose a specific version of Python
- Your project will depend on complex software libraries that are not readily
  pip-installable

The creation of an environment looks like this:

```bash
conda create -n env_name python=3.11
```

You can use `-n name` or `-p path` to specify the environment by name or
location. The above assume you used a name, but just replace names with paths if
you choose a path.

To activate an environment:

```bash
conda activate env_name
```

To deactivate, use `conda deactivate`, or leave your shell.

## Choosing an Editor

Any plain text editor will serve our purposes for this guide. Bare bones editors
like Notepad or `nano` will do the job. More feature-rich Integrated Development
Environments (IDEs) such as [PyCharm][] or [Visual Studio Code][] can provide
useful additions, such as syntax highlighting, tab completion, and more. Classic
text editors like [`vim`][] and [`emacs`][] can do the same with configuration,
and are often readily available on shared institutional systems.

You can instruct an IDE to use the virtual environment (pip or conda) that you
set up. Setting up an IDE takes extra time but often provides tools (like smart
renaming) that are useful, and if you use type hints, will probably pay for the
setup time quite quickly when developing.

[pycharm]: https://www.jetbrains.com/pycharm/
[visual studio code]: https://code.visualstudio.com/
[`vim`]: https://www.vim.org/
[`emacs`]: https://www.gnu.org/software/emacs/

<script src="{% link assets/js/tabs.js %}"></script>
