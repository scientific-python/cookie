import yaml
from repo_review.testing import compute_check


def test_sec001_precommit() -> None:
    precommit = yaml.safe_load(
        """
        repos:
          - repo: https://github.com/zizmorcore/zizmor-pre-commit
            rev: v1.22.0
            hooks:
              - id: zizmor
        """
    )
    assert compute_check("SEC001", precommit=precommit, workflows={"ci": {}}).result


def test_sec001_action() -> None:
    workflows = yaml.safe_load(
        """
        zizmor:
          jobs:
            zizmor:
              steps:
                - uses: zizmorcore/zizmor-action@v0.5.6
        """
    )
    assert compute_check("SEC001", precommit={}, workflows=workflows).result


def test_sec001_missing() -> None:
    precommit = yaml.safe_load(
        """
        repos:
          - repo: https://github.com/astral-sh/ruff-pre-commit
            rev: v0.15.16
            hooks:
              - id: ruff-check
        """
    )
    assert not compute_check(
        "SEC001", precommit=precommit, workflows={"ci": {}}
    ).result
