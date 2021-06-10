import nox
from pathlib import Path
import shutil

DIR = Path(__file__).parent.resolve()
BACKENDS = "setuptools", "pybind11", "flit", "poetry"


@nox.session()
@nox.parametrize("backend", BACKENDS, ids=BACKENDS)
def lint(session, backend):
    session.install("cookiecutter", "pre-commit")

    tmp_dir = session.create_tmp()
    session.cd(tmp_dir)
    session.run(
        "git", "clone", "--no-checkout", "--local", str(DIR), "tmp_git", external=True
    )
    session.run(
        "cookiecutter",
        "--no-input",
        str(DIR),
        "--config-file",
        str(DIR / f"tests/{backend}.yml"),
    )

    session.cd(f"cookie-{backend}")
    shutil.move("../tmp_git/.git", ".git")
    session.run("git", "add", ".", external=True)

    session.run(
        "pre-commit",
        "run",
        "--all-files",
        "--hook-stage=manual",
        "--show-diff-on-failure",
    )
