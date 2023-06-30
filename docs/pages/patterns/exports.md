---
layout: page
title: Exports
permalink: /patterns/exports/
nav_order: 1
parent: Patterns
---

{% include toc.html %}

# Exports

What objects in a module can you use? One common convention is that starting a
name with a single underscore makes it "private" (though really "hidden" might
be a better term for how it's usually handled - most tools hide these objects
from auto-complete unless you start typing an `_`).

Naming anything you don't expect outside users to use in this way is a good
practice. In practical terms for a library author, it means you can modify or
remove any `_*` objects without worrying about who it might break. And for a
library user, try to never use anything starting with a single `_`, as that
could be changed at any time.

However, this convention has limits. What about imports? You usually don't (and
shouldn't) rename your imports. But they don't start with an underscore, so does
that make them public? Even `from __future__ import anotations` will add an
`annotations` object, publicly visible, to your project!

A second solution sometimes attempted is deleting things after using them. This
can cause surprising problems in some cases, though, due to Python's late
binding. It's also easy to forget to delete something like an import, due to the
fact the `del` statements are at the end of the module, far away from the usage.

## Setting all

The solution to this is the `__all__` attribute. This is a public declaration of
your exported API. It looks like this:

```python
__all__ = ["object1", "Class1", "some_reexport"]
```

Setting this does several things:

- It controls what is imported if a user does `from module import *`.
- It provides a human readable list of the module's public API without looking
  at the entire file (ideally place it near the top of the file).
- It informs static tools like type checkers about the public API, including
  re-exports of things you import.
- It _can_ be used to control what `dir(module)` (and therefore tab completion)
  sees.

If you want to improve tab completion / `dir()` calls, you can add this small
boilerplate function to your modules:

```python
def __dir__() -> list[str]:
    return __all__
```

This causes tab completion to only show your public API! You can still access
everything in the module, it just won't be shown to the user.

{: .warning }

This `__dir__()` trick doesn't work very well on `__init__.py` modules, since
ideally you want submodules to be shown if they have been imported. It's best to
keep `__init__.py` modules minimal. It's tempting to import contents from your
submodules in `__init__.py`, but keep in mind importing any submodule always
runs all parent `__init__.py`s, so you'll likely take an import performance hit
and might have to deal with circular import issues in order to save a user a few
keystrokes.

There are some dynamic solutions to building your `__all__` variable without
having to list all the items in a list near the top of your file. However, you
lose several features doing so, such as the human readable list of module
contents and static type checker support.
