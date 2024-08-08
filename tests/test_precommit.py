import yaml
from repo_review.testing import compute_check


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


def test_pc180_alt_1():
    precommit = yaml.safe_load("""
        repos:
          - repo: https://github.com/rbubley/mirrors-prettier
    """)
    assert compute_check("PC180", precommit=precommit).result


def test_pc191():
    precommit = yaml.safe_load("""
        repos:
          - repo: https://github.com/astral-sh/ruff-pre-commit
            hooks:
              - id: ruff
                args: ["--fix", "--show-fixes"]
    """)
    assert compute_check("PC191", precommit=precommit).result


def test_pc191_no_show_fixes():
    precommit = yaml.safe_load("""
        repos:
          - repo: https://github.com/astral-sh/ruff-pre-commit
            hooks:
              - id: ruff
                args: ["--fix"]
    """)
    res = compute_check("PC191", precommit=precommit)
    assert not res.result
    assert "--show-fixes" in res.err_msg


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
