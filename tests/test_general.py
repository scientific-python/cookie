from pathlib import Path

import pytest
from repo_review.testing import compute_check

from sp_repo_review._compat import tomllib


def test_py001(tmp_path: Path):
    simple = tmp_path / "simple"
    simple.mkdir()
    simple.joinpath("pyproject.toml").touch()
    assert compute_check("PY001", package=simple).result


def test_py001_missing(tmp_path: Path):
    simple = tmp_path / "simple"
    simple.mkdir()
    assert not compute_check("PY001", package=simple).result


@pytest.mark.parametrize("readme", ["README.md", "README.rst"])
def test_py002(tmp_path: Path, readme: str):
    simple = tmp_path / "simple"
    simple.mkdir()
    simple.joinpath(readme).touch()
    assert compute_check("PY002", root=simple).result


def test_py002_missing(tmp_path: Path):
    simple = tmp_path / "simple"
    simple.mkdir()
    assert not compute_check("PY002", root=simple).result


@pytest.mark.parametrize("license", ["LICENSE", "LICENCE", "COPYING"])
def test_py003(tmp_path: Path, license: str):
    simple = tmp_path / "simple"
    simple.mkdir()
    simple.joinpath(license).touch()
    assert compute_check("PY003", package=simple).result


def test_py003_missing(tmp_path: Path):
    simple = tmp_path / "simple"
    simple.mkdir()
    assert not compute_check("PY003", package=simple).result


def test_py004(tmp_path: Path):
    simple = tmp_path / "simple"
    simple.mkdir()
    simple.joinpath("docs").mkdir()
    assert compute_check("PY004", package=simple).result


def test_py004_not_dir(tmp_path: Path):
    simple = tmp_path / "simple"
    simple.mkdir()
    simple.joinpath("docs")
    assert not compute_check("PY004", package=simple).result


def test_py004_missing(tmp_path: Path):
    simple = tmp_path / "simple"
    simple.mkdir()
    assert not compute_check("PY004", package=simple).result


def test_py005(tmp_path: Path):
    simple = tmp_path / "simple"
    simple.mkdir()
    simple.joinpath("tests").mkdir()
    assert compute_check("PY005", package=simple).result


def test_py005_alt_singular(tmp_path: Path):
    simple = tmp_path / "simple"
    simple.mkdir()
    simple.joinpath("test").mkdir()
    assert compute_check("PY005", package=simple).result


def test_py005_alt_integration(tmp_path: Path):
    simple = tmp_path / "simple"
    simple.mkdir()
    simple.joinpath("tests-integration").mkdir()
    assert compute_check("PY005", package=simple).result


def test_py005_not_folder(tmp_path: Path):
    simple = tmp_path / "simple"
    simple.mkdir()
    simple.joinpath("tests")
    assert not compute_check("PY005", package=simple).result


def test_py005_not_tests(tmp_path: Path):
    simple = tmp_path / "simple"
    simple.mkdir()
    simple.joinpath("fastest").mkdir()
    assert not compute_check("PY005", package=simple).result


def test_py005_missing(tmp_path: Path):
    simple = tmp_path / "simple"
    simple.mkdir()
    assert not compute_check("PY005", package=simple).result


def test_py005_src(tmp_path: Path):
    simple = tmp_path / "simple"
    simple.mkdir()
    src = simple.joinpath("src")
    src.mkdir()
    pkg = src.joinpath("pkg")
    pkg.mkdir()
    pkg.joinpath("tests").mkdir()
    assert compute_check("PY005", package=simple).result


def test_py005_src_missing(tmp_path: Path):
    simple = tmp_path / "simple"
    simple.mkdir()
    src = simple.joinpath("src")
    src.mkdir()
    assert not compute_check("PY005", package=simple).result


def test_py006(tmp_path: Path):
    simple = tmp_path / "simple"
    simple.mkdir()
    simple.joinpath(".pre-commit-config.yaml").touch()
    assert compute_check("PY006", root=simple).result


def test_py006_missing(tmp_path: Path):
    simple = tmp_path / "simple"
    simple.mkdir()
    assert not compute_check("PY006", root=simple).result


@pytest.mark.parametrize("runnerfile", ["noxfile.py", "tox.ini", "pixi.toml"])
def test_py007(tmp_path: Path, runnerfile: str):
    simple = tmp_path / "simple"
    simple.mkdir()
    simple.joinpath(runnerfile).touch()
    assert compute_check("PY007", root=simple, pyproject={}).result


@pytest.mark.parametrize(
    "section",
    [
        "[tool.hatch.envs]",
        "[tool.spin]",
        "[tool.tox]",
        "[tool.pixi.tasks]",
        "[tool.pixi.feature.thing.tasks]",
    ],
)
def test_py007_pyproject_sections(tmp_path: Path, section: str):
    pyproject = tomllib.loads(section)
    simple = tmp_path / "simple"
    simple.mkdir()
    assert compute_check("PY007", root=simple, pyproject=pyproject).result


def test_py007_missing(tmp_path: Path):
    simple = tmp_path / "simple"
    simple.mkdir()
    assert not compute_check("PY007", root=simple, pyproject={}).result
