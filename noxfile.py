import nox
from pathlib import Path
import shutil

DIR = Path(__file__).parent.resolve()
BACKENDS = "setuptools", "pybind11", "flit", "poetry"


def make_cookie(session: nox.Session, backend: str) -> str:
    tmp_dir = session.create_tmp()
    session.cd(tmp_dir)

    session.run(
        "cookiecutter",
        "--no-input",
        str(DIR),
        "--config-file",
        str(DIR / f"tests/{backend}.yml"),
    )
    session.cd(f"cookie-{backend}")
    return tmp_dir


@nox.session()
@nox.parametrize("backend", BACKENDS, ids=BACKENDS)
def lint(session: nox.Session, backend: str) -> None:
    session.install("cookiecutter", "pre-commit")

    make_cookie(session, backend)

    session.run(
        "git", "clone", "--no-checkout", "--local", str(DIR), "../tmp_git", external=True
    )
    shutil.move("../tmp_git/.git", ".git")
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

    session.install(".[test]", env={"SETUPTOOLS_SCM_PRETEND_VERSION": "0.1.0"})
    session.run("python", "-m", "pytest", "-ra")


@nox.session()
def tests_poetry(session):
    session.install("cookiecutter", "poetry")

    make_cookie(session, "poetry")

    session.run("poetry", "install")
    session.run("poetry", "run", "pytest")
