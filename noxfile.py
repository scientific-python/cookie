from __future__ import annotations

import json
import os
import re
import sys
import urllib.request
from pathlib import Path

import nox

DIR = Path(__file__).parent.resolve()
with DIR.joinpath("cookiecutter.json").open() as f:
    BACKENDS = json.load(f)["project_type"]

JOB_FILE = """\
default_context:
  project_name: cookie-{backend}
  project_type: {backend}
"""

nox.options.sessions = ["lint", "tests", "native"]


def make_cookie(session: nox.Session, backend: str) -> None:
    tmp_dir = session.create_tmp()
    # Nox sets TMPDIR to a relative path - fixed in nox 2022.1.7
    session.env["TMPDIR"] = os.path.abspath(tmp_dir)
    session.cd(tmp_dir)

    package_dir = Path(f"cookie-{backend}")

    with open("input.yml", "w") as f:
        f.write(JOB_FILE.format(backend=backend))

    session.run(
        "cookiecutter",
        "--no-input",
        str(DIR),
        "--config-file=input.yml",
    )
    session.cd(package_dir)
    session.run("git", "init", "-q", external=True)
    session.run("git", "add", ".", external=True)
    session.run(
        "git",
        "-c",
        "user.name=Bot",
        "-c",
        "user.email=bot@scikit-hep.org",
        "commit",
        "-qm",
        "feat: initial version",
        external=True,
    )
    session.run("git", "tag", "v0.1.0", external=True)


@nox.session()
@nox.parametrize("backend", BACKENDS, ids=BACKENDS)
def lint(session: nox.Session, backend: str) -> None:
    session.install("cookiecutter", "pre-commit")

    make_cookie(session, backend)

    session.run(
        "pre-commit",
        "run",
        "--all-files",
        "--hook-stage=manual",
        "--show-diff-on-failure",
    )


@nox.session
@nox.parametrize("backend", BACKENDS, ids=BACKENDS)
def autoupdate(session, backend):
    session.install("cookiecutter", "pre-commit")

    make_cookie(session, backend)

    session.run("pre-commit", "autoupdate")
    session.run("git", "diff", "--exit-code", external=True)


@nox.session()
@nox.parametrize("backend", BACKENDS, ids=BACKENDS)
def tests(session, backend):
    session.install("cookiecutter")

    make_cookie(session, backend)

    session.install(".[test]")
    session.run("python", "-m", "pytest", "-ra")


@nox.session()
@nox.parametrize("backend", ("poetry", "pdm", "hatch"), ids=("poetry", "pdm", "hatch"))
def native(session, backend):
    session.install("cookiecutter", backend)

    make_cookie(session, backend)

    if backend == "hatch":
        session.run(backend, "env", "create")
    else:
        session.run(backend, "install")

    session.run(backend, "run", "pytest")


@nox.session()
@nox.parametrize("backend", BACKENDS, ids=BACKENDS)
def dist(session, backend):
    session.install("cookiecutter", "build", "twine")

    make_cookie(session, backend)

    session.run("python", "-m", "build", silent=True)
    (sdist,) = Path("dist").glob("*.tar.gz")
    (wheel,) = Path("dist").glob("*.whl")

    if "0.1.0" not in str(wheel):
        session.error(f"{wheel} must be version 0.1.0")

    session.run("twine", "check", str(sdist), str(wheel))

    dist = DIR / "dist"
    dist.mkdir(exist_ok=True)
    sdist.rename(dist / sdist.stem)
    wheel.rename(dist / wheel.stem)


@nox.session(name="nox")
@nox.parametrize("backend", BACKENDS, ids=BACKENDS)
def nox_session(session, backend):
    session.install("cookiecutter", "nox")

    make_cookie(session, backend)

    if session.posargs:
        session.run("nox", "-s", *session.posargs)
    else:
        session.run("nox")


PC_VERS = re.compile(
    r"""\
^- repo: (.*?)
  rev: (.*?)$""",
    re.MULTILINE,
)

PC_REPL_LINE = '''\
- repo: {0}
  rev: "{1}"'''


GHA_VERS = re.compile(r"[\s\-]+uses: (.*?)@([^\s]+)")


@nox.session(reuse_venv=True)
def pc_bump(session: nox.Session) -> None:
    session.install("lastversion")

    style = Path("docs/pages/developers/style.md")
    txt = style.read_text()
    old_versions = {m[1]: m[2].strip('"') for m in PC_VERS.finditer(txt)}

    for proj, old_version in old_versions.items():
        new_version = session.run("lastversion", proj, silent=True).strip()

        if old_version.lstrip("v") == new_version:
            continue

        if old_version.startswith("v"):
            new_version = f"v{new_version}"

        before = PC_REPL_LINE.format(proj, old_version)
        after = PC_REPL_LINE.format(proj, new_version)

        session.log(f"Bump: {old_version} -> {new_version}")
        txt = txt.replace(before, after)

    style.write_text(txt)


@nox.session(venv_backend="none")
def gha_bump(session: nox.Session) -> None:
    pages = list(Path("docs/pages/developers").glob("gha_*.md"))
    pages.append(Path("docs/pages/developers/style.md"))
    full_txt = "\n".join(page.read_text() for page in pages)

    # This assumes there is a single version per action
    old_versions = {m[1]: m[2] for m in GHA_VERS.finditer(full_txt)}

    for repo, old_version in old_versions.items():
        print(f"{repo}: {old_version}")
        response = urllib.request.urlopen(f"https://api.github.com/repos/{repo}/tags")
        tags_js = json.loads(response.read())
        tags = [
            x["name"] for x in tags_js if x["name"].count(".") == old_version.count(".")
        ]
        new_version = tags[0]
        if new_version != old_version:
            print(f"Convert {repo}: {old_version} -> {new_version}")
            for page in pages:
                txt = page.read_text()
                txt = txt.replace(
                    f"uses: {repo}@{old_version}", f"uses: {repo}@{new_version}"
                )
                page.write_text(txt)


@nox.session(venv_backend=None)
def sync(session: nox.Session) -> None:
    for f in Path("docs/pages/developers").glob("*.md"):
        if f.name == "index.md":
            continue
        url = f"https://raw.githubusercontent.com/scikit-hep/scikit-hep.github.io/main/pages/developers/{f.name}"
        response = urllib.request.urlopen(url)
        f.write_text(response.read().decode("utf-8"))
