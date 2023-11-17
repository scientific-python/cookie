from __future__ import annotations

from sp_repo_review.checks.ruff import merge


def test_merge():
    a = {"a": 1, "b": [1], "c": {"aa": 2, "bb": [2]}, "d": {"one": 1}}
    b = {"b": [3], "c": {"bb": [4], "cc": 5}, "e": {"two": 2}}

    assert merge(a, b) == {
        "a": 1,
        "b": [3],
        "c": {"aa": 2, "bb": [4], "cc": 5},
        "d": {"one": 1},
        "e": {"two": 2},
    }
