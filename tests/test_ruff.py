from sp_repo_review._compat import tomllib
from sp_repo_review.checks import ruff


def test_rf003_with_rp():
    toml = tomllib.loads("""
        project.requires-python = ">=3.12"
        tool.ruff.anything = "1"
        """)
    assert ruff.RF002.check(toml, toml["tool"]["ruff"])


def test_rf003_no_rp():
    toml = tomllib.loads("""
        project.name = "hi"
        tool.ruff.target-version = "3.12"
        """)
    assert ruff.RF002.check(toml, toml["tool"]["ruff"])


def test_rf003_both():
    toml = tomllib.loads("""
        project.requires-python = ">=3.12"
        tool.ruff.target-version = "3.12"
        """)
    assert isinstance(ruff.RF002.check(toml, toml["tool"]["ruff"]), str)


def test_rf003_split_ok():
    toml = tomllib.loads("""
        project.requires-python = ">=3.12"
        """)
    assert ruff.RF002.check(toml, {"target-version": "3.12"})
