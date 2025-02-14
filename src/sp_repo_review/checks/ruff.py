from __future__ import annotations

from collections.abc import Generator
from typing import Any, ClassVar, Protocol

from .._compat import tomllib
from .._compat.importlib.resources.abc import Traversable
from . import mk_url

## R0xx: Ruff general
## R1xx: Ruff checks
## R2xx: Ruff deprecations


def merge(start: dict[str, Any], add: dict[str, Any]) -> dict[str, Any]:
    merged = start.copy()
    for key, value in add.items():
        merged[key] = (
            merge(start.get(key, {}), value) if isinstance(value, dict) else value
        )
    return merged


def ruff(pyproject: dict[str, Any], root: Traversable) -> dict[str, Any] | None:
    """
    Returns the ruff configuration, or None if the configuration doesn't exist.
    Respects ``ruff.toml`` and ``.ruff.toml`` in addition to
    ``pyproject.toml``. Respects the extend option.
    """
    paths = [root.joinpath(".ruff.toml"), root.joinpath("ruff.toml")]
    for path in paths:
        if path.is_file():
            with path.open("rb") as f:
                contents = tomllib.load(f)
            if contents.get("extend", "") == "pyproject.toml":
                extend = pyproject.get("tool", {}).get("ruff", {})
                return merge(extend, contents)
            return contents

    return pyproject.get("tool", {}).get("ruff", None)  # type: ignore[no-any-return]


class Ruff:
    family = "ruff"
    url = mk_url("style")
    requires = {"RF001"}


class RF001(Ruff):
    "Has Ruff config"

    requires = set()

    @staticmethod
    def check(ruff: dict[str, Any] | None) -> bool:
        """
        Must have `[tool.ruff]` section in `pyproject.toml` or
        `ruff.toml`/`.ruff.toml`.
        """

        return ruff is not None


class RF002(Ruff):
    "Target version must be set"

    @staticmethod
    def check(pyproject: dict[str, Any], ruff: dict[str, Any]) -> bool | str:
        """
        Must select a minimum version to target. Affects pyupgrade, isort, and
        others. Will be inferred from `project.requires-python`.
        """

        match pyproject:
            case {
                "project": {"requires-python": str()},
                "tool": {"ruff": {"target-version": object()}},
            }:
                return "You have both Ruff's `target-version` and `project.requires-python`. You only need the latter."
            case {"project": {"requires-python": str()}}:
                return True
            case _:
                return "target-version" in ruff


class RF003(Ruff):
    "src directory doesn't need to be specified anymore (0.6+)"

    @staticmethod
    def check(ruff: dict[str, Any], package: Traversable) -> bool | None:
        """
        Ruff now (0.6+) looks in the src directory by default. The src setting
        doesn't need to be specified if it's just set to `["src"]`.
        """

        if not package.joinpath("src").is_dir():
            return None

        match ruff:
            case {"src": ["src"]}:
                return False
            case _:
                return True


class RF1xxMixin(Protocol):
    code: ClassVar[str]
    name: ClassVar[str]


class RF1xx(Ruff):
    @classmethod
    def check(cls: type[RF1xxMixin], ruff: dict[str, Any]) -> bool:
        """
        Must select the {self.name} `{self.code}` checks. Recommended:

        ```toml
        [tool.ruff.lint]
        extend-select = [
          "{self.code}",  # {self.name}
        ]
        ```
        """

        match ruff:
            case (
                {"lint": {"select": list(x)} | {"extend-select": list(x)}}
                | {"select": list(x)}
                | {"extend-select": list(x)}
            ):
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


class RF2xxMixin(Protocol):
    @staticmethod
    def iter_check(ruff: dict[str, Any]) -> Generator[str, None, None]: ...


class RF2xx(Ruff):
    url = ""

    @classmethod
    def check(cls: type[RF2xxMixin], ruff: dict[str, Any]) -> str:
        return "\n\n".join(cls.iter_check(ruff))


class RF201(RF2xx):
    "Avoid using deprecated config settings"

    @staticmethod
    def iter_check(ruff: dict[str, Any]) -> Generator[str, None, None]:
        match ruff:
            case {"extend-unfixable": object()} | {
                "lint": {"extend-unfixable": object()}
            }:
                yield "`extend-unfixable` deprecated, use `unfixable` instead (identical)"
            case {"extend-ignore": object()} | {"lint": {"extend-ignore": object()}}:
                yield "`extend-ignore` deprecated, use `ignore` instead (identical)"
            case _:
                pass


RUFF_LINT = {
    "allowed-confusables",
    "dummy-variable-rgx",
    "explicit-preview-rules",
    "extend-fixable",
    "extend-ignore",
    "extend-per-file-ignores",
    "extend-safe-fixes",
    "extend-select",
    "extend-unfixable",
    "extend-unsafe-fixes",
    "external",
    "fixable",
    "flake8-annotations",
    "flake8-bandit",
    "flake8-bugbear",
    "flake8-builtins",
    "flake8-comprehensions",
    "flake8-copyright",
    "flake8-errmsg",
    "flake8-gettext",
    "flake8-implicit-str-concat",
    "flake8-import-conventions",
    "flake8-pytest-style",
    "flake8-quotes",
    "flake8-self",
    "flake8-tidy-imports",
    "flake8-type-checking",
    "flake8-unused-arguments",
    "ignore",
    "ignore-init-module-imports",
    "isort",
    "logger-objects",
    "mccabe",
    "pep8-naming",
    "per-file-ignores",
    "pycodestyle",
    "pydocstyle",
    "pyflakes",
    "pylint",
    "pyupgrade",
    "select",
    "task-tags",
    "typing-modules",
    "unfixable",
}

# exclude isn't the same - outer exclude avoids loading config files, so it
# might be desired.


class RF202(RF2xx):
    "Use (new) lint config section"

    @staticmethod
    def iter_check(ruff: dict[str, Any]) -> Generator[str, None, None]:
        for item in sorted(set(ruff) & RUFF_LINT):
            yield f"`{item}` should be set as `lint.{item}` instead"


def repo_review_checks() -> dict[str, Ruff]:
    classes = set(Ruff.__subclasses__()) - {RF1xx, RF2xx}
    classes |= set(RF1xx.__subclasses__())
    classes |= set(RF2xx.__subclasses__())
    return {p.__name__: p() for p in classes}
