from pathlib import Path

import pytest
from repo_review.testing import compute_check, toml_loads

from sp_repo_review.checks.mypy import pyrefly, ty


def test_my100_present():
    toml = toml_loads("""
        [tool.mypy]
        strict = true
        """)
    assert compute_check("MY100", pyproject=toml, ty=None, pyrefly=None).result


def test_my100_pyrefly():
    assert compute_check(
        "MY100", pyproject={}, ty=None, pyrefly={"project-includes": ["src"]}
    ).result


def test_my100_ty():
    assert compute_check(
        "MY100", pyproject={}, ty={"src": {"include": ["src"]}}, pyrefly=None
    ).result


def test_my100_missing():
    assert not compute_check("MY100", pyproject={}, ty=None, pyrefly=None).result


def test_ty_fixture_pyproject(tmp_path: Path):
    toml = toml_loads("""
        [tool.ty.rules]
        all = "error"
        """)
    assert ty(toml, tmp_path) == {"rules": {"all": "error"}}


def test_ty_fixture_file(tmp_path: Path):
    tmp_path.joinpath("ty.toml").write_text('[rules]\nall = "warn"\n')
    toml = toml_loads("""
        [tool.ty.rules]
        all = "error"
        """)
    assert ty(toml, tmp_path) == {"rules": {"all": "warn"}}


def test_ty_fixture_missing(tmp_path: Path):
    assert ty({}, tmp_path) is None


def test_pyrefly_fixture_pyproject(tmp_path: Path):
    toml = toml_loads("""
        [tool.pyrefly]
        preset = "strict"
        """)
    assert pyrefly(toml, tmp_path) == {"preset": "strict"}


def test_pyrefly_fixture_file(tmp_path: Path):
    tmp_path.joinpath("pyrefly.toml").write_text('preset = "all"\n')
    toml = toml_loads("""
        [tool.pyrefly]
        preset = "strict"
        """)
    assert pyrefly(toml, tmp_path) == {"preset": "all"}


def test_pyrefly_fixture_missing(tmp_path: Path):
    assert pyrefly({}, tmp_path) is None


def test_my101_present_bool():
    toml = toml_loads("""
        [tool.mypy]
        strict = false
        """)
    assert compute_check("MY101", pyproject=toml, ty=None, pyrefly=None).result


def test_my101_missing():
    toml = toml_loads("""
        [tool.mypy]
        warn_unreachable = true
        """)
    assert not compute_check("MY101", pyproject=toml, ty=None, pyrefly=None).result


@pytest.mark.parametrize("preset", ["strict", "all"])
def test_my101_pyrefly_preset(preset: str):
    assert compute_check(
        "MY101", pyproject={}, ty=None, pyrefly={"preset": preset}
    ).result


@pytest.mark.parametrize("preset", ["basic", "legacy", "default"])
def test_my101_pyrefly_loose_preset(preset: str):
    result = compute_check("MY101", pyproject={}, ty=None, pyrefly={"preset": preset})
    assert result.result is False


def test_my101_pyrefly_no_preset():
    result = compute_check(
        "MY101", pyproject={}, ty=None, pyrefly={"project-includes": ["src"]}
    )
    assert result.result is False


def test_my101_ty_rules():
    result = compute_check(
        "MY101", pyproject={}, ty={"rules": {"all": "error"}}, pyrefly=None
    )
    assert result.result


def test_my101_ty_no_rules():
    result = compute_check(
        "MY101", pyproject={}, ty={"src": {"include": ["src"]}}, pyrefly=None
    )
    assert result.result is False


def test_my101_skipped():
    assert compute_check("MY101", pyproject={}, ty=None, pyrefly=None).result is None


def test_my10x_skipped_without_mypy():
    toml = toml_loads("""
        [tool.ty.src]
        include = ["src"]
        """)
    for name in ("MY102", "MY103", "MY104", "MY105", "MY106"):
        assert compute_check(name, pyproject=toml).result is None


def test_my107_error_on_warning():
    result = compute_check("MY107", ty={"terminal": {"error-on-warning": False}})
    assert result.result


def test_my107_missing():
    assert compute_check("MY107", ty={"rules": {}}).result is False


def test_my107_skipped():
    assert compute_check("MY107", ty=None).result is None


@pytest.mark.parametrize("level", ["warn", "error"])
def test_my108_blanket_ignore(level: str):
    result = compute_check("MY108", ty={"rules": {"blanket-ignore-comment": level}})
    assert result.result


def test_my108_all_error():
    assert compute_check("MY108", ty={"rules": {"all": "error"}}).result


def test_my108_ignored():
    result = compute_check(
        "MY108",
        ty={"rules": {"all": "error", "blanket-ignore-comment": "ignore"}},
    )
    assert result.result is False


def test_my108_missing():
    assert compute_check("MY108", ty={"rules": {}}).result is False


def test_my108_skipped():
    assert compute_check("MY108", ty=None).result is None


def test_my102_pass_without_show_error_codes():
    toml = toml_loads("""
        [tool.mypy]
        strict = true
        """)
    assert compute_check("MY102", pyproject=toml).result


def test_my102_fail_with_show_error_codes():
    toml = toml_loads("""
        [tool.mypy]
        show_error_codes = true
        """)
    assert not compute_check("MY102", pyproject=toml).result


def test_my103_present():
    toml = toml_loads("""
        [tool.mypy]
        warn_unreachable = true
        """)
    assert compute_check("MY103", pyproject=toml).result


def test_my103_missing():
    toml = toml_loads("""
        [tool.mypy]
        strict = true
        """)
    assert not compute_check("MY103", pyproject=toml).result


def test_my104_present():
    toml = toml_loads("""
        [tool.mypy]
        enable_error_code = ["ignore-without-code", "redundant-expr", "truthy-bool"]
        """)
    assert compute_check("MY104", pyproject=toml).result


def test_my104_missing():
    toml = toml_loads("""
        [tool.mypy]
        enable_error_code = ["redundant-expr", "truthy-bool"]
        """)
    assert not compute_check("MY104", pyproject=toml).result


def test_my105_present():
    toml = toml_loads("""
        [tool.mypy]
        enable_error_code = ["ignore-without-code", "redundant-expr", "truthy-bool"]
        """)
    assert compute_check("MY105", pyproject=toml).result


def test_my105_missing():
    toml = toml_loads("""
        [tool.mypy]
        enable_error_code = ["ignore-without-code", "truthy-bool"]
        """)
    assert not compute_check("MY105", pyproject=toml).result


def test_my106_present():
    toml = toml_loads("""
        [tool.mypy]
        enable_error_code = ["ignore-without-code", "redundant-expr", "truthy-bool"]
        """)
    assert compute_check("MY106", pyproject=toml).result


def test_my106_missing():
    toml = toml_loads("""
        [tool.mypy]
        enable_error_code = ["ignore-without-code", "redundant-expr"]
        """)
    assert not compute_check("MY106", pyproject=toml).result
