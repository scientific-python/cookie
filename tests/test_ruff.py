from repo_review.testing import compute_check, toml_loads


def test_rf001_present():
    assert compute_check("RF001", ruff={"lint": {}}).result


def test_rf001_missing():
    assert not compute_check("RF001", ruff=None).result


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


def test_rf003_src_default_now_unneeded(tmp_path):
    package = tmp_path / "pkg"
    package.mkdir()
    package.joinpath("src").mkdir()
    assert not compute_check("RF003", ruff={"src": ["src"]}, package=package).result


def test_rf003_other_src_okay(tmp_path):
    package = tmp_path / "pkg"
    package.mkdir()
    package.joinpath("src").mkdir()
    assert compute_check("RF003", ruff={"src": ["lib"]}, package=package).result


def test_rf003_not_applicable_without_src(tmp_path):
    package = tmp_path / "pkg"
    package.mkdir()
    assert compute_check("RF003", ruff={"src": ["src"]}, package=package).result is None


def test_rf101_selected():
    assert compute_check("RF101", ruff={"lint": {"select": ["B"]}}).result


def test_rf101_missing():
    assert not compute_check("RF101", ruff={"lint": {"select": ["I"]}}).result


def test_rf102_selected():
    assert compute_check("RF102", ruff={"lint": {"select": ["I"]}}).result


def test_rf102_missing():
    assert not compute_check("RF102", ruff={"lint": {"select": ["UP"]}}).result


def test_rf103_selected():
    assert compute_check("RF103", ruff={"lint": {"select": ["UP"]}}).result


def test_rf103_selected_by_all():
    assert compute_check("RF103", ruff={"lint": {"select": ["ALL"]}}).result


def test_rf103_missing():
    assert not compute_check("RF103", ruff={"lint": {"select": ["B"]}}).result


def test_rf201_no_deprecated_keys():
    assert compute_check("RF201", ruff={"lint": {"ignore": ["E501"]}}).result


def test_rf201_deprecated_extend_ignore():
    res = compute_check("RF201", ruff={"extend-ignore": ["E501"]})
    assert not res.result
    assert "extend-ignore" in res.err_msg


def test_rf202_uses_lint_namespace():
    assert compute_check("RF202", ruff={"lint": {"ignore": ["E501"]}}).result


def test_rf202_top_level_lint_key_fails():
    res = compute_check("RF202", ruff={"ignore": ["E501"]})
    assert not res.result
    assert "lint.ignore" in res.err_msg
