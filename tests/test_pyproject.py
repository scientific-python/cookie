import configparser
import inspect
from pathlib import Path

import pytest
from repo_review.testing import compute_check, toml_loads

from sp_repo_review.checks.pyproject import PytestFile
from sp_repo_review.checks.pyproject import pytest as pytest_fixture


def test_PP002_okay():
    toml = toml_loads("""
        [build-system]
        requires = ["setuptools"]
        build-backend = "setuptools.build_meta"
        """)
    assert compute_check("PP002", pyproject=toml).result


def test_PP002_not_list():
    toml = toml_loads("""
        [build-system]
        requires = "setuptools"
        build-backend = "setuptools.build_meta"
        """)
    assert not compute_check("PP002", pyproject=toml).result


def test_PP002_missing():
    toml = toml_loads("""
        [project]
        name = "hi"
        version = "1.0.0"
        """)
    assert not compute_check("PP002", pyproject=toml).result


def test_PP003_no_wheel():
    toml = toml_loads("""
        [build-system]
        requires = ["setuptools"]
        build-backend = "setuptools.build_meta"
        """)
    assert compute_check("PP003", pyproject=toml).result


def test_PP003_has_wheel():
    toml = toml_loads("""
        [build-system]
        requires = ["setuptools", "wheel"]
        build-backend = "setuptools.build_meta"
        """)
    assert not compute_check("PP003", pyproject=toml).result


def test_PP004_no_cap_pyproject():
    toml = toml_loads("""
       [project]
       requires-python = ">=3.10"
       """)

    assert compute_check("PP004", pyproject=toml, setupcfg=None).result


def test_PP004_cap_pyproject():
    toml = toml_loads("""
        [project]
        requires-python = ">=3.10, <4"
        """)

    assert compute_check("PP004", pyproject=toml, setupcfg=None).result is False


def test_PP004_cap_tilde_pyproject():
    toml = toml_loads("""
        [project]
        requires-python = "~=3.10"
        """)

    assert compute_check("PP004", pyproject=toml, setupcfg=None).result is False


def test_PP004_cap_caret_pyproject():
    toml = toml_loads("""
        [tool.poetry.dependencies]
        python = "^3.10"
       """)

    assert compute_check("PP004", pyproject=toml, setupcfg=None).result is False


def test_PP004_setup_cfg_no_cap():
    contents = inspect.cleandoc("""
        [options]
        python_requires = >=3.10
        """)
    config = configparser.ConfigParser()
    config.read_string(contents)

    assert compute_check("PP004", pyproject={}, setupcfg=config).result


def test_PP004_setup_cfg_cap():
    contents = inspect.cleandoc("""
        [options]
        python_requires = >=3.10,<4
        """)
    config = configparser.ConfigParser()
    config.read_string(contents)

    assert compute_check("PP004", pyproject={}, setupcfg=config).result is False


def test_PP004_setup_cfg_no_section():
    contents = inspect.cleandoc("""
        [other]
        python_requires = >=3.10
        """)
    config = configparser.ConfigParser()
    config.read_string(contents)

    assert not compute_check("PP004", pyproject={}, setupcfg=config).result


def test_PP004_setup_cfg_no_value():
    contents = inspect.cleandoc("""
        [options]
        other = >=3.10
        """)
    config = configparser.ConfigParser()
    config.read_string(contents)

    assert not compute_check("PP004", pyproject={}, setupcfg=config).result


def test_PP004_not_present():
    assert compute_check("PP004", pyproject={}, setupcfg=None).result is None


def test_PP005_no_license():
    toml = toml_loads("""
        [project]
        license.text = "MIT"
        classifiers = ["License :: OSI Approved :: MIT License"]
        """)

    assert compute_check("PP005", pyproject=toml).result is None


def test_PP005_pass():
    toml = toml_loads("""
        [project]
        license = "MIT"
        """)

    assert compute_check("PP005", pyproject=toml).result


def test_PP005_pass_empty_classifiers():
    toml = toml_loads("""
        [project]
        license = "MIT"
        classifiers = []
        """)

    assert compute_check("PP005", pyproject=toml).result


def test_PP005_pass_other_classifiers():
    toml = toml_loads("""
        [project]
        license = "MIT"
        classifiers = ["Something :: Else"]
        """)

    assert compute_check("PP005", pyproject=toml).result


def test_PP005_both():
    toml = toml_loads("""
        [project]
        license = "MIT"
        classifiers = ["License :: OSI Approved :: MIT License"]
        """)

    assert not compute_check("PP005", pyproject=toml).result


def test_PP006_present():
    toml = toml_loads("""
        [dependency-groups]
        dev = [ { include-group = "test" } ]
        test = [ "pytest" ]
        """)

    assert compute_check("PP006", pyproject=toml).result


def test_PP006_missing():
    toml = toml_loads("""
        [dependency-groups]
        test = [ "pytest" ]
        """)

    assert not compute_check("PP006", pyproject=toml).result


def test_PP302_okay_intstr():
    toml = toml_loads("""
        minversion = "7"
        """)

    assert compute_check("PP302", pytest=(PytestFile.LEGACY_PYPROJECT, toml)).result


def test_PP302_okay_modern():
    toml = toml_loads("""
        minversion = "9"
        """)
    assert compute_check("PP302", pytest=(PytestFile.LEGACY_PYPROJECT, toml)).result


def test_PP302_okay_verstr():
    toml = toml_loads("""
        minversion = "7.0.2"
        """)
    assert compute_check("PP302", pytest=(PytestFile.LEGACY_PYPROJECT, toml)).result


def test_PP302_okay_rawint():
    toml = toml_loads("""
        minversion = 7
        """)
    assert compute_check("PP302", pytest=(PytestFile.LEGACY_PYPROJECT, toml)).result


def test_PP302_okay_rawfloat():
    toml = toml_loads("""
        minversion = 7.0
        """)
    assert compute_check("PP302", pytest=(PytestFile.LEGACY_PYPROJECT, toml)).result


def test_PP302_missing():
    assert not compute_check("PP302", pytest=(PytestFile.NONE, {})).result


def test_PP302_too_low():
    toml = toml_loads("""
        minversion = "5"
        """)
    assert not compute_check("PP302", pytest=(PytestFile.LEGACY_PYPROJECT, toml)).result


def test_PP302_too_modern():
    toml = toml_loads("""
        minversion = "8"
        """)
    assert not compute_check("PP302", pytest=(PytestFile.MODERN_PYPROJECT, toml)).result


def test_PP303_okay():
    toml = toml_loads("""
        testpaths = ["tests"]
        """)
    assert compute_check("PP303", pytest=(PytestFile.LEGACY_PYPROJECT, toml)).result


def test_PP303_missing():
    assert not compute_check("PP303", pytest=(PytestFile.LEGACY_PYPROJECT, {})).result


def test_PP304_okay():
    toml = toml_loads("""
        log_level = "INFO"
        """)
    assert compute_check("PP304", pytest=(PytestFile.LEGACY_PYPROJECT, toml)).result


def test_PP304_alt_okay():
    toml = toml_loads("""
        log_cli_level = "INFO"
        """)
    assert compute_check("PP304", pytest=(PytestFile.LEGACY_PYPROJECT, toml)).result


def test_PP304_missing():
    assert not compute_check("PP304", pytest=(PytestFile.LEGACY_PYPROJECT, {})).result


def test_PP305_legacy_okay():
    toml = toml_loads("""
        xfail_strict = true
        """)
    assert compute_check("PP305", pytest=(PytestFile.LEGACY_PYPROJECT, toml)).result


def test_PP305_new_okay():
    toml = toml_loads("""
        strict_xfail = true
        """)
    assert compute_check("PP305", pytest=(PytestFile.LEGACY_PYPROJECT, toml)).result


def test_PP305_missing():
    assert not compute_check("PP305", pytest=(PytestFile.LEGACY_PYPROJECT, {})).result


def test_PP306_legacy_okay():
    toml = toml_loads("""
        addopts = ["--strict-config"]
        """)
    assert compute_check("PP306", pytest=(PytestFile.LEGACY_PYPROJECT, toml)).result


def test_PP306_new_okay():
    toml = toml_loads("""
        strict_config = true
        """)
    assert compute_check("PP306", pytest=(PytestFile.LEGACY_PYPROJECT, toml)).result


def test_PP306_missing():
    assert not compute_check("PP306", pytest=(PytestFile.LEGACY_PYPROJECT, {})).result


def test_PP307_legacy_okay():
    toml = toml_loads("""
        addopts = ["--strict-markers"]
        """)
    assert compute_check("PP307", pytest=(PytestFile.LEGACY_PYPROJECT, toml)).result


def test_PP307_new_okay():
    toml = toml_loads("""
        strict_markers = true
        """)
    assert compute_check("PP307", pytest=(PytestFile.LEGACY_PYPROJECT, toml)).result


def test_PP307_missing():
    assert not compute_check("PP307", pytest=(PytestFile.LEGACY_PYPROJECT, {})).result


def test_PP308_list_okay():
    toml = toml_loads("""
        addopts = ["-ra"]
        """)
    assert compute_check("PP308", pytest=(PytestFile.LEGACY_PYPROJECT, toml)).result


def test_PP308_list_missing():
    toml = toml_loads("""
        addopts = ["-otther"]
        """)
    assert not compute_check("PP308", pytest=(PytestFile.LEGACY_PYPROJECT, toml)).result


def test_PP308_string_okay():
    toml = toml_loads("""
        addopts = "--stuff -ra --morestuff"
        """)
    assert compute_check("PP308", pytest=(PytestFile.LEGACY_PYPROJECT, toml)).result


def test_PP308_string_not_okay():
    toml = toml_loads("""
        addopts = "--stuff -ra --morestuff"
        """)
    assert not compute_check("PP308", pytest=(PytestFile.MODERN_PYPROJECT, toml)).result


def test_PP308_string_missing():
    toml = toml_loads("""
        addopts = "--stuff --morestuff"
        """)
    assert not compute_check("PP308", pytest=(PytestFile.LEGACY_PYPROJECT, toml)).result


@pytest.mark.parametrize(
    "loc",
    [PytestFile.LEGACY_PYPROJECT, PytestFile.MODERN_PYPROJECT, PytestFile.PYTEST_TOML],
)
def test_PP30x_strict_okay(loc: PytestFile):
    toml = toml_loads("""
        strict = true
        """)
    assert compute_check("PP305", pytest=(loc, toml)).result
    assert compute_check("PP306", pytest=(loc, toml)).result
    assert compute_check("PP307", pytest=(loc, toml)).result


def test_pytest_fixture_legacy(tmp_path: Path):
    toml = toml_loads("""
        [tool.pytest.ini_options]
        addopts = ["-ra", "--strict-config", "--strict-markers"]
        """)
    result = pytest_fixture(pyproject=toml, root=tmp_path)
    assert result == (
        PytestFile.LEGACY_PYPROJECT,
        {"addopts": ["-ra", "--strict-config", "--strict-markers"]},
    )


def test_pytest_fixture_modern(tmp_path: Path):
    toml = toml_loads("""
        [tool.pytest]
        addopts = ["-ra", "--strict-config", "--strict-markers"]
        """)
    result = pytest_fixture(pyproject=toml, root=tmp_path)
    assert result == (
        PytestFile.MODERN_PYPROJECT,
        {"addopts": ["-ra", "--strict-config", "--strict-markers"]},
    )


def test_pytest_fixture_none(tmp_path: Path):
    toml = toml_loads("""
        [tool.other]
        something = true
        """)
    result = pytest_fixture(pyproject=toml, root=tmp_path)
    assert result == (PytestFile.NONE, {})


@pytest.mark.parametrize("filename", ["pytest.toml", ".pytest.toml"])
def test_pytest_fixture_pytest_toml(tmp_path: Path, filename: str):
    (tmp_path / filename).write_text(
        inspect.cleandoc("""
        [pytest]
        addopts = ["-ra", "--strict-config", "--strict-markers"]
        """),
        encoding="utf-8",
    )
    result = pytest_fixture(pyproject={}, root=tmp_path)
    assert result == (
        PytestFile.PYTEST_TOML,
        {"addopts": ["-ra", "--strict-config", "--strict-markers"]},
    )
