from __future__ import annotations

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
        return len([p for p in package.iterdir() if "LICENSE" in p.name]) > 0


class PY004(General):
    "Has docs folder"
    url = mk_url("packaging-simple")

    @staticmethod
    def check(package: Traversable) -> bool:
        "Projects must have documentation in a folder called docs (disable if not applicable)"
        return len([p for p in package.iterdir() if "doc" in p.name]) > 0


class PY005(General):
    "Has tests folder"
    url = mk_url("packaging-simple")

    @staticmethod
    def check(package: Traversable) -> bool:
        "Projects must have a folder called `*test*` or `src/*/*test*`"
        # Out-of-source tests
        if len([p for p in package.iterdir() if "test" in p.name]) > 0:
            return True

        # In-source tests
        src = package.joinpath("src")
        if src.is_dir():
            for pkg in src.iterdir():
                if len([p for p in pkg.iterdir() if "test" in p.name]) > 0:
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
    "Supports an easy task runner (nox or tox)"
    url = mk_url("tasks")

    @staticmethod
    def check(root: Traversable) -> bool:
        """
        Projects must have a `noxfile.py` or `tox.ini` to encourage new contributors.
        """
        return (
            root.joinpath("noxfile.py").is_file() or root.joinpath("tox.ini").is_file()
        )


def repo_review_checks() -> dict[str, General]:
    return {p.__name__: p() for p in General.__subclasses__()}
