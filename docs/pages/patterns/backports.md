---
layout: page
title: Backports
permalink: /patterns/backports/
nav_order: 2
parent: Patterns
---

{% include toc.html %}

# Backports

A lot of additions to Python come with backports for older Pythons. Here are a
few tips for using backports:

- A backport is a _very_ lightweight dependency, since one way to get rid of it
  is to just upgrade Python.
- A backport will stop being a dependency in the future, when you drop older
  Python versions.
- If a package made it into the standard library, it should be well designed,
  well documented, and likely to be something someone learns anyway.
- Backports can't be broken by a new version Python, since you aren't using the
  backport on a new version of Python.

The rules for using a backport are as follows:

## Conditional requirement

Add it conditionally to your requirements. This looks something like this:

```toml
[project]
dependencies = [
    "importlib_metadata>=4.6; python_version<'3.10'",
    "importlib_resources; python_version<'3.9'",
    "typing_extensions>=4.6; python_version<'3.11'",
]
```

## Conditional usage

Always use the backport conditionally, with the following idiom:

```python
import sys

if sys.version_info < (3, 10):
    import importlib_metadata as metadata
else:
    from importlib import metadata
```

Never use `try/except` for a backport. The idiom above has the following
advantages:

- The reason for the conditional import is expressed in code. You don't need to
  add a comment explaining that this is needed to support X.Y version of Python;
  it's there in the code for the reader to see.
- Static analysis tools like MyPy understand this check and will handle it
  correctly.
- Static autofixers like pyupgrade and Ruff's pyupgrade will automatically
  remove the useless branch when you bump your Python version. You can also
  manually look at the output of `git grep "sys.version_info"` to clean these
  up.
- You can select the specific version of Python to switch on, even if the import
  was available sooner. In this case, `import.metadata` was added in 3.8 but
  important fixes landed in 3.10.
- It matches your conditional requirements.

## Placement in a file

Placing all conditional backports in a common location is a nice practice.
Here's a suggestion: Place all imports inside `src/<package>/_compat`, in the
standard library structure. This provides very clean, searchable imports in your
codebase that look similar to the normal usage.

For example, you could have a file `src/<package>/_compat/typing.py` with
contents like this:

```python
from __future__ import annotations

import sys

if sys.version_info < (3, 10):
    from typing_extensions import TypeAlias
else:
    from typing import TypeAlias

if sys.version_info < (3, 11):
    from typing_extensions import Self, assert_never
else:
    from typing import Self, assert_never

__all__ = ["TypeAlias", "Self", "assert_never"]


def __dir__() -> list[str]:
    return __all__
```

Ruff needs to know if you are re-exporting `typing`/`typing_extensions`, so make
sure you add `typing-modules = ["<package>._compat.typing"]` to Ruff's config in
`pyproject.toml`.

## Typing dependencies

While it's not usually necessary, you can avoid the `typing_extensions` backport
at runtime by protecting the imports with `typing.TYPE_CHECKING`.
`typing_extensions` is a first-party backport and very commonly required, so
there's a good chance one of your dependencies is already pulling it. But if you
really, really want to keep dependencies minimal, you can do this in your typing
backport re-export file.

## Common backport packages

- `typing_extensions`: New features in `typing` are added here first.
- `importlib_metadata`: Added as `importlib.metadata` in 3.8, important updates
  in 3.10 (and no longer provisional).
- `importlib_resources`: Added as `importlib.resources` in 3.7, important
  updates in 3.9 (`files` added, which is the recommended public API!).
- `tomli`: Added as `tomllib` in 3.11. Likely to become important again when
  TOML 1.1 is released. (Note that `toml_w` is not in the stdlib.)
- `exceptiongroup`: A new builtin (`ExceptionGroup`) in 3.11.
- `tz-data`: A first-party PyPI version of `zoneinfo` from 3.9, though with more
  up-to-date timezone info.
