# PC: Pre-commit
## PC0xx: pre-commit-hooks

from __future__ import annotations

from typing import Any, ClassVar

import yaml

from .._compat.importlib.resources.abc import Traversable
from . import mk_url


def precommit(root: Traversable) -> dict[str, Any]:
    precommit_path = root.joinpath(".pre-commit-config.yaml")
    if precommit_path.is_file():
        with precommit_path.open("rb") as f:
            return yaml.safe_load(f)  # type: ignore[no-any-return]

    return {}


class PreCommit:
    family = "pre-commit"
    requires = {"PY006"}
    url = mk_url("style")
    renamed: ClassVar[str | None] = None
    repo: ClassVar[str | None] = None

    @classmethod
    def check(cls, precommit: dict[str, Any]) -> bool | None | str:
        "Must have `{self.repo}` repo in `.pre-commit-config.yaml`"
        assert cls.repo is not None
        for repo in precommit.get("repos", {}):
            if repo.get("repo", "").lower() == cls.repo:
                return True
            if cls.renamed is not None and repo.get("repo", "").lower() == cls.renamed:
                return f"Use `{cls.repo}` instead of `{cls.renamed}` in `.pre-commit-config.yaml`"
        return False


class PC100(PreCommit):
    "Has pre-commit-hooks"

    repo = "https://github.com/pre-commit/pre-commit-hooks"


class PC110(PreCommit):
    "Uses black or ruff-format"

    repo = "https://github.com/psf/black-pre-commit-mirror"
    renamed = "https://github.com/psf/black"
    alternate = "https://github.com/astral-sh/ruff-pre-commit"

    @classmethod
    def check(cls, precommit: dict[str, Any]) -> bool | None | str:
        "Must have `{self.repo}` or `{self.alternate}` + `id: ruff-format` in `.pre-commit-config.yaml`"
        for repo in precommit.get("repos", {}):
            if repo.get("repo", "").lower() == cls.alternate and any(
                hook.get("id", "") == "ruff-format" for hook in repo.get("hooks", {})
            ):
                return True

        return super().check(precommit)


class PC111(PreCommit):
    "Uses blacken-docs"

    requires = {"PY006", "PC110"}
    repo = "https://github.com/adamchainz/blacken-docs"
    renamed = "https://github.com/asottile/blacken-docs"


class PC190(PreCommit):
    "Uses Ruff"

    repo = "https://github.com/astral-sh/ruff-pre-commit"
    renamed = "https://github.com/charliermarsh/ruff-pre-commit"


class PC140(PreCommit):
    "Uses mypy"

    repo = "https://github.com/pre-commit/mirrors-mypy"


class PC160(PreCommit):
    "Uses codespell"

    repo = "https://github.com/codespell-project/codespell"


class PC170(PreCommit):
    "Uses PyGrep hooks (only needed if RST present)"

    repo = "https://github.com/pre-commit/pygrep-hooks"


class PC180(PreCommit):
    "Uses prettier"

    repo = "https://github.com/pre-commit/mirrors-prettier"


class PC191(PreCommit):
    "Ruff show fixes if fixes enabled"

    requires = {"PC190"}
    repo = "https://github.com/astral-sh/ruff-pre-commit"

    @classmethod
    def check(cls, precommit: dict[str, Any]) -> bool | None:
        """
        If `--fix` is present, `--show-fixes` must be too.
        """
        for repo in precommit.get("repos", {}):
            if "repo" in repo and repo["repo"].lower() == cls.repo:
                for hook in repo["hooks"]:
                    if (
                        hook["id"] == "ruff"
                        and "args" in hook
                        and "--fix" in hook["args"]
                    ):
                        return "--show-fixes" in hook["args"]
                return None
        return False


class PC901(PreCommit):
    "Custom pre-commit CI message"

    @staticmethod
    def check(precommit: dict[str, Any]) -> bool:
        """
        Should have something like this in `.pre-commit-config.yaml`:

        ```yaml
        ci:
          autoupdate_commit_msg: 'chore: update pre-commit hooks'
        ```
        """

        return "autoupdate_commit_msg" in precommit.get("ci", {})


def repo_review_checks() -> dict[str, PreCommit]:
    return {p.__name__: p() for p in PreCommit.__subclasses__()}
