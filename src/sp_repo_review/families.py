from __future__ import annotations

import typing
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Generator


__all__ = ["Family", "get_families"]


def __dir__() -> list[str]:
    return __all__


class Family(typing.TypedDict, total=False):
    name: str  # defaults to key
    order: int  # defaults to 0
    description: str  # Defaults to empty


def general_description(pyproject: dict[str, Any]) -> Generator[str, None, None]:
    yield f"- Detected build backend: `{pyproject.get('build-system', {}).get('build-backend', 'MISSING')}`"
    match pyproject:
        case {"project": {"license": str() as license}}:
            yield f"- SPDX license expression: `{license}`"
        case {"project": {"classifiers": classifiers}}:
            licenses = [
                c.removeprefix("License :: ").removeprefix("OSI Approved :: ")
                for c in classifiers
                if c.startswith("License :: ")
            ]
            if licenses:
                yield f"- Detected license(s): {', '.join(licenses)}"


def ruff_description(ruff: dict[str, Any]) -> str:
    common = {
        "ARG",
        "B",
        "C4",
        "DTZ",
        "EM",
        "EXE",
        "FA",
        "FURB",
        "G",
        "I",
        "ICN",
        "NPY",
        "PD",
        "PERF",
        "PGH",
        "PIE",
        "PL",
        "PT",
        "PTH",
        "PYI",
        "RET",
        "RUF",
        "SIM",
        "SLOT",
        "T20",
        "TC",
        "UP",
        "YTT",
    }

    match ruff:
        case (
            {"lint": {"select": x} | {"extend-select": x}}
            | {"select": x}
            | {"extend-select": x}
        ):
            selected = set(x)
            known = common - selected
            if not known or "ALL" in selected:
                return "All mentioned rules selected"
            rulelist = ", ".join(f'"{r}"' for r in known)
            return f"Rules mentioned in guide but not here: `{rulelist}`"
    return ""


def get_families(pyproject: dict[str, Any], ruff: dict[str, Any]) -> dict[str, Family]:
    return {
        "general": Family(
            name="General",
            order=-3,
            description="\n".join(general_description(pyproject)),
        ),
        "pyproject": Family(
            name="PyProject",
            order=-2,
        ),
        "github": Family(
            name="GitHub Actions",
        ),
        "pre-commit": Family(
            name="Pre-commit",
        ),
        "mypy": Family(
            name="MyPy",
        ),
        "ruff": Family(
            name="Ruff",
            description=ruff_description(ruff),
        ),
        "docs": Family(
            name="Documentation",
        ),
        "setupcfg": Family(
            name="Setuptools Config",
        ),
        "noxfile": Family(
            name="Nox",
        ),
    }
