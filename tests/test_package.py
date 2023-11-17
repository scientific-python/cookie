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


@pytest.mark.parametrize("name", ["ruff_extend"])
def test_examples(name: str) -> None:
    package = DIR / "packages" / name
    _, results = process(package)

    failures = [r for r in results if r.result is not None and not r.result]
    assert not failures
