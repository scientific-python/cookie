import nox
from pathlib import Path

DIR = Path(__file__).parent.resolve()
BACKENDS = "setuptools", "pybind11", "poetry", "flit", "flit621", "trampolim", "whey"

JOB_FILE = """\
default_context:
  project_name: cookie-{backend}
  project_type: {backend}
"""

# Work around bug: https://github.com/FFY00/trampolim/issues/4
ENV = {
    "TRAMPOLIM_VCS_VERSION": "0.1.0",
}


def make_cookie(session: nox.Session, backend: str) -> str:
    tmp_dir = session.create_tmp()
    session.cd(tmp_dir)

    with open("input.yml", "w") as f:
        f.write(JOB_FILE.format(backend=backend))

    session.run(
        "cookiecutter",
        "--no-input",
        str(DIR),
        "--config-file=input.yml",
    )
    session.cd(f"cookie-{backend}")
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
    return tmp_dir


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


@nox.session()
@nox.parametrize("backend", BACKENDS, ids=BACKENDS)
def tests(session, backend):
    session.install("cookiecutter")

    make_cookie(session, backend)

    session.install(".[test]", env=ENV)
    session.run("python", "-m", "pytest", "-ra")


@nox.session()
def tests_poetry(session):
    session.install("cookiecutter", "poetry")

    make_cookie(session, "poetry")

    session.run("poetry", "install")
    session.run("poetry", "run", "pytest")


@nox.session()
@nox.parametrize("backend", BACKENDS, ids=BACKENDS)
def dist(session, backend):
    session.install("cookiecutter", "build", "twine")

    make_cookie(session, backend)

    session.run("python", "-m", "build", env=ENV, silent=True)
    (sdist,) = Path("dist").glob("*.tar.gz")
    (wheel,) = Path("dist").glob("*.whl")

    if "0.1.0" not in str(wheel):
        session.error(f"{wheel} must be version 0.1.0")

    # Twine only supports metadata 2.1, trampoline produces metadata 2.2
    if backend != "trampolim":
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
        session.run("nox", "-s", *session.posargs, env=ENV)
    else:
        session.run("nox", env=ENV)
