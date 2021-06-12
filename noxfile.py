import nox
from pathlib import Path

DIR = Path(__file__).parent.resolve()
BACKENDS = "setuptools", "pybind11", "poetry", "flit", "flit621", "trampolim"

JOB_FILE = """\
default_context:
  project_name: cookie-{backend}
  project_type: {backend}
"""

ENV = {"SETUPTOOLS_SCM_PRETEND_VERSION": "0.1.0"}


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
    return tmp_dir


@nox.session()
@nox.parametrize("backend", BACKENDS, ids=BACKENDS)
def lint(session: nox.Session, backend: str) -> None:
    session.install("cookiecutter", "pre-commit")

    make_cookie(session, backend)

    session.run(
        "git",
        "clone",
        "--no-checkout",
        "--local",
        str(DIR),
        "../tmp_git",
        external=True,
    )
    Path("../tmp_git/.git").rename(".git")
    session.run("git", "add", ".", external=True)

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

    session.run("python", "-m", "build", env=ENV)
    (sdist,) = Path("dist").glob("*.tar.gz")
    (wheel,) = Path("dist").glob("*.whl")

    # Twine only supports metadata 2.1, trampoline produces metadata 2.2
    if backend != "trampolim":
        session.run("twine", "check", str(sdist), str(wheel))

    dist = DIR / "dist"
    dist.mkdir(exist_ok=True)
    sdist.rename(dist / sdist.stem)
    wheel.rename(dist / wheel.stem)
