from repo_review.testing import compute_check, toml_loads


def test_rf003_with_rp():
    toml = toml_loads("""
        project.requires-python = ">=3.12"
        tool.ruff.anything = "1"
        """)
    assert compute_check("RF002", pyproject=toml, ruff=toml["tool"]["ruff"]).result


def test_rf003_no_rp():
    toml = toml_loads("""
        project.name = "hi"
        tool.ruff.target-version = "3.12"
        """)
    assert compute_check("RF002", pyproject=toml, ruff=toml["tool"]["ruff"]).result


def test_rf003_both():
    toml = toml_loads("""
        project.requires-python = ">=3.12"
        tool.ruff.target-version = "3.12"
        """)
    check_result = compute_check("RF002", pyproject=toml, ruff=toml["tool"]["ruff"])
    assert check_result.result is False


def test_rf003_split_ok():
    toml = toml_loads("""
        project.requires-python = ">=3.12"
        """)
    assert compute_check(
        "RF002", pyproject=toml, ruff={"target-version": "3.12"}
    ).result
