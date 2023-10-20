from __future__ import annotations

from typing import Any, ClassVar, Protocol

from .._compat.importlib.resources.abc import Traversable
from . import mk_url

## R0xx: Ruff general
## R1xx: Ruff checks


class Ruff:
    family = "ruff"
    url = mk_url("style")


class RF001(Ruff):
    "Has Ruff config"
    requires = {"PY001"}

    @staticmethod
    def check(pyproject: dict[str, Any]) -> bool:
        """
        Must have `[tool.ruff]` section in `pyproject.toml`. Other forms of
        configuration are not supported by this check.
        """

        match pyproject:
            case {"tool": {"ruff": object()}}:
                return True
            case _:
                return False


class RF002(Ruff):
    "Target version must be set"
    requires = {"RF001"}

    @staticmethod
    def check(pyproject: dict[str, Any]) -> bool:
        """
        Must select a minimum version to target. Affects pyupgrade, isort, and
        others. Will be inferred from `project.requires-python`.
        """

        match pyproject:
            case {"tool": {"ruff": {"target-version": str()}}}:
                return True
            case {"project": {"requires-python": str()}}:
                return True
            case _:
                return False


class RF003(Ruff):
    "src directory specified if used"

    requires = {"RF001"}

    @staticmethod
    def check(pyproject: dict[str, Any], package: Traversable) -> bool | None:
        """
        Must specify `src` directory if it exists.

        ```toml
        [tool.ruff]
        src = ["src"]
        ```
        """
        if not package.joinpath("src").is_dir():
            return None

        match pyproject["tool"]["ruff"]:
            case {"src": list(x)}:
                return "src" in x
            case _:
                return False


class RF004(Ruff):
    "Deprecated config options should be avoided"

    requires = {"RF001"}
    url = ""

    @staticmethod
    def check(pyproject: dict[str, Any]) -> str:
        match pyproject["tool"]["ruff"]:
            case {"extend-unfixable": object()}:
                return "`extend-unfixable` deprecated, use `unfixable` (identical)"
            case {"extend-ignore": object()}:
                return "`extend-ignore` deprecated, use `ignore` (identical)"
            case _:
                return ""


class RuffMixin(Protocol):
    code: ClassVar[str]
    name: ClassVar[str]


class RF1xx(Ruff):
    family = "ruff"
    requires = {"RF001"}

    @classmethod
    def check(cls: type[RuffMixin], pyproject: dict[str, Any]) -> bool:
        """
        Must select the {self.name} `{self.code}` checks. Recommended:

        ```toml
        [tool.ruff]
        select = [
          "{self.code}",  # {self.name}
        ]
        ```
        """

        match pyproject["tool"]["ruff"]:
            case {"select": list(x)} | {"extend-select": list(x)}:
                return cls.code in x or "ALL" in x
            case _:
                return False


class RF101(RF1xx):
    "Bugbear must be selected"
    code = "B"
    name = "flake8-bugbear"


class RF102(RF1xx):
    "isort must be selected"
    code = "I"
    name = "isort"


class RF103(RF1xx):
    "pyupgrade must be selected"
    code = "UP"
    name = "pyupgrade"


def repo_review_checks() -> dict[str, Ruff]:
    base_classes = set(Ruff.__subclasses__()) - {RF1xx}
    rf1xx_classes = set(RF1xx.__subclasses__())
    repo_review_checks = base_classes | rf1xx_classes
    return {p.__name__: p() for p in repo_review_checks}
