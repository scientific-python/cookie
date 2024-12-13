from __future__ import annotations

from typing import Any

from .._compat.importlib.resources.abc import Traversable
from . import mk_url

# PY: Python Project
## 0xx: File existence


class General:
    family = "general"


class PY001(General):
    "Has a pyproject.toml"

    url = mk_url("packaging-simple")

    @staticmethod
    def check(package: Traversable) -> bool:
        """
        All projects should have a `pyproject.toml` file to support a modern
        build system and support wheel installs properly.
        """
        return package.joinpath("pyproject.toml").is_file()


class PY002(General):
    "Has a README.(md|rst) file"

    url = mk_url("packaging-simple")

    @staticmethod
    def check(root: Traversable) -> bool:
        "Projects must have a readme file"
        return (
            root.joinpath("README.md").is_file()
            or root.joinpath("README.rst").is_file()
        )


class PY003(General):
    "Has a LICENSE* file"

    url = mk_url("packaging-simple")

    @staticmethod
    def check(package: Traversable) -> bool:
        "Projects must have a license"
        spellings = ("LICENSE", "LICENCE", "COPYING")
        return any(
            p.name.startswith(spelling)
            for p in package.iterdir()
            for spelling in spellings
        )


class PY004(General):
    "Has docs folder"

    url = mk_url("packaging-simple")

    @staticmethod
    def check(package: Traversable) -> bool:
        "Projects must have documentation in a folder called docs (disable if not applicable)"
        return (
            len([p for p in package.iterdir() if p.is_dir() and p.name == "docs"]) > 0
        )


class PY005(General):
    "Has tests folder"

    url = mk_url("packaging-simple")

    @staticmethod
    def check(package: Traversable) -> bool:
        "Projects must have a folder called `test*` or `src/*/test*`"
        # Out-of-source tests
        if (
            len(
                [
                    p
                    for p in package.iterdir()
                    if p.is_dir() and p.name.startswith("test")
                ]
            )
            > 0
        ):
            return True

        # In-source tests
        src = package.joinpath("src")
        if src.is_dir():
            for pkg in src.iterdir():
                if (
                    pkg.is_dir()
                    and len(
                        [
                            p
                            for p in pkg.iterdir()
                            if p.is_dir() and p.name.startswith("test")
                        ]
                    )
                    > 0
                ):
                    return True
        return False


class PY006(General):
    "Has pre-commit config"

    url = mk_url("style")

    @staticmethod
    def check(root: Traversable) -> bool:
        "Projects must have a `.pre-commit-config.yaml` file"
        return root.joinpath(".pre-commit-config.yaml").is_file()


class PY007(General):
    "Supports an easy task runner (nox, tox, pixi, etc.)"

    url = mk_url("tasks")

    @staticmethod
    def check(root: Traversable, pyproject: dict[str, Any]) -> bool:
        """
        Projects must have a `noxfile.py`, `tox.ini`, or
        `tool.hatch.envs`/`tool.spin`/`tool.tox` in `pyproject.toml` to encourage new
        contributors.
        """
        if root.joinpath("noxfile.py").is_file():
            return True
        if root.joinpath("tox.ini").is_file():
            return True
        if root.joinpath("pixi.toml").is_file():
            return True
        match pyproject.get("tool", {}):
            case {"hatch": {"envs": object()}}:
                return True
            case {"spin": object()}:
                return True
            case {"tox": object()}:
                return True
            case {"pixi": {"tasks": {}}}:
                return True
            case {"pixi": {"feature": feats}} if any(
                "tasks" in feat for feat in feats.values()
            ):
                return True
            case _:
                return False


def repo_review_checks() -> dict[str, General]:
    return {p.__name__: p() for p in General.__subclasses__()}
