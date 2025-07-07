---
layout: page
title: Style & static checks
permalink: /guides/style/
nav_order: 8
parent: Topical Guides
custom_title: Style and static checks
---

{% include toc.html %}

# Style and static checks

## Pre-commit

{% rr PY006 %} Scientific Python projects often use [pre-commit][] to check code
style. It can be installed through `brew` (macOS) or `pip` (anywhere). There are
two modes to use it locally; you can check manually with `pre-commit run`
(changes only) or `pre-commit run --all-files` (all). You can also run
`pre-commit install` to add checks as a git pre-commit hook (which is where it
gets its name). It's worth trying, even if you've tried and failed to set up a
custom pre-commit hook before; it's quite elegant and does not add or commit the
changes, it just makes the changes and allows you to check and add them. You can
always override the hook with `-n`.

[pre-commit]: https://pre-commit.com

{% rr PC100 %} Here is a minimal `.pre-commit-config.yaml` file with some handy
options:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: "v5.0.0"
    hooks:
      - id: check-added-large-files
      - id: check-case-conflict
      - id: check-merge-conflict
      - id: check-symlinks
      - id: check-yaml
      - id: debug-statements
      - id: end-of-file-fixer
      - id: mixed-line-ending
      - id: name-tests-test
        args: ["--pytest-test-first"]
      - id: requirements-txt-fixer
      - id: trailing-whitespace
```

**Helpful tip**: Pre-commit runs top-to-bottom, so put checks that modify
content (like the several of the pre-commit-hooks above, or Black) above checks
that might be more likely to pass after the modification (like flake8).

**Keeping pinned versions fresh**: You can use `pre-commit autoupdate` to move
your tagged versions forward to the latest tags! Due to the design of
pre-commit's caching system, these _must_ point at fixed tags, never put a
branch here.

**Checking in CI**: You can have this checked and often automatically corrected
for you using [pre-commit.ci](https://pre-commit.ci). It will even update your
`rev:` versions every week or so if your checks update!

To use, just go to [pre-commit.ci](https://pre-commit.ci), click "Log in with
GitHub", click "Add an Installation" if adding for the first time for an org or
user, or "Manage repos on GitHub" for an existing installation, then add your
repository from the list in GitHub's interface.

Now there will be a new check, and pre-commit.ci will commit changes if the
pre-commit check made any changes. Note that there are a couple of missing
features: Docker based checks will not work (pre-commit.ci already runs in
docker), you cannot enable a `--manual` flag, so extra checks will not run, and
jobs should not download packages (use `additional-dependencies:` to add what
you need).

{% rr PC901 %} You can customize the pre-commit message with:

```yaml
ci:
  autoupdate_commit_msg: "chore: update pre-commit hooks"
```

## Format

{% rr PC110 %} [Black](https://black.readthedocs.io/en/latest/) is a popular
auto-formatter from the Python Software Foundation. One of the main features of
Black is that it is "opinionated"; that is, it is almost completely
unconfigurable. Instead of allowing you to come up with your own format, it
enforces one on you. While I am quite sure you can come up with a better format,
having a single standard makes it possible to learn to read code very fast - you
can immediately see nested lists, matching brackets, etc. There also is a
faction of developers that dislikes all auto-formatting tools, but inside a
system like pre-commit, auto-formatters are ideal. They also speed up the
writing of code because you can ignore formatting your code when you write it.
By imposing a standard, all scientific Python developers can quickly read any
package's code.

Also, properly formatted code has other benefits, such as if two developers make
the same change, they get the same formatting, and merge requests are easier.
The style choices in Black were explicitly made to optimize git diffs!

There are a _few_ options, mostly to enable/disable certain files, remove string
normalization, and to change the line length, and those go in your
`pyproject.toml` file.

{% tabs %} {% tab ruff Ruff-format %}

Ruff, the powerful Rust-based linter, has a formatter that is designed with the
help of some of the Black authors to look 99.9% like Black, but run 30x faster.
Here is the snippet to add the formatter to your `.pre-commit-config.yml`
(combine with the Ruff linter below):

```yaml
- repo: https://github.com/astral-sh/ruff-pre-commit
  rev: "v0.12.2"
  hooks:
    #  id: ruff-check would go here if using both
    - id: ruff-format
```

As you likely will be using Ruff if you follow this guide, the formatter is
recommended as well.

{% details You can add a Ruff badge to your repo as well %}

[![Code style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/format.json)](https://github.com/astral-sh/ruff)

```md
[![Code style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/format.json)](https://github.com/astral-sh/ruff)
```

```
.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/format.json
    :target: https://github.com/astral-sh/ruff
```

{% enddetails %}

{% endtab %} {% tab black Black %}

Here is the snippet to add Black to your `.pre-commit-config.yml`:

```yaml
- repo: https://github.com/psf/black-pre-commit-mirror
  rev: "25.1.0"
  hooks:
    - id: black
```

{% details You can add a Black badge to your repo as well %}

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

```md
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
```

```
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
```

{% enddetails %}

{% endtab %} {% endtabs %}

In _very_ specific situations, like when making a 2D array, you may want to
retain special formatting. After carefully deciding that it is a special use
case, you can use `# fmt: on` and `# fmt: off` around a code block to have it
keep custom formatting. _Always_ consider refactoring before you try this
option! Most of the time, you can find a way to make the Blacked code look
better by rewriting your code; factor out long unreadable portions into a
variable, avoid writing matrices as 1D lists, etc.

{% details Documentation / README snippets support %}

{% rr PC111 %} If you want Black used in your documentation, you can use
blacken-docs. This can even catch syntax errors in code snippets! It supports
markdown and restructured text. Note that because black is in
`additional_dependencies`, you'll have to keep it up to date manually.

```yaml
- repo: https://github.com/adamchainz/blacken-docs
  rev: "1.19.1"
  hooks:
    - id: blacken-docs
      additional_dependencies: [black==24.*]
```

{% enddetails %}

## Ruff

{% rr PC190 %} [Ruff][] [(docs)][ruff docs] is a Python code linter and
autofixer that replaces many other tools in the ecosystem with a ultra-fast
(written in Rust), single zero-dependency package. All plugins are compiled in,
so you can't get new failures from plugins updating without updating your
pre-commit hook.

[ruff docs]: https://beta.ruff.rs
[ruff]: https://github.com/astral-sh/ruff

```yaml
- repo: https://github.com/astral-sh/ruff-pre-commit
  rev: "v0.12.2"
  hooks:
    - id: ruff-check
      args: ["--fix", "--show-fixes"]
```

{% rr PC192 %} The hook is named `ruff-check`. {% rr PC191 %} The `--fix`
argument is optional, but recommended, since you can inspect and undo changes in
git. `--show-fixes` is highly recommended if `--fix` is present, otherwise it
won't tell you what or why it fixed things.

{% rr RF001 %} Ruff is configured in your `pyproject.toml`. Here's an example:

```toml
[tool.ruff.lint]
extend-select = [
  "ARG",      # flake8-unused-arguments
  "B",        # flake8-bugbear
  "C4",       # flake8-comprehensions
  "EM",       # flake8-errmsg
  "EXE",      # flake8-executable
  "FURB",     # refurb
  "G",        # flake8-logging-format
  "I",        # isort
  "ICN",      # flake8-import-conventions
  "NPY",      # NumPy specific rules
  "PD",       # pandas-vet
  "PGH",      # pygrep-hooks
  "PIE",      # flake8-pie
  "PL",       # pylint
  "PT",       # flake8-pytest-style
  "PTH",      # flake8-use-pathlib
  "PYI",      # flake8-pyi
  "RET",      # flake8-return
  "RUF",      # Ruff-specific
  "SIM",      # flake8-simplify
  "T20",      # flake8-print
  "UP",       # pyupgrade
  "YTT",      # flake8-2020
]
ignore = [
  "PLR09",    # Too many <...>
  "PLR2004",  # Magic value used in comparison
]
typing-modules = ["mypackage._compat.typing"]
isort.required-imports = ["from __future__ import annotations"]

[tool.ruff.lint.per-file-ignores]
"tests/**" = ["T20"]
```

Ruff [provides dozens of rule sets](https://beta.ruff.rs/docs/rules/); you can
select what you want from these. Like Flake8, plugins match by whole letter
sequences (with the special exception of pylint's "PL" shortcut), then you can
also include leading or whole error codes. Codes starting with 9 must be
selected explicitly, with at least the letters followed by a 9. You can also
ignore certain error codes via `ignore`. You can also set codes per paths to
ignore in `per-file-ignores`. If you don't like certain auto-fixes, you can
disable auto-fixing for specific error codes via `unfixable`.

There are other configuration options, such as `typing-modules`, which helps
apply typing-specific rules to a re-exported typing module (a common practice
for unifying typing and `typing_extensions` based on Python version). There's
also a file `exclude` set, which you can override if you are running this
entirely from pre-commit (default excludes include "build", so if you have a
`build` module or file named `build.py`, it would get skipped by default without
this).

The `src` list which tells it where to look for top level packages is no longer
needed if just set to `["src"]` in Ruff 0.6+. {% rr RF003 %}

{: .warning }

> If you don't use a `[project]` table (older setuptools or Poetry), then you
> should also set:
>
> ```toml
> target-version = "py39"
> ```
>
> This selects the minimum version you want to target (primarily for `"UP"` and
> `"I"`) {% rr RF002 %}

Here are some good error codes to enable on most (but not all!) projects:

- `E`, `F`, `W`: These are the standard flake8 checks, classic checks that have
  stood the test of time. Not required if you use `extend-select` (`W` not
  needed if you use a formatter)
- `B`: This finds patterns that are very bug-prone. {% rr RF101 %}
- `I`: This sorts your includes. There are multiple benefits, such as smaller
  diffs, fewer conflicts, a way to auto-inject `__future__` imports, and easier
  for readers to tell what's built-in, third-party, and local. It has a lot of
  configuration options, but defaults to a Black-compatible style.
  {% rr RF102 %}
- `ARG`: This looks for unused arguments. You might need to `# noqa: ARG001`
  occasionally, but it's overall pretty useful.
- `C4`: This looks for places that could use comprehensions, and can autofix
  them.
- `EM`: Very opinionated trick for error messages: it stops you from putting the
  error string directly in the exception you are throwing, producing a cleaner
  traceback without duplicating the error string.
- `ISC`: Checks for implicit string concatenation, which can help catch mistakes
  with missing commas. (May collide with formatter)
- `PGH`: Checks for patterns, such as type ignores or noqa's without a specific
  error code.
- `PL`: A set of four code groups that cover some (200 or so out of 600 rules)
  of Pylint.
- `PT`: Helps tests follow best pytest practices. A few codes are not ideal, but
  many are helpful.
- `PTH`: Want to move to using modern pathlib? This will help. There are some
  cases where performance matters, but otherwise, pathlib is easier to read and
  use.
- `RUF`: Codes specific to Ruff, including removing noqa's that aren't used.
- `T20`: Disallow `print` in your code (built on the assumption that it's a
  common debugging tool).
- `UP`: Upgrade old Python syntax to your `target-version`. {% rr RF103 %}
- `FURB`: From the refurb tool, a collection of helpful cleanups.
- `PYI`: Typing related checks

A few others small ones are included above, and there are even more available in
Ruff. You can use `ALL` to get them all, then ignore the ones you want to
ignore. New checks go into `--preview` before being activated in a minor
release.

{% details You can add a Ruff badge to your repo as well %}

[![Code style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json))](https://github.com/astral-sh/ruff)

```md
[![Code style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json))](https://github.com/astral-sh/ruff)
```

```rst
.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
    :target: https://github.com/astral-sh/ruff
```

{% enddetails %}

{% details Separate tools that Ruff replaces %}

### PyCln

[PyCln][] will clean up your imports if you have any that are not needed. There
is a Flake8 check for this, but it's usually nicer to automatically do the
cleanup instead of forcing a user to manually delete unneeded imports. If you
use the manual stage, it's opt-in instead of automatic.

```yaml
- repo: https://github.com/hadialqattan/pycln
  rev: "v2.5.0"
  hooks:
    - id: pycln
      args: [--all]
      stages: [manual]
```

### Flake8

[Flake8][] can check a collection of good practices for you, ranging from simple
style to things that might confuse or detract users, such as unused imports,
named values that are never used, mutable default arguments, and more. Unlike
black and some other tools, flake8 does not correct problems, it just reports
them. Some of the checks could have had automated fixes, sadly (which is why
Black is nice). Here is a suggested `.flake8` or `setup.cfg` to enable
compatibility with Black (flake8 does not support pyproject.toml configuration,
sadly):

```ini
[flake8]
extend-ignore = E203, E501
```

One recommended plugin for flake8 is `flake8-bugbear`, which catches many common
bugs. It is highly opinionated and can be made more so with the `B9` setting.
You can also set a max complexity, which bugs you when you have complex
functions that should be broken up. Here is an opinionated config:

```ini
[flake8]
max-complexity = 12
extend-select = B9
extend-ignore = E203, E501, E722, B950
```

(Error E722 is important, but it is identical to the activated B001.) Here is
the flake8 addition for pre-commit, with the `bugbear` plugin:

```yaml
- repo: https://github.com/pycqa/flake8
  rev: "7.3.0"
  hooks:
    - id: flake8
      additional_dependencies: [flake8-bugbear]
```

This _will_ be too much at first, so you can disable or enable any test by it's
label. You can also disable a check or a list of checks inline with
`# noqa: X###` (where you list the check label(s)). Over time, you can fix and
enable more checks. A few interesting plugins:

- [`flake8-bugbear`](https://pypi.org/project/flake8-bugbear/): Fantastic
  checker that catches common situations that tend to create bugs. Codes: `B`,
  `B9`
- [`flake8-docstrings`](https://pypi.org/project/flake8-docstrings/): Docstring
  checker. `--docstring-convention=pep257` is default, `numpy` and `google` also
  allowed.
- [`flake8-spellcheck`](https://pypi.org/project/flake8-spellcheck/): Spelling
  checker. Code: `SC`
- [`flake8-import-order`](https://pypi.org/project/flake8-import-order/):
  Enforces PEP8 grouped imports (you may prefer isort). Code: `I`
- [`pep8-naming`](https://pypi.org/project/pep8-naming/): Enforces PEP8 naming
  rules. Code: `N`
- [`flake8-print`](https://pypi.org/project/pep8-naming/): Makes sure you don't
  have print statements that sneak in. Code: `T`

{% details Flake8-print details %}

Having something verify you don't add a print statement by mistake is _very_
useful. A common need for the print checker would be to add it to a single
directory (`src` if you are following the convention recommended). You can do
the next best thing by removing directories and file just for this check (`T`)
in your flake8 config:

```ini
[flake8]
per-file-ignores =
    tests/*: T
    examples/*: T
```

{% enddetails %}

### YesQA

Over time, you can end up with extra "noqa" comments that are no longer needed.
This is a flake8 helper that removes those comments when they are no longer
required.

```yaml
- repo: https://github.com/asottile/yesqa
  rev: "v1.5.0"
  hooks:
    - id: yesqa
```

You need to have the same extra dependencies as flake8. In YAML, you can save
the list given to yesqa and repeat it in flake8 using `&flake8-dependencies` and
`*flake8-dependencies` after the colon.

### isort

You can have your imports sorted automatically by [isort][]. This will sort your
imports, and is black compatible. One reason to have sorted imports is to reduce
merge conflicts. Another is to clarify where imports come from - standard
library imports are in a group above third party imports, which are above local
imports. All this is configurable, as well. To use isort, the following
pre-commit config will work:

[isort]: https://pycqa.github.io/isort/

```yaml
- repo: https://github.com/PyCQA/isort
  rev: "6.0.1"
  hooks:
    - id: isort
```

In order to use it, you need to add some configuration. You can add it to
`pyproject.toml` or classic config files:

```ini
[tool.isort]
profile = "black"
```

[isort]: https://pycqa.github.io/isort/

### PyUpgrade

Another useful tool is [PyUpgrade][], which monitors your codebase for "old"
style syntax. Most useful to keep Python 2 outdated constructs out, it can even
do some code updates for different versions of Python 3, like adding f-strings
when clearly better (please always use them, they are faster) if you set
`--py36-plus` (for example). This is a recommended addition for any project.

```yaml
- repo: https://github.com/asottile/pyupgrade
  rev: "v3.20.0"
  hooks:
    - id: pyupgrade
      args: ["--py39-plus"]
```

[pyupgrade]: https://github.com/asottile/pyupgrade

{: .note }

> If you set this to at least `--py37-plus`, you can add the annotations import
> by adding the following line to your isort pre-commit hook configuration:
>
> ```yaml
> args: ["-a", "from __future__ import annotations"]
> ```
>
> Also make sure isort comes before pyupgrade. Now when you run pre-commit, it
> will clean up your annotations to 3.7+ style, too!

{% enddetails %}

## Type checking

{% rr PC140 %} One of the most exciting advancements in Python in the last 10
years has been static type hints. Scientific Python projects vary in the degree
to which they are type-hint ready. One of the challenges for providing static
type hints is that it was developed in the Python 3 era and it really shines in
a Python 3.7+ codebase (due to `from __future__ import annotations`, which turns
annotations into strings and allows you to use future Python features in Python
3.7+ annotations as long as your type checker supports them). For now, it is
recommended that you make an attempt to support type checking through your
public API in the best way that you can (based on your supported Python
versions). Stub files can be used instead for out-of-line typing.
[MyPy](https://mypy.readthedocs.io/en/stable/) is suggested for type checking,
though there are several other good options to try, as well. If you have
built-in support for type checking, you need to add empty `py.typed` files to
all packages/subpackages to indicate that you support it.

Read more about type checking on the [dedicated page][mypy page].

The MyPy addition for pre-commit:

```yaml
- repo: https://github.com/pre-commit/mirrors-mypy
  rev: "v1.16.1"
  hooks:
    - id: mypy
      files: src
      args: []
```

You should always specify args, as the hook's default hides issues - it's
designed to avoid configuration, but you should add configuration. You can also
add items to the virtual environment setup for MyPy by pre-commit, for example:

```yaml
additional_dependencies: [attrs==23.1.0]
```

{% rr MY100 %} MyPy has a config section in `pyproject.toml` that looks like
this:

```ini
[tool.mypy]
files = "src"
python_version = "3.9"
strict = true
enable_error_code = ["ignore-without-code", "redundant-expr", "truthy-bool"]
warn_unreachable = true


# You can disable imports or control per-module/file settings here
[[tool.mypy.overrides]]
module = [ "numpy.*", ]
ignore_missing_imports = true
```

There are a lot of options, and you can start with only typing global code and
functions with at least one type annotation (the default) and enable more checks
as you go (possibly by slowly uncommenting items in the list above). You can
ignore missing imports on libraries as shown above, one section each. And you
can disable MyPy on a line with `# type: ignore`. One strategy would be to
enable `check_untyped_defs` first, followed by `disallow_untyped_defs` then
`disallow_incomplete_defs`. You can add these _per file_ by adding a
`# mypy: <option>` at the top of a file. You can also pass `--strict` on the
command line. `strict = true` is now allowed in config files, too
{% rr MY101 %}.

The extra strict options shown above, like `warn_unreachable` {% rr MY103 %},
and `ignore-without-code` {% rr MY104 %}, `redundant-expr` {% rr MY105 %}, and
`truthy-bool` {% rr MY106 %} can trigger too often (like on `sys.platform`
checks) and have to be ignored occasionally, but can find some significant logic
errors in your typing.

[mypy page]: {% link pages/guides/mypy.md %}

## Setuptools specific checks

If you use setuptools, these checks are useful:

{% details Setuptools-only checks %}

### Check-Manifest (setuptools only)

[Check-manifest](https://pypi.org/project/check-manifest/) is a fantastic,
highly recommended tool that verifies you have working SDists. You can install
it from PyPI. Run it on your repository and see what it says. If you want to
ignore files (like test folders, example folders, docs, etc) you can add these
into your `pyproject.toml` file:

```toml
[tool.check-manifest]
ignore = [
    ".travis.yml",
]
```

Add the following to your pre-commit config:

```yaml
- repo: https://github.com/mgedmin/check-manifest
  rev: "0.50"
  hooks:
    - id: check-manifest
```

If you use `setuptools_scm`, you might want to add:

```yaml
additional_dependencies: ["setuptools_scm[toml]"]
```

{% details If this is too slow: %}

**Warning**: For a complex package, this may be slow. You can optionally set
`stages: [manual]` just below the id, and then only run this explicitly
(probably in CI only). In GHA, you should enable the manual stage, which will
run all checks:

```yaml
- uses: pre-commit/action@v3.0.1
  with:
    extra_args: --show-diff-on-failure --all-files --hook-stage manual
```

{% enddetails %}

### Setup.cfg format (setuptools only)

There is a tool that keeps your `setup.cfg` organized, and makes sure that
important parts (like Python classifiers) are in sync. This tool,
`setup-cfg-fmt`, has native support for pre-commit:

```yaml
- repo: https://github.com/asottile/setup-cfg-fmt
  rev: "v2.8.0"
  hooks:
    - id: setup-cfg-fmt
      args: [--include-version-classifiers, --max-py-version=3.12]
```

Make sure you list the highest version of Python you are testing with here.

{% enddetails %}

## Spelling

{% rr PC160 %} You can and should check for spelling errors in your code too. If
you want to add this, you can use [codespell][] for common spelling mistakes.
Unlike most spell checkers, this has a list of mistakes it looks for, rather
than a list of "valid" words. To use:

```yaml
- repo: https://github.com/codespell-project/codespell
  rev: "v2.4.1"
  hooks:
    - id: codespell
      additional_dependencies:
        - tomli; python_version<'3.11'
```

You can list allowed spellings in a comma separated string passed to `-L` (or
`--ignore-words-list` - usually it is better to use long options when you are
not typing things live). The example below will allow "Big Sur" and "ND". Here's
an example of `pyproject.toml` configuration:

```ini
[tool.codespell]
ignore-words-list = ["sur", "nd"]
```

You can also add the `-w` flag to have it automatically correct errors - this is
very helpful to quickly make corrections if you have a lot of them when first
adding the check. `uvx codespell -w` will quickly correct all non-hidden files.

You can also use a local pygrep check to eliminate common capitalization errors,
such as the one below:

```yaml
- repo: local
  hooks:
    - id: disallow-caps
      name: Disallow improper capitalization
      language: pygrep
      entry: PyBind|Numpy|Cmake|CCache|Github|PyTest
      exclude: .pre-commit-config.yaml
```

## PyGrep hooks

{% rr PC170 %} This is a repository with a
[collection of pre-commit extra hooks](https://github.com/pre-commit/pygrep-hooks)
that protect against some common, easy to detect, mistakes. You can pick and
choose the hooks you want from the repo; here are some common ones for
Restructured Text:

```yaml
- repo: https://github.com/pre-commit/pygrep-hooks
  rev: "v1.10.0"
  hooks:
    - id: rst-backticks
    - id: rst-directive-colons
    - id: rst-inline-touching-normal
```

If you want to add specific type ignores, see
[mypy_clean_slate](https://github.com/geo7/mypy_clean_slate) for a tool that
will add the specific ignores for you. You'll need to remove the existing type
ignores (`git ls-files '*.py' | xargs sed -i '' 's/ # type: ignore//g'`), copy
the pre-commit output (with `--show-error-codes` in mypy's args) to a file
called `mypy_error_report.txt`, then run `pipx run mypy_clean_slate -a`.

[codespell]: https://github.com/codespell-project/codespell

{: .note }

> Note that if you are not using Ruff's "PGH" code, there are `python-*` hooks
> also:
>
> ```yaml
> - id: python-check-blanket-noqa
> - id: python-check-blanket-type-ignore
> - id: python-no-log-warn
> - id: python-no-eval
> - id: python-use-type-annotations
> ```

## Clang-format (C++ only)

If you have C++ code, you should have a `.clang-format` file and use the
following pre-commit config:

```yaml
- repo: https://github.com/pre-commit/mirrors-clang-format
  rev: "v20.1.7"
  hooks:
    - id: clang-format
      types_or: [c++, c, cuda]
```

This will use 1-2 MB binary wheels from PyPI on all common platforms. You can
generated such a file using
`pipx run clang-format -style=llvm -dump-config > .clang-format`.

## Shellcheck (shell scripts only)

If you have shell scripts, you can protect against common mistakes using
[shellcheck](https://github.com/koalaman/shellcheck).

```yaml
- repo: https://github.com/shellcheck-py/shellcheck-py
  rev: "v0.10.0.1"
  hooks:
    - id: shellcheck
```

## Prettier

{% rr PC180 %} The [prettier](https://prettier.io) tool can format a large
number of different file types. An example of usage:

```yaml
- repo: https://github.com/rbubley/mirrors-prettier
  rev: "v3.6.2"
  hooks:
    - id: prettier
      types_or: [yaml, markdown, html, css, scss, javascript, json]
```

Since this formats a variety of very common file types (like `.html`, `.md`,
`.yaml`, `.js`, and `.json`), you will usually want to provide a `types_or`
setting (shown above) with the files you are interested in auto-formatting. You
can try it without the `types_or` first to see what it can do. Special markups
in html/markdown files might clash with auto-formatting - check to verify your
files are supported. This check runs using node, but pre-commit handles this for
you.

If you have a .editor-config file, prettier will respect the rules in it. You
can also specify [a config file](https://prettier.io/docs/en/configuration.html)
for prettier, or pass options to `args:` in pre-commit. One such option is
[`--prose-wrap`](https://prettier.io/docs/en/options.html#prose-wrap), which can
be set to `"never"` or `"always"` to have prettier reflow text. You can turn off
prettier for blocks with
[comments depending on language](https://prettier.io/docs/en/ignore.html).

## Schema validation

There are two tools, both based on JSON Schema, that you can use to validate
various configuration files. The first, [validate-pyproject][], validates your
`pyproject.toml` file. By default, it checks the standards-defined sections
(`build-system` and `project`), along with `tool.setuptools`. There are also
plugins for some other tools, like `scikit-build-core` and `cibuildwheel`. You
can even get all [SchemaStore][]'s plugins with the
[validate-pyproject-schema-store][] plugin. Using it looks like this:

```yaml
- repo: https://github.com/abravalheri/validate-pyproject
  rev: "v0.24.1"
  hooks:
    - id: validate-pyproject
      additional_dependencies: ["validate-pyproject-schema-store[all]"]
```

You can also validate various other types of files with [check-jsonschema][]. It
supports a variety of common files built-in ([see the docs][cjs-common]) like
various CI configuration files. You can also write/provide your own schemas and
validate using those - [SchemaStore][] provides a few hundred different common
schemas, and you can load them via URL. It work on JSON, YAML, and TOML.

```yaml
- repo: https://github.com/python-jsonschema/check-jsonschema
  rev: "0.33.2"
  hooks:
    - id: check-dependabot
    - id: check-github-workflows
    - id: check-readthedocs
```

## Pylint (noisy)

Pylint is very opinionated, with a high signal-to-noise ratio. However, by
limiting the default checks or by starting off a new project using them, you can
get some very nice linting, including catching some problematic code that
otherwise is hard to catch. Pylint is generally not a good candidate for
pre-commit, since it needs to have your package installed - it is less static of
check than Ruff or Flake8. Here is a suggested `pyproject.toml` entry to get you
started:

```toml
[tool.pylint]
py-version = "3.9"
jobs = "0"
reports.output-format = "colorized"
similarities.ignore-imports = "yes"
messages_control.enable = ["useless-suppression"]
messages_control.disable = [
  "design",
  "fixme",
  "line-too-long",
  "wrong-import-position",
]
```

And a noxfile entry:

```python
@nox.session
def pylint(session: nox.Session) -> None:
    session.install("-e.")
    session.install("pylint>=3.2")
    session.run("pylint", "<your package>", *session.posargs)
```

And you can add this to your GitHub Actions using
`run: pipx run nox -s pylint -- --output-format=github`. You can replace
`<your package>` with the module name.

## Jupyter notebook support

### Ruff

Ruff natively supports notebooks. You no longer need to enable it, it's on by
default with Ruff 0.6+. If you want to control rules based on being notebooks,
you can just match with `**.ipynb` like any other file.

### Black

For Black, just make sure you use the `id: black-jupyter` hook instead of
`id: black`; that will also include notebooks.

### NBQA

You can adapt other tools to notebooks using
[nbQA](https://github.com/nbQA-dev/nbQA). However, check to see if the tool
natively supports notebooks first, several of them do now.

### Stripping output

You also might like the following hook, which cleans Jupyter outputs:

```yaml
- repo: https://github.com/kynan/nbstripout
  rev: "0.8.1"
  hooks:
    - id: nbstripout
```

<!-- prettier-ignore-start -->

[flake8]: https://github.com/pycqa/flake8
[pycln]: https://hadialqattan.github.io/pycln
[validate-pyproject]: https://validate-pyproject.readthedocs.io
[check-jsonschema]: https://check-jsonschema.readthedocs.io/en/latest/
[cjs-common]: https://check-jsonschema.readthedocs.io/en/latest/precommit_usage.html#supported-hooks
[schemastore]: https://schemastore.org

<!-- prettier-ignore-end -->

<script src="{% link assets/js/tabs.js %}"></script>
