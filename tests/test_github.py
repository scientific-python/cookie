import yaml
from repo_review.testing import compute_check


def test_gh105_trusted_publishing() -> None:
    workflows = yaml.safe_load(
        """
        cd:
          jobs:
            publish:
              steps:
                - uses: pypa/gh-action-pypi-publish@release/v1
        """
    )
    assert compute_check("GH105", workflows=workflows).result


def test_gh105_token_based_upload() -> None:
    workflows = yaml.safe_load(
        """
        cd:
          jobs:
            publish:
              steps:
                - uses: pypa/gh-action-pypi-publish@release/v1
                  with:
                    password: ${{ secrets.pypi_password }}
        """
    )
    res = compute_check("GH105", workflows=workflows)
    assert not res.result
    assert "Token-based publishing" in res.err_msg
