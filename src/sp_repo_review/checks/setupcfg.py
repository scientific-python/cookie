# SCFG: setup.cfg
## SCFG0xx: setup.cfg checks

from __future__ import annotations

import configparser
from typing import TYPE_CHECKING

from . import mk_url

if TYPE_CHECKING:
    from .._compat.importlib.resources.abc import Traversable


def setupcfg(root: Traversable) -> configparser.ConfigParser | None:
    setupcfg_path = root.joinpath("setup.cfg")
    if setupcfg_path.is_file():
        config = configparser.ConfigParser()
        with setupcfg_path.open("r") as f:
            config.read_file(f)
        return config
    return None


class SCFG:
    family = "setupcfg"


class SCFG001(SCFG):
    "Avoid deprecated setup.cfg names"

    url = mk_url("packaging-classic")

    @staticmethod
    def check(setupcfg: configparser.ConfigParser | None) -> str | None:
        if setupcfg is None:
            return None
        invalid = []
        if setupcfg.has_section("metadata"):
            invalid += [
                f"metadata.{x}" for x, _ in setupcfg.items("metadata") if "-" in x
            ]
        if setupcfg.has_section("options"):
            invalid += [
                f"options.{x}" for x, _ in setupcfg.items("options") if "-" in x
            ]
        if invalid:
            return (
                "Invalid setup.cfg options found, only underscores allowed: "
                + ", ".join(invalid)
            )
        return ""


def repo_review_checks(
    list_all: bool = True, setupcfg: configparser.ConfigParser | None = None
) -> dict[str, SCFG]:
    if not list_all and setupcfg is None:
        return {}
    return {p.__name__: p() for p in SCFG.__subclasses__()}
