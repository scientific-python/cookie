from pathlib import Path

import pytest
import yaml
from repo_review.testing import compute_check


@pytest.mark.parametrize("readthedocs", [".readthedocs.yml", ".readthedocs.yaml"])
def test_rtd100(tmp_path: Path, readthedocs: str) -> None:
    simple = tmp_path / "simple"
    simple.mkdir()
    simple.joinpath(readthedocs).touch()
    assert compute_check("RTD100", root=simple).result


def test_rtd101_true() -> None:
    readthedocs = yaml.safe_load("""
        version: 2
    """)
    assert compute_check("RTD101", readthedocs=readthedocs).result


def test_rtd101_false() -> None:
    readthedocs = yaml.safe_load("""
        other: 2
    """)
    assert not compute_check("RTD101", readthedocs=readthedocs).result


def test_rtd102_true() -> None:
    readthedocs = yaml.safe_load("""
        build:
          os: ubuntu-22.04
    """)
    assert compute_check("RTD102", readthedocs=readthedocs).result


def test_rtd102_false() -> None:
    readthedocs = yaml.safe_load("""
        build:
          python: "3.12"
    """)
    assert not compute_check("RTD102", readthedocs=readthedocs).result


def test_rtd103_true() -> None:
    readthedocs = yaml.safe_load("""
        build:
          tools:
            python: "3.12"
    """)
    assert compute_check("RTD103", readthedocs=readthedocs).result


def test_rtd103_false() -> None:
    readthedocs = yaml.safe_load("""
        build:
          os: ubuntu-22.04
    """)
    assert not compute_check("RTD103", readthedocs=readthedocs).result


def test_rtd104_commands() -> None:
    readthedocs = yaml.safe_load("""
        build:
          commands: []
    """)
    assert compute_check("RTD104", readthedocs=readthedocs).result


def test_rtd104_sphinx() -> None:
    readthedocs = yaml.safe_load("""
        sphinx:
          configuration: docs/conf.py
    """)
    assert compute_check("RTD104", readthedocs=readthedocs).result


def test_rtd104_mkdocs() -> None:
    readthedocs = yaml.safe_load("""
        mkdocs:
          configuration: docs/mkdocs.yml
    """)
    assert compute_check("RTD104", readthedocs=readthedocs).result


def test_rtd104_false() -> None:
    readthedocs = yaml.safe_load("""
        build:
    """)
    assert not compute_check("RTD104", readthedocs=readthedocs).result
