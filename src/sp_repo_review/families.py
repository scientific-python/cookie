from __future__ import annotations

import typing
from typing import Any

__all__ = ["Family", "get_families"]


def __dir__() -> list[str]:
    return __all__


class Family(typing.TypedDict, total=False):
    name: str  # defaults to key
    order: int  # defaults to 0
    description: str  # Defaults to empty


def get_families(pyproject: dict[str, Any]) -> dict[str, Family]:
    pyproject_description = f"- Detected build backend: `{pyproject.get('build-system', {}).get('build-backend', 'MISSING')}`"
    if isinstance(license := pyproject.get("project", {}).get("license", {}), str):
        pyproject_description += f"\n- SPDX license expression: `{license}`"
    elif classifiers := pyproject.get("project", {}).get("classifiers", []):
        licenses = [
            c.removeprefix("License :: ").removeprefix("OSI Approved :: ")
            for c in classifiers
            if c.startswith("License :: ")
        ]
        if licenses:
            pyproject_description += f"\n- Detected license(s): {', '.join(licenses)}"
    return {
        "general": Family(
            name="General",
            order=-3,
            description=pyproject_description,
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
        ),
        "docs": Family(
            name="Documentation",
        ),
        "setupcfg": Family(
            name="Setuptools Config",
        ),
    }
