import json
import sys

import pytest
from repo_review.ghpath import GHPath
from repo_review.testing import compute_check

from sp_repo_review.checks._jsonc import strip_jsonc
from sp_repo_review.checks.renovate import renovate

# Real-world Renovate configs, one per supported format/location, pinned to a
# specific commit so upstream edits cannot break this. Skipped by default
# (network access, GitHub rate limits); run manually to confirm coverage.
REAL_WORLD_CONFIGS = [
    (
        "gulfofmaine/climatology_py_dash",
        "e4ead74d17d7c07dbb40b9c99fc1138f927abdd3",
        "renovate.json",
    ),
    (
        "jumpstarter-dev/jumpstarter",
        "8bae226d0a2d9cbe156bded24628e85c6d9f6cd9",
        "renovate.jsonc",
    ),
    (
        "SonarSource/docker-sonarqube",
        "9f00ce57d8654a3737ae0b22997d7198f71660d8",
        "renovate.json5",
    ),
    (
        "adobe/spectrum-css",
        "37620864c60c4c142a506017e1a15348a26abb0e",
        ".github/renovate.json",
    ),
    (
        "paddyroddy/.github",
        "c97ca7c448df211268616ce438777228fe103733",
        ".renovaterc.json5",
    ),
    (
        "zammad/zammad",
        "93fb7f107b07b4b4294e21249b277bc48c431da5",
        ".gitlab/renovate.json",
    ),
    (
        "prettier/eslint-config-prettier",
        "07829b4912d173986610a4985247896b09f9fcaf",
        ".renovaterc",
    ),
    (
        "Esri/calcite-design-system",
        "5613d9f8000ba12bf55c7da50e2f119c12435302",
        ".renovaterc.json",
    ),
]


def test_strip_jsonc_line_comment() -> None:
    text = '{\n  // a comment\n  "a": 1 // trailing\n}'
    assert json.loads(strip_jsonc(text)) == {"a": 1}


def test_strip_jsonc_block_comment() -> None:
    text = '{\n  /* multi\n     line */ "a": 1\n}'
    assert json.loads(strip_jsonc(text)) == {"a": 1}


def test_strip_jsonc_preserves_string_content() -> None:
    # Comment markers and commas inside strings must survive untouched.
    text = '{"url": "https://x/y", "csv": "a,b,", "block": "/* not a comment */"}'
    assert json.loads(strip_jsonc(text)) == {
        "url": "https://x/y",
        "csv": "a,b,",
        "block": "/* not a comment */",
    }


def test_strip_jsonc_escaped_quote_in_string() -> None:
    text = r'{"a": "she said \"hi\" // ok"}'
    assert json.loads(strip_jsonc(text)) == {"a": 'she said "hi" // ok'}


def test_strip_jsonc_trailing_commas() -> None:
    text = '{\n  "a": [1, 2, 3,],\n  "b": {"c": 1,},\n}'
    assert json.loads(strip_jsonc(text)) == {"a": [1, 2, 3], "b": {"c": 1}}


def test_strip_jsonc_plain_json_unchanged() -> None:
    text = '{"a": 1, "b": [1, 2]}'
    assert strip_jsonc(text) == text


def test_renovate_fixture_jsonc(tmp_path) -> None:
    (tmp_path / "renovate.jsonc").write_text(
        '{\n  // pin digests\n  "extends": ["config:recommended"],\n}',
        encoding="utf-8",
    )
    assert renovate(tmp_path) == {"extends": ["config:recommended"]}


def test_renovate_fixture_json5_fallback(tmp_path) -> None:
    pytest.importorskip("json5")
    # Unquoted keys are true JSON5 and cannot be stripped to plain JSON.
    (tmp_path / "renovate.json5").write_text(
        '{\n  extends: ["config:recommended"],\n}',
        encoding="utf-8",
    )
    assert renovate(tmp_path) == {"extends": ["config:recommended"]}


def test_renovate_fixture_json5_missing_errors(tmp_path, monkeypatch) -> None:
    (tmp_path / "renovate.json5").write_text(
        '{\n  extends: ["config:recommended"],\n}',
        encoding="utf-8",
    )
    # Simulate the json5 extra not being installed.
    monkeypatch.setitem(sys.modules, "json5", None)
    with pytest.raises(ImportError, match=r"sp-repo-review\[json5\]"):
        renovate(tmp_path)


@pytest.mark.skip(reason="Network access, can be rate limited")
@pytest.mark.parametrize(("repo", "sha", "location"), REAL_WORLD_CONFIGS)
def test_renovate_real_world(repo, sha, location) -> None:
    root = GHPath(repo=repo, branch=sha)
    assert root.joinpath(location).is_file()
    assert renovate(root)


def test_ren200() -> None:
    renovate = {"extends": ["config:recommended"]}
    assert compute_check("REN200", renovate=renovate).result


def test_ren200_missing() -> None:
    assert not compute_check("REN200", renovate={}).result


def test_ren210_gha_manager() -> None:
    renovate = {
        "github-actions": {
            "enabled": True,
        }
    }
    assert compute_check("REN210", renovate=renovate).result


def test_ren210_gha_manager_disabled() -> None:
    renovate = {
        "github-actions": {
            "enabled": False,
        }
    }
    assert not compute_check("REN210", renovate=renovate).result


def test_ren210_common_extends() -> None:
    renovate = {"extends": ["config:recommended"]}
    assert compute_check("REN210", renovate=renovate).result


def test_ren210_common_extends_missing() -> None:
    renovate = {"extends": ["some-other-config"]}
    assert not compute_check("REN210", renovate=renovate).result
