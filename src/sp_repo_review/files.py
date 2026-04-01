from __future__ import annotations


def prefetch_root() -> set[str]:
    """
    This entry-point lists files that should be prefetched. This is a suggestion
    for async loading.
    """

    return {
        "setup.cfg",
    }


def prefetch_package() -> set[str]:
    """
    This entry-point lists files that should be prefetched. This is a suggestion
    for async loading.
    """

    return {
        ".github/dependabot.yml",
        ".github/dependabot.yaml",
        ".github/workflows/*.yml",
        ".github/workflows/*.yaml",
        ".pre-commit-config.yaml",
        ".readthedocs.yml",
        "noxfile.py",
        "ruff.toml",
        ".ruff.toml",
    }
