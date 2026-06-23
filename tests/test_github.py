import yaml
from repo_review.testing import compute_check


def test_gh100() -> None:
    workflows = yaml.safe_load(
        """
        ci:
          name: CI
        """
    )
    assert compute_check("GH100", workflows=workflows).result


def test_gh100_missing() -> None:
    assert not compute_check("GH100", workflows={}).result


def test_gh101() -> None:
    workflows = yaml.safe_load(
        """
        ci:
          name: CI
        docs:
          name: Docs
        """
    )
    assert compute_check("GH101", workflows=workflows).result


def test_gh101_missing_names() -> None:
    workflows = yaml.safe_load(
        """
        ci:
          name: CI
        docs:
          jobs: {}
        """
    )
    assert not compute_check("GH101", workflows=workflows).result


def test_gh102() -> None:
    workflows = yaml.safe_load(
        """
        ci:
          concurrency:
            group: ${{ github.workflow }}-${{ github.ref }}
            cancel-in-progress: true
        """
    )
    assert compute_check("GH102", workflows=workflows).result


def test_gh102_missing_concurrency() -> None:
    workflows = yaml.safe_load(
        """
        ci:
          jobs: {}
        """
    )
    assert not compute_check("GH102", workflows=workflows).result


def test_gh103() -> None:
    workflows = yaml.safe_load(
        """
        ci:
          on:
            workflow_dispatch:
        """
    )
    assert compute_check("GH103", workflows=workflows).result


def test_gh103_missing_dispatch() -> None:
    workflows = yaml.safe_load(
        """
        ci:
          on:
            push:
        """
    )
    assert not compute_check("GH103", workflows=workflows).result


def test_gh104() -> None:
    workflows = yaml.safe_load(
        """
        cd:
          jobs:
            wheels:
              strategy:
                matrix:
                  python: ["3.11", "3.12"]
              steps:
                - uses: actions/upload-artifact@v4
                  with:
                    name: wheels-${{ matrix.python }}
            sdist:
              steps:
                - uses: actions/upload-artifact@v4
                  with:
                    name: sdist
                - uses: actions/upload-artifact@v4
                  with:
                    name: docs
        """
    )
    assert compute_check("GH104", workflows=workflows).result


def test_gh104_duplicate_names() -> None:
    workflows = yaml.safe_load(
        """
        cd:
          jobs:
            wheels:
              steps:
                - uses: actions/upload-artifact@v4
                  with:
                    name: wheel
                - uses: actions/upload-artifact@v4
                  with:
                    name: wheel
        """
    )
    res = compute_check("GH104", workflows=workflows)
    assert not res.result
    assert "Multiple matching upload artifact names" in res.err_msg


def test_gh104_matrix_without_substitution() -> None:
    workflows = yaml.safe_load(
        """
        cd:
          jobs:
            wheels:
              strategy:
                matrix:
                  python: ["3.11", "3.12"]
              steps:
                - uses: actions/upload-artifact@v4
                  with:
                    name: wheel
        """
    )
    res = compute_check("GH104", workflows=workflows)
    assert not res.result
    assert "No variable substitutions were detected" in res.err_msg


def test_gh105_trusted_publishing() -> None:
    workflows = yaml.safe_load(
        """
        cd:
          jobs:
            publish:
              steps:
                - uses: pypa/gh-action-pypi-publish@release/v1
        """
    )
    assert compute_check("GH105", workflows=workflows).result


def test_gh105_token_based_upload() -> None:
    workflows = yaml.safe_load(
        """
        cd:
          jobs:
            publish:
              steps:
                - uses: pypa/gh-action-pypi-publish@release/v1
                  with:
                    password: ${{ secrets.pypi_password }}
        """
    )
    res = compute_check("GH105", workflows=workflows)
    assert not res.result
    assert "Token-based publishing" in res.err_msg


def test_gh200() -> None:
    dependabot = yaml.safe_load(
        """
        version: 2
        updates:
          - package-ecosystem: github-actions
            directory: "/"
            schedule:
              interval: weekly
        """
    )
    assert compute_check("GH200", dependabot=dependabot).result


def test_gh200_missing() -> None:
    assert not compute_check("GH200", dependabot={}).result


def test_gh210() -> None:
    dependabot = yaml.safe_load(
        """
        version: 2
        updates:
          - package-ecosystem: github-actions
            directory: "/"
            schedule:
              interval: weekly
        """
    )
    assert compute_check("GH210", dependabot=dependabot).result


def test_gh210_missing_github_actions() -> None:
    dependabot = yaml.safe_load(
        """
        version: 2
        updates:
          - package-ecosystem: pip
            directory: "/"
            schedule:
              interval: weekly
        """
    )
    assert not compute_check("GH210", dependabot=dependabot).result


def test_gh211() -> None:
    dependabot = yaml.safe_load(
        """
        version: 2
        updates:
          - package-ecosystem: github-actions
            directory: "/"
            schedule:
              interval: weekly
            ignore:
              - dependency-name: pypa/cibuildwheel
        """
    )
    assert compute_check("GH211", dependabot=dependabot).result


def test_gh211_pins_major_core_actions() -> None:
    dependabot = yaml.safe_load(
        """
        version: 2
        updates:
          - package-ecosystem: github-actions
            directory: "/"
            schedule:
              interval: weekly
            ignore:
              - dependency-name: actions/*
        """
    )
    assert not compute_check("GH211", dependabot=dependabot).result


def test_gh212() -> None:
    dependabot = yaml.safe_load(
        """
        version: 2
        updates:
          - package-ecosystem: github-actions
            directory: "/"
            schedule:
              interval: weekly
            groups:
              actions:
                patterns:
                  - "*"
        """
    )
    assert compute_check("GH212", dependabot=dependabot).result


def test_gh212_missing_groups() -> None:
    dependabot = yaml.safe_load(
        """
        version: 2
        updates:
          - package-ecosystem: github-actions
            directory: "/"
            schedule:
              interval: weekly
        """
    )
    assert not compute_check("GH212", dependabot=dependabot).result
