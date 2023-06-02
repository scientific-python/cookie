from __future__ import annotations

from pathlib import Path

import pytest

import repo_review as m
from repo_review.ghpath import GHPath
from repo_review.processor import process

DIR = Path(__file__).parent.resolve()


def test_version():
    assert m.__version__


@pytest.mark.skip(reason="Can be rate limited")
def test_pyodide():
    pytest.importorskip("sp_repo_review")
    package = GHPath(repo="scientific-python/repo-review", branch="main")
    results = process(package)
    assert results


def test_local():
    package = DIR.parent
    results = process(package)
    assert results
