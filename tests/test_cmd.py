import subprocess

import pytest

pytest.importorskip("rich")


def test_cmd_help():
    subprocess.run(["repo-review", "--help"], check=True)


def test_cmd_basic():
    subprocess.run(["repo-review", "."], check=True)


def test_cmd_html():
    subprocess.run(["repo-review", ".", "--format", "html"], check=True)


def test_cmd_json():
    subprocess.run(["repo-review", ".", "--format", "json"], check=True)
