from __future__ import annotations

from .._compat.importlib.resources.abc import Traversable

# PY: Python Project
## 0xx: File existence


class General:
    family = "general"


class PY001(General):
    "Has a pyproject.toml"

    @staticmethod
    def check(package: Traversable) -> bool:
        """
        All projects should have a `pyproject.toml` file to support a modern
        build system and support wheel installs properly.
        """
        return package.joinpath("pyproject.toml").is_file()


class PY002(General):
    "Has a README.(md|rst) file"

    @staticmethod
    def check(package: Traversable) -> bool:
        "Projects must have a readme file"
        return (
            package.joinpath("README.md").is_file()
            or package.joinpath("README.rst").is_file()
        )


class PY003(General):
    "Has a LICENSE* file"

    @staticmethod
    def check(package: Traversable) -> bool:
        "Projects must have a license"
        return len([p for p in package.iterdir() if "LICENSE" in p.name]) > 0


class PY004(General):
    "Has docs folder"

    @staticmethod
    def check(package: Traversable) -> bool:
        "Projects must have documentation in a folder called docs (disable if not applicable)"
        return len([p for p in package.iterdir() if "doc" in p.name]) > 0


class PY005(General):
    "Has tests folder"

    @staticmethod
    def check(package: Traversable) -> bool:
        "Projects must have a folder called tests"
        return len([p for p in package.iterdir() if "test" in p.name]) > 0


class PY006(General):
    "Has pre-commit config"

    @staticmethod
    def check(package: Traversable) -> bool:
        "Projects must have a `.pre-commit-config.yaml` file"
        return package.joinpath(".pre-commit-config.yaml").is_file()


class PY007(General):
    "Supports an easy task runner (nox or tox)"

    @staticmethod
    def check(package: Traversable) -> bool:
        """
        Projects must have a `noxfile.py` or `tox.ini` to encourage new contributors.
        """
        return (
            package.joinpath("noxfile.py").is_file()
            or package.joinpath("tox.ini").is_file()
        )


def repo_review_checks() -> dict[str, General]:
    return {p.__name__: p() for p in General.__subclasses__()}
