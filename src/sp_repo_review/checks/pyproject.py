from __future__ import annotations

import enum
from typing import TYPE_CHECKING, Any

from .._compat import tomllib
from . import mk_url

if TYPE_CHECKING:
    from configparser import ConfigParser

    from .._compat.importlib.resources.abc import Traversable


class PytestFile(enum.Enum):
    PYTEST_TOML = enum.auto()
    MODERN_PYPROJECT = enum.auto()
    LEGACY_PYPROJECT = enum.auto()
    NONE = enum.auto()


def pytest(
    pyproject: dict[str, Any], root: Traversable
) -> tuple[PytestFile, dict[str, Any]]:
    """
    Returns the pytest configuration, or None if the configuration doesn't exist.
    Respects toml configurations only.
    """
    paths = [root.joinpath("pytest.toml"), root.joinpath(".pytest.toml")]
    for path in paths:
        if path.is_file():
            with path.open("rb") as f:
                contents = tomllib.load(f)
            return (PytestFile.PYTEST_TOML, contents.get("pytest", {}))

    match pyproject:
        case {"tool": {"pytest": {"ini_options": config}}}:
            return (PytestFile.LEGACY_PYPROJECT, config)
        case {"tool": {"pytest": config}}:
            return (PytestFile.MODERN_PYPROJECT, config)
        case _:
            return (PytestFile.NONE, {})


def get_requires_python(
    pyproject: dict[str, Any], setupcfg: ConfigParser | None
) -> str | None:
    match pyproject:
        case {"project": {"requires-python": str() as requires}}:
            return requires
        case {
            "tool": {
                "poetry": {
                    "dependencies": {"python": str() as requires}
                    | {"version": str() as requires}
                }
            }
        }:
            return requires

    if setupcfg and (
        requires := setupcfg.get("options", "python_requires", fallback="")
    ):
        return requires
    return None


class PyProject:
    family = "pyproject"


class PP002(PyProject):
    "Has a proper build-system table"

    requires = {"PY001"}
    url = mk_url("packaging-simple")

    @staticmethod
    def check(pyproject: dict[str, Any]) -> bool:
        """
        Must have `build-system.requires` *and* `build-system.backend`. Both
        should be present in all modern packages.
        """

        match pyproject:
            case {"build-system": {"requires": list(), "build-backend": str()}}:
                return True
            case _:
                return False


class PP003(PyProject):
    "Does not list wheel as a build-dep"

    requires = {"PY001"}
    url = mk_url("packaging-classic")

    @staticmethod
    def check(pyproject: dict[str, Any]) -> bool:
        """
        Do not include `"wheel"` in your `build-system.requires`, setuptools
        does this via PEP 517 already. Setuptools will also only require this
        for actual wheel builds, and might have version limits.
        """

        match pyproject:
            case {"build-system": {"requires": req}}:
                return all(not r.startswith("wheel") for r in req)
            case _:
                return False


class PP004(PyProject):
    "Does not upper cap Python requires"

    url = mk_url("packaging-simple")

    @staticmethod
    def check(pyproject: dict[str, Any], setupcfg: ConfigParser | None) -> bool | None:
        """
        You should never upper cap your Python requirement. This is rarely correct, and
        tools like pip do not handle this properly even if it is correct. This field is used
        to back-solve. If you want to specify versions you've tested on, use classifiers. If
        you want to add a custom error message, add a build-type and/or runtime assert.
        """

        requires = get_requires_python(pyproject, setupcfg)
        if requires is not None:
            return "^" not in requires and "~=" not in requires and "<" not in requires

        return None


class PP005(PyProject):
    "Using SPDX project.license should not use deprecated trove classifiers"

    requires = {"PY001"}
    url = mk_url("packaging-simple")

    @staticmethod
    def check(pyproject: dict[str, Any]) -> bool | None:
        """
        If you use SPDX identifiers in `project.license`, then all the `License ::`
        classifiers are deprecated.

        See https://packaging.python.org/en/latest/specifications/core-metadata/#license-expression
        """
        match pyproject:
            case {"project": {"license": str(), "classifiers": classifiers}}:
                return all(not c.startswith("License ::") for c in classifiers)
            case {"project": {"license": str()}}:
                return True
            case _:
                return None


class PP006(PyProject):
    "The dev dependency group should be defined"

    requires = {"PY001"}
    url = mk_url("packaging-simple")

    @staticmethod
    def check(pyproject: dict[str, Any]) -> bool:
        """
        The `dev` dependency group should be defined so tools like uv will work.
        These are better than the old `extras` system for tests, docs, and other
        dependencies that are not needed for PyPI installs.

        ```toml
        [dependency-groups]
        dev = [ {{ include-group = "test" }} ]
        test = [ "pytest" ]
        ```
        """
        match pyproject:
            case {"dependency-groups": {"dev": list()}}:
                return True
            case _:
                return False


class PP301(PyProject):
    "Has pytest in pyproject"

    requires = set[str]()
    url = mk_url("pytest")

    @staticmethod
    def check(pytest: tuple[PytestFile, dict[str, Any]]) -> bool:
        """
        Must have a `[tool.pytest]` (pytest 9+) or `[tool.pytest.ini_options]`
        (pytest 6+) configuration section in pyproject.toml. If you must have it
        in ini format, ignore this check.  pytest.toml and .pytest.toml files
        (pytest 9+) are also supported.
        """

        loc, _ = pytest
        return loc is not PytestFile.NONE


class PP302(PyProject):
    "Sets a minimum pytest to at least 6 or 9"

    requires = {"PP301"}
    url = mk_url("pytest")

    @staticmethod
    def check(pytest: tuple[PytestFile, dict[str, Any]]) -> bool:
        """
        Must have a `minversion=`, and must be at least 6 (first version to
        support `pyproject.toml` ini configuration) or 9 (first version to
        support native configuration and toml config files).

        ```toml
        [tool.pytest.ini_options]
        minversion = "9"
        ```
        """
        loc, options = pytest
        minversion = 6 if loc is PytestFile.LEGACY_PYPROJECT else 9
        return (
            "minversion" in options
            and int(str(options["minversion"]).split(".", maxsplit=1)[0]) >= minversion
        )


class PP303(PyProject):
    "Sets the test paths"

    requires = {"PP301"}
    url = mk_url("pytest")

    @staticmethod
    def check(pytest: tuple[PytestFile, dict[str, Any]]) -> bool:
        """
        The `testpaths` setting should be set to a reasonable default.

        ```toml
        [tool.pytest.ini_options]
        testpaths = ["tests"]
        ```
        """
        _, options = pytest
        return "testpaths" in options


class PP304(PyProject):
    "Sets the log level in pytest"

    requires = {"PP301"}
    url = mk_url("pytest")

    @staticmethod
    def check(pytest: tuple[PytestFile, dict[str, Any]]) -> bool:
        """
        `log_level` should be set. This will allow logs to be displayed on
        failures.

        ```toml
        [tool.pytest.ini_options]
        log_level = "INFO"
        ```
        """
        _, options = pytest
        return "log_cli_level" in options or "log_level" in options


class PP305(PyProject):
    "Specifies strict xfail"

    requires = {"PP301"}
    url = mk_url("pytest")

    @staticmethod
    def check(pytest: tuple[PytestFile, dict[str, Any]]) -> bool:
        """
        `xfail_strict`, or if using pytest 9+, `strict_xfail` or `strict` should
        be set. You can manually specify if a check should be strict when
        setting each xfail.

        ```toml
        [tool.pytest.ini_options]
        xfail_strict = true
        ```
        """
        _, options = pytest
        return (
            "xfail_strict" in options
            or "strict_xfail" in options
            or "strict" in options
        )


class PP306(PyProject):
    "Specifies strict config"

    requires = {"PP301"}
    url = mk_url("pytest")

    @staticmethod
    def check(pytest: tuple[PytestFile, dict[str, Any]]) -> bool:
        """
        `--strict-config` should be in `addopts = [...]` or (pytest 9+)
        `strict_config` or `strict` should be set. This forces an error if a
        config setting is misspelled.

        ```toml
        [tool.pytest.ini_options]
        addopts = ["-ra", "--strict-config", "--strict-markers"]
        ```
        """
        _, options = pytest
        return (
            "strict" in options
            or "strict_config" in options
            or "--strict-config" in options.get("addopts", [])
        )


class PP307(PyProject):
    "Specifies strict markers"

    requires = {"PP301"}
    url = mk_url("pytest")

    @staticmethod
    def check(pytest: tuple[PytestFile, dict[str, Any]]) -> bool:
        """
        `--strict-markers` should be in `addopts = [...]` or (pytest 9+)
        `strict_markers` or `strict` should be set. This forces test markers to
        be specified in config, avoiding misspellings.

        ```toml
        [tool.pytest.ini_options]
        addopts = ["-ra", "--strict-config", "--strict-markers"]
        ```
        """
        _, options = pytest
        return (
            "strict" in options
            or "strict_markers" in options
            or "--strict-markers" in options.get("addopts", [])
        )


class PP308(PyProject):
    "Specifies useful pytest summary"

    requires = {"PP301"}
    url = mk_url("pytest")

    @staticmethod
    def check(pytest: tuple[PytestFile, dict[str, Any]]) -> bool:
        """
        An explicit summary flag like `-ra` should be in `addopts = [...]`
        (print summary of all fails/errors).

        ```toml
        [tool.pytest.ini_options]
        addopts = ["-ra", "--strict-config", "--strict-markers"]
        ```
        """
        loc, options = pytest
        addopts = options.get("addopts", [])
        if loc is PytestFile.LEGACY_PYPROJECT and isinstance(addopts, str):
            addopts = addopts.split()
        return any(opt.startswith("-r") for opt in addopts)


class PP309(PyProject):
    "Filter warnings specified"

    requires = {"PP301"}
    url = mk_url("pytest")

    @staticmethod
    def check(pytest: tuple[PytestFile, dict[str, Any]]) -> bool:
        """
        `filterwarnings` must be set (probably to at least `["error"]`). Python
        will hide important warnings otherwise, like deprecations.

        ```toml
        [tool.pytest.ini_options]
        filterwarnings = ["error"]
        ```
        """
        _, options = pytest
        return "filterwarnings" in options


def repo_review_checks() -> dict[str, PyProject]:
    return {p.__name__: p() for p in PyProject.__subclasses__()}
