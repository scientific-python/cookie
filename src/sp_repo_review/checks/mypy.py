from __future__ import annotations

from typing import Any

from . import mk_url


class MyPy:
    family = "mypy"


class MY100(MyPy):
    "Uses MyPy (pyproject config)"

    requires = {"PY001"}
    url = mk_url("style")

    @staticmethod
    def check(pyproject: dict[str, Any]) -> bool:
        """
        Must have `tool.mypy` section in `pyproject.toml`. Other forms of
        configuration are not supported by this check.
        """

        match pyproject:
            case {"tool": {"mypy": object()}}:
                return True
            case _:
                return False


class MY101(MyPy):
    "MyPy strict mode"

    requires = {"MY100"}
    url = mk_url("style")

    @staticmethod
    def check(pyproject: dict[str, Any]) -> bool:
        """
        Must have `strict = true` in the mypy config. MyPy is best with strict
        or nearly strict configuration. If you are happy with the strictness of
        your settings already, ignore this check.
        """

        match pyproject:
            case {"tool": {"mypy": {"strict": True}}}:
                return True
            case _:
                return False


class MY102(MyPy):
    "MyPy show error codes"

    requires = {"MY100"}
    url = mk_url("style")

    @staticmethod
    def check(pyproject: dict[str, Any]) -> bool:
        """
        Must have `show_error_codes = true`. This will print helpful error codes
        for users that clarify why something fails if you need to skip it.
        """

        match pyproject:
            case {"tool": {"mypy": {"show_error_codes": True}}}:
                return True
            case _:
                return False


class MY103(MyPy):
    "MyPy warn unreachable"

    requires = {"MY100"}
    url = mk_url("style")

    @staticmethod
    def check(pyproject: dict[str, Any]) -> bool:
        """
        Must have `warn_unreachable = true` to pass this check. There are
        occasionally false positives (often due to platform or Python version
        static checks), so it's okay to ignore this check. But try it first - it
        can catch real bugs too.
        """

        match pyproject:
            case {"tool": {"mypy": {"warn_unreachable": True}}}:
                return True
            case _:
                return False


class MY104(MyPy):
    "MyPy enables ignore-without-code"

    requires = {"MY100"}
    url = mk_url("style")

    @staticmethod
    def check(pyproject: dict[str, Any]) -> bool:
        """
        Must have `"ignore-without-code"` in `enable_error_code = [...]`. This
        will force all skips in your project to include the error code, which
        makes them more readable, and avoids skipping something unintended.
        """

        match pyproject:
            case {"tool": {"mypy": {"enable_error_code": list(codes)}}}:
                return "ignore-without-code" in codes
            case _:
                return False


class MY105(MyPy):
    "MyPy enables redundant-expr"

    requires = {"MY100"}
    url = mk_url("style")

    @staticmethod
    def check(pyproject: dict[str, Any]) -> bool:
        """
        Must have `"redundant-expr"` in `enable_error_code = [...]`. This helps
        catch useless lines of code, like checking the same condition twice.
        """

        match pyproject:
            case {"tool": {"mypy": {"enable_error_code": list(codes)}}}:
                return "redundant-expr" in codes
            case _:
                return False


class MY106(MyPy):
    "MyPy enables truthy-bool"

    requires = {"MY100"}
    url = mk_url("style")

    @staticmethod
    def check(pyproject: dict[str, Any]) -> bool:
        """
        Must have `"truthy-bool"` in `enable_error_code = []`. This catches
        mistakes in using a value as truthy if it cannot be falsey.
        """

        match pyproject:
            case {"tool": {"mypy": {"enable_error_code": list(codes)}}}:
                return "truthy-bool" in codes
            case _:
                return False


def repo_review_checks() -> dict[str, MyPy]:
    return {p.__name__: p() for p in MyPy.__subclasses__()}
