# GH: GitHub Actions
## GH1xx: Normal actions

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .._compat.importlib.resources.abc import Traversable
from . import mk_url


def workflows(root: Traversable) -> dict[str, Any]:
    workflows_base_path = root.joinpath(".github/workflows")
    workflows_dict: dict[str, Any] = {}
    if workflows_base_path.is_dir():
        for workflow_path in workflows_base_path.iterdir():
            if workflow_path.name.endswith(".yml"):
                with workflow_path.open("rb") as f:
                    workflows_dict[Path(workflow_path.name).stem] = yaml.safe_load(f)

    return workflows_dict


def dependabot(root: Traversable) -> dict[str, Any]:
    dependabot_path = root.joinpath(".github/dependabot.yml")
    if dependabot_path.is_file():
        with dependabot_path.open("rb") as f:
            result: dict[str, Any] = yaml.safe_load(f)
            return result

    return {}


class GitHub:
    family = "github"


class GH100(GitHub):
    "Has GitHub Actions config"
    url = mk_url("gha-basic")

    @staticmethod
    def check(workflows: dict[str, Any]) -> bool:
        """
        All projects should have GitHub Actions config for this series of
        checks.  If there are no `.yml` files in `.github/workflows`, the
        remaining checks will be skipped.
        """
        return bool(workflows)


class GH101(GitHub):
    "Has nice names"
    requires = {"GH100"}
    url = mk_url("gha-basic")

    @staticmethod
    def check(workflows: dict[str, Any]) -> bool:
        """
        All workflows should have a nice readable `name:` field to pass this
        check. Feel free to ignore if you are happy with the filenames as names.
        """
        return all("name" in w for w in workflows.values())


class GH102(GitHub):
    "Auto-cancel on repeated PRs"
    requires = {"GH100"}
    url = mk_url("gha-basic")

    @staticmethod
    def check(workflows: dict[str, Any]) -> bool:
        """
        At least one workflow should auto-cancel.

        ```yaml
        concurrency:
          group: ${{{{ github.workflow }}}}-${{{{ github.head_ref }}}}
          cancel-in-progress: true
        ```
        """
        return any("concurrency" in w for w in workflows.values())


class GH103(GitHub):
    "At least one workflow with manual dispatch trigger"
    requires = {"GH100"}
    url = mk_url("gha-basic")

    @staticmethod
    def check(workflows: dict[str, Any]) -> bool:
        """
        At least one workflow should have manual dispatch to allow easy triggering from the web.

        ```yaml
        on:
          workflow_dispatch:
        ```
        """
        return any("workflow_dispatch" in w.get(True, {}) for w in workflows.values())


class GH200(GitHub):
    "Maintained by Dependabot"
    url = mk_url("gha-basic")

    @staticmethod
    def check(dependabot: dict[str, Any]) -> bool:
        """
        All projects should have a `.github/dependabot.yml` file to support at least
        GitHub Actions regular updates. Something like this:

        ```yaml
        version: 2
        updates:
        # Maintain dependencies for GitHub Actions
          - package-ecosystem: "github-actions"
            directory: "/"
            schedule:
              interval: "weekly"
        ```
        """
        return bool(dependabot)


class GH210(GitHub):
    "Maintains the GitHub action versions with Dependabot"
    requires = {"GH200"}
    url = mk_url("gha-basic")

    @staticmethod
    def check(dependabot: dict[str, Any]) -> bool:
        """
        All projects should maintain the GH Actions with dependabot.

        ```yaml
        version: 2
        updates:
        # Maintain dependencies for GitHub Actions
          - package-ecosystem: "github-actions"
            directory: "/"
            schedule:
            interval: "weekly"
        ```
        """
        for ecosystem in dependabot.get("updates", []):
            if ecosystem.get("package-ecosystem", "") == "github-actions":
                return True
        return False


class GH211(GitHub):
    "Do not pin core actions as major versions"
    requires = {"GH200", "GH210"}  # Currently listing both helps - TODO: remove GH200
    url = mk_url("gha-basic")

    @staticmethod
    def check(dependabot: dict[str, Any]) -> bool:
        """
        Projects should not pin major versions for official actions. This is now
        supported by dependabot respecting the tag style you are already using
        since April 2022.
        """
        for ecosystem in dependabot.get("updates", []):
            if ecosystem.get("package-ecosystem", "") == "github-actions":
                for ignore in ecosystem.get("ignore", []):
                    if "actions/*" in ignore.get("dependency-name", ""):
                        return False
        return True


def repo_review_checks() -> dict[str, GitHub]:
    return {p.__name__: p() for p in GitHub.__subclasses__()}
