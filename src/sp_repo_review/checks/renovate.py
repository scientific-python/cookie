# REN: Renovate Actions

from __future__ import annotations

__lazy_modules__ = ["json"]

import json
from typing import TYPE_CHECKING, Any

from . import mk_url

if TYPE_CHECKING:
    from .._compat.importlib.resources.abc import Traversable


SUPPORTED_RENOVATE_FILES = [
    "renovate.json",
    "renovate.jsonc",
    "renovate.json5",
    ".github/renovate.json",
    ".github/renovate.jsonc",
    ".github/renovate.json5",
    ".gitlab/renovate.json",
    ".gitlab/renovate.jsonc",
    ".gitlab/renovate.json5",
    ".renovaterc",
    ".renovaterc.json",
    ".renovaterc.jsonc",
    ".renovaterc.json5",
    # "package.json"  # Deprecated by Renovate
]


def renovate(root: Traversable) -> dict[str, Any]:
    renovate_paths = [root.joinpath(f) for f in SUPPORTED_RENOVATE_FILES]

    for renovate_path in renovate_paths:
        if renovate_path.is_file():
            with renovate_path.open() as f:
                try:
                    result: dict[str, Any] = json.load(f)
                except json.JSONDecodeError:
                    continue
                else:
                    return result
    return {}


class Renovate:
    family = "renovate"


class REN200(Renovate):
    """Maintained by Renovate"""

    requires = {"DEP200"}
    url = mk_url("gha-basic")

    @staticmethod
    def check(renovate: dict[str, Any]) -> bool | None:
        """
        All projects should have a renovate configuration file (`renovate.json` or other supported locations)
        to support dependency updates. Something like this:

        ```json
        {{
          "extends": ["config:recommended"]
        }}
        ```

        Renovate configurations in `package.json` are not supported.
        Configurations in `.jsonc` or `.json5` files are not fully supported.
        """
        if not renovate:
            return None
        return bool(renovate)


GHA_EXTENDS = {"config:recommended", "config:best-practices"}


class REN210(Renovate):
    """Maintains the GitHub action versions with Renovate"""

    requires = {"REN200"}
    url = mk_url("gha-basic")

    @staticmethod
    def check(renovate: dict[str, Any]) -> bool | None | str:
        """
        Ensures that Renovate is configured to maintain GitHub action versions.

        Checks for if the `github-actions` manager is enabled or if the Renovate config extends a known config (`config:recommended` or `config:best-practices`).
        """
        if (manager := renovate.get("github-actions", {})) and manager.get("enabled"):
            return True
        if extends := renovate.get("extends", []):
            if any(e in GHA_EXTENDS for e in extends):
                return True
            return f"Renovate config extends {extends}, but none are a known config: {', '.join(GHA_EXTENDS)}."
        return False


def repo_review_checks() -> dict[str, Renovate]:
    return {p.__name__: p() for p in Renovate.__subclasses__()}
