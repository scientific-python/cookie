# SEC: Security
## SEC0xx: GitHub Actions security

from __future__ import annotations

from typing import Any

from . import mk_url


class Security:
    family = "security"


class SEC001(Security):
    "Use zizmor to check the GitHub Actions"

    requires = {"GH100"}
    url = mk_url("security")

    @staticmethod
    def check(precommit: dict[str, Any], workflows: dict[str, Any]) -> bool:
        """
        Projects with GitHub Actions should statically analyze their workflows
        with [zizmor](https://docs.zizmor.sh), which catches common security
        issues such as template injection, excessive permissions, and
        credential persistence. The simplest way is to add the pre-commit hook:

        ```yaml
        - repo: https://github.com/zizmorcore/zizmor-pre-commit
          rev: v1.26.1
          hooks:
            - id: zizmor
        ```

        You can also run it as the `zizmorcore/zizmor-action` GitHub Action.
        """
        for repo_item in precommit.get("repos", []):
            if (
                repo_item.get("repo", "").lower()
                == "https://github.com/zizmorcore/zizmor-pre-commit"
            ):
                return True
        for workflow in workflows.values():
            for job in workflow.get("jobs", {}).values():
                if not isinstance(job, dict):
                    continue
                for step in job.get("steps", []):
                    if step.get("uses", "").startswith("zizmorcore/zizmor-action"):
                        return True
        return False


def repo_review_checks() -> dict[str, Security]:
    return {p.__name__: p() for p in Security.__subclasses__()}
