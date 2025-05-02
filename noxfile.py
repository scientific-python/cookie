"""
Nox runner for cookie & sp-repo-review.

sp-repo-review checks start with "rr-".
"""

from __future__ import annotations

import difflib
import email.message
import functools
import json
import os
import re
import shutil
import stat
import sys
import tarfile
import urllib.error
import urllib.request
import zipfile
from collections.abc import Callable
from pathlib import Path
from typing import Any

import nox

nox.needs_version = ">=2025.2.9"
nox.options.sessions = ["rr_lint", "rr_tests", "rr_pylint", "readme"]
nox.options.default_venv_backend = "uv|virtualenv"


DIR = Path(__file__).parent.resolve()
with DIR.joinpath("cookiecutter.json").open() as f:
    BACKENDS = json.load(f)["backend"]

JOB_FILE = """\
default_context:
  project_name: cookie-{backend}
  backend: {backend}
  vcs: {vcs}
"""


def _remove_readonly(func: Callable[[str], None], path: str, _: object) -> None:
    os.chmod(path, stat.S_IWRITE)  # noqa: PTH101
    func(path)


def rmtree_ro(path: Path) -> None:
    if sys.version_info >= (3, 12):
        shutil.rmtree(path, onexc=_remove_readonly)
    else:
        shutil.rmtree(path, onerror=_remove_readonly)


def get_expected_version(backend: str, vcs: bool) -> str:
    return "0.2.3" if vcs and backend not in {"maturin", "mesonpy"} else "0.1.0"


def make_copier(session: nox.Session, backend: str, vcs: bool) -> None:
    package_dir = Path(f"copy-{backend}")
    if package_dir.exists():
        rmtree_ro(package_dir)

    session.run(
        "copier",
        "copy",
        f"{DIR}",
        f"{package_dir}",
        "--defaults",
        "--trust",
        "--vcs-ref=HEAD",
        f"--data=project_name=cookie-{backend}",
        "--data=org=org",
        f"--data=backend={backend}",
        "--data=full_name=My Name",
        "--data=email=me@email.com",
        "--data=license=BSD",
        f"--data=vcs={vcs}",
    )

    init_git(session, package_dir)

    return package_dir


def make_cookie(session: nox.Session, backend: str, vcs: bool) -> None:
    package_dir = Path(f"cookie-{backend}")
    if package_dir.exists():
        rmtree_ro(package_dir)

    Path("input.yml").write_text(
        JOB_FILE.format(backend=backend, vcs=vcs), encoding="utf-8"
    )

    session.run(
        "cookiecutter",
        "--no-input",
        f"{DIR}",
        "--config-file=input.yml",
    )

    init_git(session, package_dir)

    return package_dir


def make_cruft(session: nox.Session, backend: str, vcs: bool) -> None:
    package_dir = Path(f"cruft-{backend}")
    if package_dir.exists():
        rmtree_ro(package_dir)

    tmp_dir = Path("tmp_loc")
    tmp_dir.mkdir()

    session.cd(tmp_dir)
    Path("input.yml").write_text(
        JOB_FILE.format(backend=backend, pkg=package_dir, vcs=vcs), encoding="utf-8"
    )
    session.run(
        "cruft",
        "create",
        "--no-input",
        f"{DIR}",
        "--config-file=input.yml",
    )
    session.cd("..")
    tmp_dir.joinpath(f"cookie-{backend}").rename(package_dir)
    shutil.rmtree(tmp_dir)

    init_git(session, package_dir)

    return package_dir


def init_git(session: nox.Session, package_dir: Path) -> None:
    session.run("git", "-C", f"{package_dir}", "init", "-q", external=True)
    session.run("git", "-C", f"{package_dir}", "add", ".", external=True)
    session.run(
        "git",
        "-C",
        f"{package_dir}",
        "-c",
        "user.name=Bot",
        "-c",
        "user.email=bot@scikit-hep.org",
        "commit",
        "-qm",
        "feat: initial version",
        external=True,
    )
    session.run("git", "-C", f"{package_dir}", "tag", "v0.2.3", external=True)


IGNORE_FILES = {"__pycache__", ".git", ".copier-answers.yml", ".cruft.json"}


def valid_path(path: Path):
    return path.is_file() and not IGNORE_FILES & set(path.parts)


def diff_files(p1: Path, p2: Path) -> bool:
    f1set = {p.relative_to(p1) for p in p1.rglob("*") if valid_path(p)}
    f2set = {p.relative_to(p2) for p in p2.rglob("*") if valid_path(p)}

    same = True

    for f in sorted(f1set | f2set):
        f1 = p1 / f
        f2 = p2 / f
        with f1.open(encoding="utf-8") as c1, f2.open(encoding="utf-8") as c2:
            diff = list(
                difflib.unified_diff(c1.readlines(), c2.readlines(), f"{f1}", f"{f2}")
            )
        if diff:
            sys.stdout.writelines(diff)
            same = False

    return same


@nox.session(default=False)
@nox.parametrize("vcs", [False, True], ids=["novcs", "vcs"])
@nox.parametrize("backend", BACKENDS, ids=BACKENDS)
def lint(session: nox.Session, backend: str, vcs: bool) -> None:
    session.install("cookiecutter", "pre-commit")

    tmp_dir = session.create_tmp()
    session.cd(tmp_dir)
    cookie = make_cookie(session, backend, vcs)
    session.chdir(cookie)

    session.run(
        "pre-commit",
        "run",
        "--all-files",
        "--hook-stage=manual",
        "--show-diff-on-failure",
    )


@nox.session(default=False)
@nox.parametrize("backend", BACKENDS, ids=BACKENDS)
def autoupdate(session: nox.Session, backend: str) -> None:
    session.install("cookiecutter", "pre-commit")

    tmp_dir = session.create_tmp()
    session.cd(tmp_dir)
    cookie = make_cookie(session, backend, True)
    session.chdir(cookie)

    session.run("pre-commit", "autoupdate")
    session.run("git", "diff", "--exit-code", external=True)


@nox.session(default=False)
@nox.parametrize("vcs", [False, True], ids=["novcs", "vcs"])
@nox.parametrize("backend", BACKENDS, ids=BACKENDS)
def tests(session: nox.Session, backend: str, vcs: bool) -> None:
    session.install("cookiecutter")

    tmp_dir = session.create_tmp()
    session.cd(tmp_dir)
    cookie = make_cookie(session, backend, vcs)
    session.chdir(cookie)

    name = f"cookie-{backend}"
    session.install(".", "--group=test")
    session.run("python", "-m", "pytest", "-ra")
    version = session.run(
        "python",
        "-c",
        f'import importlib.metadata as m; print(m.version("{name}"))',
        silent=True,
    ).strip()
    expected_version = get_expected_version(backend, vcs)
    assert version == expected_version, f"{version=} != {expected_version=}"


@nox.session(default=False)
@nox.parametrize("vcs", [False, True], ids=["novcs", "vcs"])
@nox.parametrize("backend", ("poetry", "pdm", "hatch"), ids=("poetry", "pdm", "hatch"))
def native(session: nox.Session, backend: str, vcs: bool) -> None:
    session.install("cookiecutter", backend)

    tmp_dir = session.create_tmp()
    session.cd(tmp_dir)
    cookie = make_cookie(session, backend, vcs)
    session.chdir(cookie)

    if backend == "hatch":
        session.run(backend, "run", "test")
    elif backend == "poetry":
        session.run(backend, "sync", env={"VIRTUAL_ENV": None})
        session.run(backend, "run", "pytest", env={"VIRTUAL_ENV": None})
    else:
        session.run(backend, "install")
        session.run(backend, "run", "pytest")


@nox.session(default=False)
@nox.parametrize("vcs", [False, True], ids=["novcs", "vcs"])
@nox.parametrize("backend", BACKENDS, ids=BACKENDS)
def dist(session: nox.Session, backend: str, vcs: bool) -> None:
    session.install("cookiecutter", "build", "twine")

    tmp_dir = session.create_tmp()
    session.cd(tmp_dir)
    cookie = make_cookie(session, backend, vcs)
    session.chdir(cookie)

    session.run("python", "-m", "build", silent=True)
    (sdist,) = Path("dist").glob("*.tar.gz")
    (wheel,) = Path("dist").glob("*.whl")

    expected_version = get_expected_version(backend, vcs)
    if expected_version not in str(wheel):
        session.error(f"{wheel} must be version {expected_version}")

    session.run("twine", "check", f"{sdist}", f"{wheel}")

    # Check for LICENSE in SDist
    with tarfile.open(sdist) as tf:
        names = tf.getnames()
        if backend not in {"mesonpy", "poetry", "maturin"}:
            (metadata_path,) = (
                n for n in names if n.endswith("PKG-INFO") and "egg-info" not in n
            )
            with tf.extractfile(metadata_path) as mfile:
                info = mfile.read().decode("utf-8")
                if "License-Expression: BSD-3-Clause" not in info:
                    msg = "License expression not found in METADATA"
                    session.error(msg)
    if not any(n.endswith("LICENSE") for n in names):
        msg = f"license file missing from {backend} vcs={vcs}'s sdist. Found: {names}"
        session.error(msg)

    # Check for LICENSE in wheel
    with zipfile.ZipFile(wheel) as zf:
        names = zf.namelist()
        metadata_path = next(iter(n for n in names if n.endswith("METADATA")))
        with zf.open(metadata_path) as mfile:
            txt = mfile.read()
    license_fields = email.message.EmailMessage(txt).get_all("License", [])
    if license_fields:
        msg = f"Should not have anything in the License slot, got {license_fields}"
        session.error(msg)
    if not any(n.endswith("LICENSE") for n in names):
        msg = f"license file missing from {backend} vcs={vcs}'s wheel. Found: {names}"
        session.error(msg)

    dist = DIR / "dist"
    dist.mkdir(exist_ok=True)
    sdist.rename(dist / sdist.stem)
    wheel.rename(dist / wheel.stem)


@nox.session(name="nox", default=False)
@nox.parametrize("vcs", [False, True], ids=["novcs", "vcs"])
@nox.parametrize("backend", BACKENDS, ids=BACKENDS)
def nox_session(session: nox.Session, backend: str, vcs: bool) -> None:
    session.install("cookiecutter", "nox")

    tmp_dir = session.create_tmp()
    session.cd(tmp_dir)
    cookie = make_cookie(session, backend, vcs)
    session.chdir(cookie)

    if session.posargs:
        session.run("nox", "-s", *session.posargs)
    else:
        session.run("nox")


@nox.session(default=False)
def compare_copier(session):
    session.install("cookiecutter", "copier", "copier-templates-extensions")

    tmp_dir = session.create_tmp()
    session.cd(tmp_dir)

    for backend in BACKENDS:
        for vcs in (False, True):
            cookie = make_cookie(session, backend, vcs)
            copier = make_copier(session, backend, vcs)

            if diff_files(cookie, copier):
                session.log(f"{backend} {vcs=} passed")
            else:
                session.error(f"{backend} {vcs=} files are not the same!")


@nox.session(default=False)
def compare_cruft(session):
    session.install("cookiecutter", "cruft")

    tmp_dir = session.create_tmp()
    session.cd(tmp_dir)

    for backend in BACKENDS:
        for vcs in (False, True):
            cookie = make_cookie(session, backend, vcs)
            cruft = make_cruft(session, backend, vcs)

            if diff_files(cookie, cruft):
                session.log(f"{backend} {vcs=} passed")
            else:
                session.error(f"{backend} {vcs=} files are not the same!")


PC_VERS = re.compile(
    r"""\
^( *)- repo: (.*?)
 *  rev: (.*?)$""",
    re.MULTILINE,
)

PC_REPL_LINE = """\
{2}- repo: {0}
{2}  rev: {3}{1}{3}"""


GHA_VERS = re.compile(r"[\s\-]+uses: (.*?)@([^\s]+)")


@nox.session(reuse_venv=True, default=False)
def pc_bump(session: nox.Session) -> None:
    """
    Bump the pre-commit versions.
    """
    session.install("lastversion>=3.4")
    versions = {}
    pages = [
        Path("docs/pages/guides/style.md"),
        Path("{{cookiecutter.project_name}}/.pre-commit-config.yaml"),
        Path(".pre-commit-config.yaml"),
    ]

    for page in pages:
        txt = page.read_text()
        old_versions = {m[2]: (m[3].strip('"'), m[1]) for m in PC_VERS.finditer(txt)}

        for proj, (old_version, space) in old_versions.items():
            if proj not in versions:
                versions[proj] = session.run(
                    "lastversion",
                    "--at=github",
                    "--format=tag",
                    "--exclude=~alpha|beta|rc",
                    proj,
                    silent=True,
                ).strip()
            new_version = versions[proj]

            after = PC_REPL_LINE.format(proj, new_version, space, '"')

            session.log(f"Bump {proj}: {old_version} -> {new_version} ({page})")
            txt = txt.replace(PC_REPL_LINE.format(proj, old_version, space, '"'), after)
            txt = txt.replace(PC_REPL_LINE.format(proj, old_version, space, ""), after)

            page.write_text(txt)


@functools.lru_cache(maxsize=None)  # noqa: UP033
def get_latest_version_tag(repo: str, old_version: str) -> dict[str, Any] | None:
    auth = os.environ.get("GITHUB_TOKEN", os.environ.get("GITHUB_API_TOKEN", ""))
    request = urllib.request.Request(
        f"https://api.github.com/repos/{repo}/tags?per_page=100"
    )
    request.add_header("Accept", "application/vnd.github+json")
    request.add_header("X-GitHub-Api-Version", "2022-11-28")
    if auth:
        request.add_header("Authorization", f"Bearer: {auth}")
    try:
        response = urllib.request.urlopen(request)
    except urllib.error.HTTPError as err:
        err.add_note(f"URL: {request.full_url}")
        raise

    results = json.loads(response.read())
    if not results:
        msg = f"No results for {repo}"
        raise RuntimeError(msg)
    tags = [
        x["name"]
        for x in results
        if x["name"].count(".") == old_version.count(".")
        and x["name"].startswith("v") == old_version.startswith("v")
    ]
    if tags:
        return tags[0]
    return None


@nox.session(venv_backend="none", default=False)
def gha_bump(session: nox.Session) -> None:
    """
    Bump the GitHub Actions.
    """
    pages = list(Path("docs/pages/guides").glob("gha_*.md"))
    pages.extend(Path("{{cookiecutter.project_name}}/.github/workflows").iterdir())
    pages.append(Path("docs/pages/guides/style.md"))
    pages.append(Path("docs/pages/guides/tasks.md"))
    pages.append(Path("docs/pages/guides/coverage.md"))
    full_txt = "\n".join(page.read_text() for page in pages)

    # This assumes there is a single version per action
    old_versions = {m[1]: m[2] for m in GHA_VERS.finditer(full_txt)}

    for repo, old_version in old_versions.items():
        session.log(f"{repo}: {old_version}")
        new_version = get_latest_version_tag(repo, old_version)
        if not new_version:
            continue
        if new_version != old_version:
            session.log(f"Convert {repo}: {old_version} -> {new_version}")
            for page in pages:
                txt = page.read_text()
                txt = txt.replace(
                    f"uses: {repo}@{old_version}", f"uses: {repo}@{new_version}"
                )
                page.write_text(txt)


# -- Repo review --


@nox.session(tags=["gen"])
def readme(session: nox.Session) -> None:
    """
    Update the readme with cog. Pass --check to check instead.
    """

    args = session.posargs or ["-r"]

    session.install("-e.", "cogapp", "repo-review>=0.8")
    session.run("cog", "-P", *args, "README.md")


@nox.session(reuse_venv=True, default=False)
def rr_run(session: nox.Session) -> None:
    """
    Run sp-repo-review.
    """

    session.install("-e.[cli]")
    session.run("python", "-m", "repo_review", *session.posargs)


@nox.session
def rr_lint(session: nox.Session) -> None:
    """
    Run the linter.
    """
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files", *session.posargs)


@nox.session
def rr_pylint(session: nox.Session) -> None:
    """
    Run Pylint.
    """
    # This needs to be installed into the package environment, and is slower
    # than a pre-commit check
    session.install("-e.[cli]", "pylint")
    session.run("pylint", "src", *session.posargs)


@nox.session
def rr_tests(session: nox.Session) -> None:
    """
    Run the unit and regular tests for sp-repo-review.
    """
    pyproject = nox.project.load_toml()
    test_deps = nox.project.dependency_groups(pyproject, "test")

    session.install("-e.[cli]", *test_deps)
    session.run("pytest", *session.posargs, env={"PYTHONWARNDEFAULTENCODING": "1"})


@nox.session(reuse_venv=True, default=False)
def rr_build(session: nox.Session) -> None:
    """
    Build an SDist and wheel for sp-repo-review.
    """

    session.install("build")
    session.run("python", "-m", "build")
