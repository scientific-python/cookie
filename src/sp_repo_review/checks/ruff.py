from __future__ import annotations

from typing import Any, ClassVar, Protocol

from .._compat.importlib.resources.abc import Traversable

## R0xx: Ruff general
## R1xx: Ruff checks


class Ruff:
    family = "ruff"
    requires = {"PY001"}


class R001(Ruff):
    "Has Ruff config"

    @staticmethod
    def check(pyproject: dict[str, Any]) -> bool:
        """
        Must have `tool.ruff` section in `pyproject.toml`. Other forms of
        configuration are not supported by this check.
        """

        match pyproject:
            case {"tool": {"ruff": object()}}:
                return True
            case _:
                return False


class R002(Ruff):
    "Target version must be set"
    requires = {"R001"}

    @staticmethod
    def check(pyproject: dict[str, Any]) -> bool:
        """
        Must select a minimum version to target. Affects pyupgrade,
        isort, and others.
        """

        match pyproject:
            case {"tool": {"ruff": {"target-version": str()}}}:
                return True
            case _:
                return False


class R003(Ruff):
    "src directory specified if used"

    requires = {"R001"}

    @staticmethod
    def check(pyproject: dict[str, Any], package: Traversable) -> bool | None:
        """
        Must specify `src` directory if it exists.
        ```toml
        src = ["src"]
        ```
        """
        if not package.joinpath("src").is_dir():
            return None

        match pyproject:
            case {"tool": {"ruff": {"src": list(x)}}}:
                return "src" in x
            case _:
                return False


class RuffMixin(Protocol):
    code: ClassVar[str]
    name: ClassVar[str]


class R1xx(Ruff):
    family = "ruff"
    requires = {"R001"}

    @classmethod
    def check(cls: type[RuffMixin], pyproject: dict[str, Any]) -> bool:
        """
        Must select the {cls.name} `{cls.code}` checks. Recommended:
        ```toml
        select = ["{cls.code}"]  # {cls.name}
        ```
        """

        match pyproject:
            case {"tool": {"ruff": {"select": list(x)}}} | {
                "tool": {"ruff": {"extend-select": list(x)}}
            }:
                return cls.code in x
            case _:
                return False


class R101(R1xx):
    "Bugbear must be selected"
    code = "B"
    name = "flake8-bugbear"


class R102(R1xx):
    "isort must be selected"
    code = "I"
    name = "isort"


class R103(R1xx):
    "pyupgrade must be selected"
    code = "UP"
    name = "pyupgrade"


def repo_review_checks() -> dict[str, Ruff]:
    base_classes = set(Ruff.__subclasses__()) - {R1xx}
    r1xx_classes = set(R1xx.__subclasses__())
    repo_review_checks = base_classes | r1xx_classes
    return {p.__name__: p() for p in repo_review_checks}
