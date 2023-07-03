# PC: Pre-commit
## PC0xx: pre-commit-hooks

from __future__ import annotations

from typing import Any, ClassVar, Protocol

import yaml

from .._compat.importlib.resources.abc import Traversable
from . import mk_url


def precommit(root: Traversable) -> dict[str, Any]:
    precommit_path = root.joinpath(".pre-commit-config.yaml")
    if precommit_path.is_file():
        with precommit_path.open("rb") as f:
            return yaml.safe_load(f)  # type: ignore[no-any-return]

    return {}


class PreCommitMixin(Protocol):
    repo: ClassVar[str]


class PreCommit:
    family = "pre-commit"
    requires = {"PY006"}
    url = mk_url("style")

    @classmethod
    def check(cls: type[PreCommitMixin], precommit: dict[str, Any]) -> bool | None:
        "Must have `{self.repo}` repo in `.pre-commit-config.yaml`"
        for repo in precommit.get("repos", {}):
            if "repo" in repo and repo["repo"].lower() == cls.repo:
                return True
        return False


class PC100(PreCommit):
    "Has pre-commit-hooks"
    repo = "https://github.com/pre-commit/pre-commit-hooks"


class PC110(PreCommit):
    "Uses black"
    repo = "https://github.com/psf/black"


class PC111(PreCommit):
    "Uses blacken-docs"
    requires = {"PY006", "PC110"}
    repo = "https://github.com/asottile/blacken-docs"


class PC190(PreCommit):
    "Uses Ruff"
    repo = "https://github.com/astral-sh/ruff-pre-commit"


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
