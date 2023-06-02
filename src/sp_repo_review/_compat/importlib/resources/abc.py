from __future__ import annotations

import sys

if sys.version_info < (3, 11):
    from importlib.abc import Traversable
else:
    from importlib.resources.abc import Traversable


__all__ = ["Traversable"]


def __dir__() -> list[str]:
    return __all__
