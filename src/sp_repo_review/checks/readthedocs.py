from __future__ import annotations

from typing import Any

import yaml

from .._compat.importlib.resources.abc import Traversable
from . import mk_url


class ReadTheDocs:
    family = "docs"
    url = mk_url("docs")


class RTD100(ReadTheDocs):
    "Uses ReadTheDocs (pyproject config)"

    @staticmethod
    def check(root: Traversable) -> bool:
        """
        Should have a .readthedocs.yml file in the root of the repository.
        Modern ReadTheDocs requires (or will require soon) this file.
        """

        return root.joinpath(".readthedocs.yml").is_file()


class RTD101(ReadTheDocs):
    "You have to set the RTD version number to 2"

    requires = {"RTD100"}

    @staticmethod
    def check(readthedocs: dict[str, Any]) -> bool:
        """
        You must set `version: 2` in the `.readthedocs.yml` file.
        """

        match readthedocs:
            case {"version": int(x)} if x >= 2:
                return True
        return False


class RTD102(ReadTheDocs):
    "You have to set the RTD build image"

    requires = {"RTD100"}

    @staticmethod
    def check(readthedocs: dict[str, Any]) -> bool:
        """
        You must set `build: image: ubuntu-22.04` or similar in the
        `.readthedocs.yml` file.  Otherwise, you will get old, unsupported
        versions of software for backward compatibility.
        """

        match readthedocs:
            case {"build": {"os": object()}}:
                return True
            case _:
                return False


class RTD103(ReadTheDocs):
    "You have to set the RTD python version"

    requires = {"RTD100"}

    @staticmethod
    def check(readthedocs: dict[str, Any]) -> bool:
        """
        You must set `build: tools: python: "3.11"` or similar in the
        `.readthedocs.yml` file for a Python project.
        """

        match readthedocs:
            case {"build": {"tools": {"python": object()}}}:
                return True
            case _:
                return False


def readthedocs(root: Traversable) -> dict[str, Any]:
    readthedocs_path = root.joinpath(".readthedocs.yml")

    if not readthedocs_path.is_file():
        return {}

    with readthedocs_path.open("rb") as f:
        result: dict[str, Any] = yaml.safe_load(f)
        return result


def repo_review_checks() -> dict[str, ReadTheDocs]:
    return {p.__name__: p() for p in ReadTheDocs.__subclasses__()}
