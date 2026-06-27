import yaml
from repo_review.testing import compute_check

dependabot = yaml.safe_load(
    """
        version: 2
        updates:
          - package-ecosystem: github-actions
            directory: "/"
            schedule:
              interval: weekly
        """
)

renovate = {"extends": ["config:recommended"]}


def test_du100_both() -> None:
    assert compute_check("DEP200", dependabot=dependabot, renovate=renovate).result


def test_du100_missing_renovate() -> None:
    assert compute_check("GH200", dependabot=dependabot, renovate={}).result


def test_du100_missing_dependabot() -> None:
    assert compute_check("DEP200", dependabot={}, renovate=renovate).result


def test_du100_missing_both() -> None:
    assert not compute_check("DEP200", dependabot={}, renovate={}).result
