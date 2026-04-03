"""
Copyright (c) 2022 Henry Schreiner. All rights reserved.

sp-repo-review: Review repos with a set of checks defined by plugins.
"""

from __future__ import annotations

__lazy_modules__ = [f"{__spec__.parent}._version"]

from ._version import version as __version__

__all__ = ["__version__"]
