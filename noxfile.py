from __future__ import annotations

from pathlib import Path
import json
import os
import sys


import nox

DIR = Path(__file__).parent.resolve()
with DIR.joinpath("cookiecutter.json").open() as f:
    BACKENDS = json.load(f)["project_type"]

JOB_FILE = """\
default_context:
  project_name: cookie-{backend}
  project_type: {backend}
"""


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
        
    # Temporary workaround for https://github.com/pdm-project/pdm/issues/1411
    if backend == "pdm" and sys.version_info < (3, 8):
        session.run(backend, "install", "importlib_metadata<5")

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
