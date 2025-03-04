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
    renamed: ClassVar[dict[str, str]] = {}
    repos: ClassVar[set[str]] = set()
    ids: ClassVar[dict[str, str]] = {}

    @property
    def describe(self) -> str:
        msgs = sorted(
            f"`{r}` (with `{self.ids[r]}` hook)" if r in self.ids else f"`{r}`"
            for r in self.repos
        )
        if not msgs:
            return "..."
        if len(msgs) == 1:
            return msgs[0]
        return "one of " + ", ".join(msgs)

    @classmethod
    def check(cls, precommit: dict[str, Any]) -> bool | None | str:
        "Must have {self.describe} in `.pre-commit-config.yaml`"
        assert cls.repos, f"{cls.__name__} must have a repo, invalid class definition"
        for repo_item in precommit.get("repos", {}):
            repo = repo_item.get("repo", "").lower()
            if not repo:
                continue
            if repo in cls.repos:
                if cls.ids and repo in cls.ids:
                    if any(
                        hook.get("id", "") == cls.ids[repo]
                        for hook in repo_item.get("hooks", {})
                    ):
                        return True
                else:
                    return True
            if cls.renamed and repo in cls.renamed:
                rename = cls.renamed[repo]
                return (
                    f"Use `{rename}` instead of `{repo}` in `.pre-commit-config.yaml`"
                )
        return False


class PC100(PreCommit):
    "Has pre-commit-hooks"

    repos = {"https://github.com/pre-commit/pre-commit-hooks"}


class PC110(PreCommit):
    "Uses black or ruff-format"

    repos = {
        "https://github.com/psf/black-pre-commit-mirror",
        "https://github.com/astral-sh/ruff-pre-commit",
    }
    renamed = {
        "https://github.com/psf/black": "https://github.com/psf/black-pre-commit-mirror"
    }
    ids = {"https://github.com/astral-sh/ruff-pre-commit": "ruff-format"}


class PC111(PreCommit):
    "Uses blacken-docs"

    requires = {"PY006", "PC110"}
    repos = {"https://github.com/adamchainz/blacken-docs"}
    renamed = {
        "https://github.com/asottile/blacken-docs": "https://github.com/adamchainz/blacken-docs"
    }


class PC190(PreCommit):
    "Uses Ruff"

    repos = {"https://github.com/astral-sh/ruff-pre-commit"}
    renamed = {
        "https://github.com/charliermarsh/ruff-pre-commit": "https://github.com/astral-sh/ruff-pre-commit"
    }


class PC140(PreCommit):
    "Uses a type checker"

    repos = {"https://github.com/pre-commit/mirrors-mypy"}


class PC160(PreCommit):
    "Uses a spell checker"

    repos = {
        "https://github.com/codespell-project/codespell",
        "https://github.com/crate-ci/typos",
    }


class PC170(PreCommit):
    "Uses PyGrep hooks (only needed if rST present)"

    repos = {"https://github.com/pre-commit/pygrep-hooks"}


class PC180(PreCommit):
    "Uses a markdown formatter"

    renamed = {
        "https://github.com/pre-commit/mirrors-prettier": "https://github.com/rbubley/mirrors-prettier"
    }

    repos = {
        "https://github.com/rbubley/mirrors-prettier",
        "https://github.com/executablebooks/mdformat",
        "https://github.com/hukkin/mdformat",
    }


class PC191(PreCommit):
    "Ruff show fixes if fixes enabled"

    requires = {"PC190"}
    repos = {"https://github.com/astral-sh/ruff-pre-commit"}

    @classmethod
    def check(cls, precommit: dict[str, Any]) -> bool | None:
        """
        If `--fix` is present, `--show-fixes` must be too.
        """
        for repo in precommit.get("repos", {}):
            if "repo" in repo and repo["repo"].lower() in cls.repos:
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
