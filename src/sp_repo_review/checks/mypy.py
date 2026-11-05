from __future__ import annotations

__lazy_modules__ = ["tomllib"]

import tomllib
from typing import TYPE_CHECKING, Any

from . import mk_url

if TYPE_CHECKING:
    from importlib.resources.abc import Traversable


def _load_config(
    pyproject: dict[str, Any], package: Traversable, name: str
) -> dict[str, Any] | None:
    path = package.joinpath(f"{name}.toml")
    if path.is_file():
        with path.open("rb") as f:
            return tomllib.load(f)
    config: dict[str, Any] | None = pyproject.get("tool", {}).get(name)
    return config


def ty(pyproject: dict[str, Any], package: Traversable) -> dict[str, Any] | None:
    """
    Returns the ty configuration, or None if ty is not configured. A
    ``ty.toml`` file takes precedence over ``pyproject.toml``.
    """
    return _load_config(pyproject, package, "ty")


def pyrefly(pyproject: dict[str, Any], package: Traversable) -> dict[str, Any] | None:
    """
    Returns the Pyrefly configuration, or None if Pyrefly is not configured.
    A ``pyrefly.toml`` file takes precedence over ``pyproject.toml``.
    """
    return _load_config(pyproject, package, "pyrefly")


class MyPy:
    family = "mypy"


class MY100(MyPy):
    "Uses a type checker"

    requires = {"PY001"}
    url = mk_url("style")

    @staticmethod
    def check(
        pyproject: dict[str, Any],
        ty: dict[str, Any] | None,
        pyrefly: dict[str, Any] | None,
    ) -> bool:
        """
        Must have a `tool.mypy`, `tool.pyrefly`, or `tool.ty` section in
        `pyproject.toml`, or a `ty.toml` or `pyrefly.toml` file.
        """

        match pyproject:
            case {"tool": {"mypy": object()}}:
                return True
            case _:
                return ty is not None or pyrefly is not None


class MY101(MyPy):
    "Type checker in strict mode"

    requires = {"MY100"}
    url = mk_url("style")

    @staticmethod
    def check(
        pyproject: dict[str, Any],
        ty: dict[str, Any] | None,
        pyrefly: dict[str, Any] | None,
    ) -> bool | None:
        """
        Should opt into strict checking. For MyPy, set `strict` (true/false).
        For Pyrefly, set `preset` to `"strict"` or `"all"`. ty has no strict
        switch, so set the levels of rules in `[tool.ty.rules]`. Passes if any
        configured type checker is strict.

        ```toml
        [tool.mypy]
        strict = true
        ```
        """

        mypy = pyproject.get("tool", {}).get("mypy")
        if mypy is None and ty is None and pyrefly is None:
            return None

        match mypy:
            case {"strict": bool()}:
                return True
        match pyrefly:
            case {"preset": "strict" | "all"}:
                return True
        match ty:
            case {"rules": dict()}:
                return True
        return False


class MY102(MyPy):
    "MyPy show_error_codes deprecated"

    requires = {"MY100"}

    @staticmethod
    def check(pyproject: dict[str, Any]) -> bool | None:
        """
        Must not have `show_error_codes`. It is now the default, or you can
        use `hide_error_codes` with the reverse value instead (since MyPy v0.990).
        Skipped if MyPy is not configured.
        """

        match pyproject:
            case {"tool": {"mypy": {"show_error_codes": bool()}}}:
                return False
            case {"tool": {"mypy": object()}}:
                return True
            case _:
                return None


class MY103(MyPy):
    "MyPy warn unreachable"

    requires = {"MY100"}
    url = mk_url("style")

    @staticmethod
    def check(pyproject: dict[str, Any]) -> bool | None:
        """
        Must have `warn_unreachable` (true/false) to pass this check. There are
        occasionally false positives (often due to platform or Python version
        static checks), so it's okay to set it to false if you need to. But try
        it first - it can catch real bugs too. Skipped if MyPy is not configured.

        ```toml
        [tool.mypy]
        warn_unreachable = true
        ```
        """

        match pyproject:
            case {"tool": {"mypy": {"warn_unreachable": bool()}}}:
                return True
            case {"tool": {"mypy": object()}}:
                return False
            case _:
                return None


class MY104(MyPy):
    "MyPy enables ignore-without-code"

    requires = {"MY100"}
    url = mk_url("style")

    @staticmethod
    def check(pyproject: dict[str, Any]) -> bool | None:
        """
        Must have `"ignore-without-code"` in `enable_error_code = [...]`. This
        will force all skips in your project to include the error code, which
        makes them more readable, and avoids skipping something unintended.
        Skipped if MyPy is not configured.

        ```toml
        [tool.mypy]
        enable_error_code = ["ignore-without-code", "redundant-expr", "truthy-bool"]
        ```
        """

        match pyproject:
            case {"tool": {"mypy": {"enable_error_code": codes}}}:
                return "ignore-without-code" in codes
            case {"tool": {"mypy": object()}}:
                return False
            case _:
                return None


class MY105(MyPy):
    "MyPy enables redundant-expr"

    requires = {"MY100"}
    url = mk_url("style")

    @staticmethod
    def check(pyproject: dict[str, Any]) -> bool | None:
        """
        Must have `"redundant-expr"` in `enable_error_code = [...]`. This helps
        catch useless lines of code, like checking the same condition twice.
        Skipped if MyPy is not configured.

        ```toml
        [tool.mypy]
        enable_error_code = ["ignore-without-code", "redundant-expr", "truthy-bool"]
        ```
        """

        match pyproject:
            case {"tool": {"mypy": {"enable_error_code": codes}}}:
                return "redundant-expr" in codes
            case {"tool": {"mypy": object()}}:
                return False
            case _:
                return None


class MY106(MyPy):
    "MyPy enables truthy-bool"

    requires = {"MY100"}
    url = mk_url("style")

    @staticmethod
    def check(pyproject: dict[str, Any]) -> bool | None:
        """
        Must have `"truthy-bool"` in `enable_error_code = []`. This catches
        mistakes in using a value as truthy if it cannot be falsy. Skipped if
        MyPy is not configured.

        ```toml
        [tool.mypy]
        enable_error_code = ["ignore-without-code", "redundant-expr", "truthy-bool"]
        ```
        """

        match pyproject:
            case {"tool": {"mypy": {"enable_error_code": codes}}}:
                return "truthy-bool" in codes
            case {"tool": {"mypy": object()}}:
                return False
            case _:
                return None


class MY107(MyPy):
    "ty fails on warnings"

    requires = {"MY100"}
    url = mk_url("style")

    @staticmethod
    def check(ty: dict[str, Any] | None) -> bool | None:
        """
        Must set `error-on-warning` (true/false) in `[tool.ty.terminal]`. ty
        exits successfully on warnings by default, so CI does not fail on
        rules such as `unused-ignore-comment`. Skipped if ty is not configured.

        ```toml
        [tool.ty.terminal]
        error-on-warning = true
        ```
        """

        match ty:
            case None:
                return None
            case {"terminal": {"error-on-warning": bool()}}:
                return True
            case _:
                return False


class MY108(MyPy):
    "ty enables blanket-ignore-comment"

    requires = {"MY100"}
    url = mk_url("style")

    @staticmethod
    def check(ty: dict[str, Any] | None) -> bool | None:
        """
        Must enable the `blanket-ignore-comment` rule (or set `all` to a
        level other than `"ignore"`). This forces every `# ty: ignore` to list
        the rules it ignores, like MyPy's `ignore-without-code`. Skipped if ty
        is not configured.

        ```toml
        [tool.ty.rules]
        blanket-ignore-comment = "error"
        ```
        """

        match ty:
            case None:
                return None
            case {"rules": {"blanket-ignore-comment": str(level)}}:
                return level != "ignore"
            case {"rules": {"all": str(level)}}:
                return level != "ignore"
            case _:
                return False


def repo_review_checks() -> dict[str, MyPy]:
    return {p.__name__: p() for p in MyPy.__subclasses__()}
