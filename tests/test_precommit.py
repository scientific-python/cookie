from pathlib import Path

import pytest
import yaml
from repo_review.testing import compute_check

from sp_repo_review.checks.precommit import repo_review_checks


@pytest.fixture(params=["ruff", "ruff-check"])
def ruff_check(request: pytest.FixtureRequest) -> str:
    return request.param  # type: ignore[no-any-return]


def test_pc100():
    precommit = yaml.safe_load("""
        repos:
          - repo: https://github.com/pre-commit/pre-commit-hooks
    """)
    assert compute_check("PC100", precommit=precommit).result


def test_pc110_black():
    precommit = yaml.safe_load("""
        repos:
          - repo: https://github.com/psf/black-pre-commit-mirror
    """)
    assert compute_check("PC110", precommit=precommit).result


def test_pc110_ruff():
    precommit = yaml.safe_load("""
        repos:
          - repo: https://github.com/astral-sh/ruff-pre-commit
            hooks:
              - id: ruff-format
    """)
    assert compute_check("PC110", precommit=precommit).result


def test_pc110_ruff_no_hook():
    precommit = yaml.safe_load("""
        repos:
          - repo: https://github.com/astral-sh/ruff-pre-commit
    """)
    res = compute_check("PC110", precommit=precommit)
    assert not res.result
    assert "ruff-format" in res.err_msg


def test_pc110_rename():
    precommit = yaml.safe_load("""
        repos:
          - repo: https://github.com/psf/black
    """)
    res = compute_check("PC110", precommit=precommit)
    assert not res.result
    assert "black-pre-commit-mirror" in res.err_msg


def test_pc111():
    precommit = yaml.safe_load("""
        repos:
          - repo: https://github.com/adamchainz/blacken-docs
    """)
    assert compute_check("PC111", precommit=precommit).result


def test_pc111_rename():
    precommit = yaml.safe_load("""
        repos:
          - repo: https://github.com/asottile/blacken-docs
    """)
    res = compute_check("PC111", precommit=precommit)
    assert not res.result
    assert "adamchainz" in res.err_msg


def test_pc190():
    precommit = yaml.safe_load("""
        repos:
          - repo: https://github.com/astral-sh/ruff-pre-commit
    """)
    assert compute_check("PC190", precommit=precommit).result


def test_pc190_rename():
    precommit = yaml.safe_load("""
        repos:
          - repo: https://github.com/charliermarsh/ruff-pre-commit
    """)
    res = compute_check("PC190", precommit=precommit)
    assert not res.result
    assert "astral-sh" in res.err_msg


def test_pc140():
    precommit = yaml.safe_load("""
        repos:
          - repo: https://github.com/pre-commit/mirrors-mypy
    """)
    assert compute_check("PC140", precommit=precommit).result


def test_pc160_codespell():
    precommit = yaml.safe_load("""
        repos:
          - repo: https://github.com/codespell-project/codespell
    """)
    assert compute_check("PC160", precommit=precommit).result


def test_pc160_typos():
    precommit = yaml.safe_load("""
        repos:
          - repo: https://github.com/crate-ci/typos
    """)
    assert compute_check("PC160", precommit=precommit).result


def test_pc170():
    precommit = yaml.safe_load("""
        repos:
          - repo: https://github.com/pre-commit/pygrep-hooks
    """)
    assert compute_check("PC170", precommit=precommit).result


def test_pc180():
    precommit = yaml.safe_load("""
        repos:
          - repo: https://github.com/rbubley/mirrors-prettier
    """)
    assert compute_check("PC180", precommit=precommit).result


def test_pc180_rename():
    precommit = yaml.safe_load("""
        repos:
          - repo: https://github.com/pre-commit/mirrors-prettier
    """)
    res = compute_check("PC180", precommit=precommit)
    assert not res.result
    assert "https://github.com/rbubley/mirrors-prettier" in res.err_msg


def test_pc180_alt_2():
    precommit = yaml.safe_load("""
        repos:
          - repo: https://github.com/hukkin/mdformat
    """)
    assert compute_check("PC180", precommit=precommit).result


def test_pc180_rename_1():
    precommit = yaml.safe_load("""
        repos:
          - repo: https://github.com/executablebooks/mdformat
    """)
    res = compute_check("PC180", precommit=precommit)
    assert not res.result
    assert "https://github.com/hukkin/mdformat" in res.err_msg


def test_pc180_alt_3():
    precommit = yaml.safe_load("""
        repos:
          - repo: https://github.com/rvben/rumdl-pre-commit
    """)
    assert compute_check("PC180", precommit=precommit).result


def test_pc180_alt_4():
    precommit = yaml.safe_load("""
        repos:
          - repo: https://github.com/DavidAnson/markdownlint-cli2
    """)
    assert compute_check("PC180", precommit=precommit).result


def test_pc191(ruff_check: str):
    precommit = yaml.safe_load(f"""
        repos:
          - repo: https://github.com/astral-sh/ruff-pre-commit
            hooks:
              - id: {ruff_check}
                args: ["--fix", "--show-fixes"]
    """)
    assert compute_check("PC191", precommit=precommit, ruff={}).result


def test_pc191_ruffconfig(ruff_check: str):
    precommit = yaml.safe_load(f"""
        repos:
          - repo: https://github.com/astral-sh/ruff-pre-commit
            hooks:
              - id: {ruff_check}
                args: ["--fix"]
    """)
    assert compute_check("PC191", precommit=precommit, ruff={"show-fixes": True}).result


def test_pc191_no_show_fixes(ruff_check: str):
    precommit = yaml.safe_load(f"""
        repos:
          - repo: https://github.com/astral-sh/ruff-pre-commit
            hooks:
              - id: {ruff_check}
                args: ["--fix"]
    """)
    res = compute_check("PC191", precommit=precommit, ruff={})
    assert not res.result
    assert "--show-fixes" in res.err_msg


def test_pc192():
    precommit = yaml.safe_load("""
        repos:
          - repo: https://github.com/astral-sh/ruff-pre-commit
            hooks:
              - id: ruff
                args: ["--fix"]
    """)
    res = compute_check("PC192", precommit=precommit)
    assert not res.result
    assert "ruff-check" in res.err_msg


def test_pc192_not_needed():
    precommit = yaml.safe_load("""
        repos:
          - repo: https://github.com/astral-sh/ruff-pre-commit
            hooks:
              - id: ruff-format
    """)
    res = compute_check("PC192", precommit=precommit)
    assert res.result is None


def test_pc901():
    precommit = yaml.safe_load("""
        ci:
          autoupdate_commit_msg: 'chore: update pre-commit hooks'
    """)
    assert compute_check("PC901", precommit=precommit).result


def test_pc901_no_msg():
    precommit = yaml.safe_load("""
    repos:
    """)
    res = compute_check("PC901", precommit=precommit)
    assert not res.result
    assert "autoupdate_commit_msg" in res.err_msg


def test_pc902():
    precommit = yaml.safe_load("""
        ci:
          autofix_commit_msg: 'style: pre-commit fixes'
    """)
    assert compute_check("PC902", precommit=precommit).result


def test_pc902_no_msg():
    precommit = yaml.safe_load("""
    repos:
    """)
    res = compute_check("PC902", precommit=precommit)
    assert not res.result
    assert "autofix_commit_msg" in res.err_msg


def test_pc903():
    precommit = yaml.safe_load("""
        ci:
          autoupdate_schedule: "monthly"

    """)
    assert compute_check("PC903", precommit=precommit).result


def test_pc903_no_msg():
    precommit = yaml.safe_load("""
    repos:
    """)
    res = compute_check("PC903", precommit=precommit)
    assert not res.result
    assert "autoupdate_schedule" in res.err_msg


def test_repo_review_checks_skips_with_lefthook_only(tmp_path: Path) -> None:
    """PreCommit checks should be omitted if only lefthook.yml is present.

    When a repository uses `lefthook.yml` and does not have a
    `.pre-commit-config.yaml`, `repo_review_checks` should return an empty
    mapping when `list_all=False` indicating the pre-commit family is skipped.
    """
    # Create only a lefthook configuration
    (tmp_path / "lefthook.yml").write_text("hooks:\n", encoding="utf-8")

    checks = repo_review_checks(list_all=False, root=tmp_path)
    assert checks == {}
