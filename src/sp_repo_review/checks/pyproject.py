from __future__ import annotations

from typing import TYPE_CHECKING, Any

from . import mk_url

if TYPE_CHECKING:
    from configparser import ConfigParser


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
            case {"build-system": {"requires": list(req)}}:
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

        match pyproject:
            case {"project": {"requires-python": requires}}:
                return "~=" not in requires and "<" not in requires
            case {
                "tool": {
                    "poetry": {
                        "dependencies": {
                            "python": str(requires) | {"version": str(requires)}
                        }
                    }
                }
            }:
                return (
                    "^" not in requires and "~=" not in requires and "<" not in requires
                )

        if setupcfg and (
            requires := setupcfg.get("options", "python_requires", fallback=None)
        ):
            return "~=" not in requires and "<" not in requires

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


class PP301(PyProject):
    "Has pytest in pyproject"

    requires = {"PY001"}
    url = mk_url("pytest")

    @staticmethod
    def check(pyproject: dict[str, Any]) -> bool:
        """
        Must have a `[tool.pytest.ini_options]` configuration section in
        pyproject.toml. If you must have it somewhere else (such as to support
        `pytest<6`), ignore this check.
        """

        match pyproject:
            case {"tool": {"pytest": {"ini_options": {}}}}:
                return True
            case _:
                return False


class PP302(PyProject):
    "Sets a minimum pytest to at least 6"

    requires = {"PP301"}
    url = mk_url("pytest")

    @staticmethod
    def check(pyproject: dict[str, Any]) -> bool:
        """
        Must have a `minversion=`, and must be at least 6 (first version to
        support `pyproject.toml` configuration).

        ```toml
        [tool.pytest.ini_options]
        minversion = "7"
        ```
        """
        options = pyproject["tool"]["pytest"]["ini_options"]
        return (
            "minversion" in options
            and int(str(options["minversion"]).split(".", maxsplit=1)[0]) >= 6
        )


class PP303(PyProject):
    "Sets the test paths"

    requires = {"PP301"}
    url = mk_url("pytest")

    @staticmethod
    def check(pyproject: dict[str, Any]) -> bool:
        """
        The `testpaths` setting should be set to a reasonable default.

        ```toml
        [tool.pytest.ini_options]
        testpaths = ["tests"]
        ```
        """
        options = pyproject["tool"]["pytest"]["ini_options"]
        return "testpaths" in options


class PP304(PyProject):
    "Sets the log level in pytest"

    requires = {"PP301"}
    url = mk_url("pytest")

    @staticmethod
    def check(pyproject: dict[str, Any]) -> bool:
        """
        `log_cli_level` should be set. This will allow logs to be displayed on
        failures.

        ```toml
        [tool.pytest.ini_options]
        log_cli_level = "INFO"
        ```
        """
        options = pyproject["tool"]["pytest"]["ini_options"]
        return "log_cli_level" in options


class PP305(PyProject):
    "Specifies xfail_strict"

    requires = {"PP301"}
    url = mk_url("pytest")

    @staticmethod
    def check(pyproject: dict[str, Any]) -> bool:
        """
        `xfail_strict` should be set. You can manually specify if a check
        should be strict when setting each xfail.

        ```toml
        [tool.pytest.ini_options]
        xfail_strict = true
        ```
        """
        options = pyproject["tool"]["pytest"]["ini_options"]
        return "xfail_strict" in options


class PP306(PyProject):
    "Specifies strict config"

    requires = {"PP301"}
    url = mk_url("pytest")

    @staticmethod
    def check(pyproject: dict[str, Any]) -> bool:
        """
        `--strict-config` should be in `addopts = [...]`. This forces an error
        if a config setting is misspelled.

        ```toml
        [tool.pytest.ini_options]
        addopts = ["-ra", "--strict-config", "--strict-markers"]
        ```
        """
        options = pyproject["tool"]["pytest"]["ini_options"]
        return "--strict-config" in options.get("addopts", [])


class PP307(PyProject):
    "Specifies strict markers"

    requires = {"PP301"}
    url = mk_url("pytest")

    @staticmethod
    def check(pyproject: dict[str, Any]) -> bool:
        """
        `--strict-markers` should be in `addopts = [...]`. This forces all
        markers to be specified in config, avoiding misspellings.

        ```toml
        [tool.pytest.ini_options]
        addopts = ["-ra", "--strict-config", "--strict-markers"]
        ```
        """
        options = pyproject["tool"]["pytest"]["ini_options"]
        return "--strict-markers" in options.get("addopts", [])


class PP308(PyProject):
    "Specifies useful pytest summary"

    requires = {"PP301"}
    url = mk_url("pytest")

    @staticmethod
    def check(pyproject: dict[str, Any]) -> bool:
        """
        An explicit summary flag like `-ra` should be in `addopts = [...]`
        (print summary of all fails/errors).

        ```toml
        [tool.pytest.ini_options]
        addopts = ["-ra", "--strict-config", "--strict-markers"]
        ```
        """
        options = pyproject["tool"]["pytest"]["ini_options"]
        addopts = options.get("addopts", [])
        if isinstance(addopts, str):
            addopts = addopts.split()
        return any(opt.startswith("-r") for opt in addopts)


class PP309(PyProject):
    "Filter warnings specified"

    requires = {"PP301"}
    url = mk_url("pytest")

    @staticmethod
    def check(pyproject: dict[str, Any]) -> bool:
        """
        `filterwarnings` must be set (probably to at least `["error"]`). Python
        will hide important warnings otherwise, like deprecations.

        ```toml
        [tool.pytest.ini_options]
        filterwarnings = ["error"]
        ```
        """
        options = pyproject["tool"]["pytest"]["ini_options"]
        return "filterwarnings" in options


def repo_review_checks() -> dict[str, PyProject]:
    return {p.__name__: p() for p in PyProject.__subclasses__()}
