from repo_review.testing import compute_check


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
