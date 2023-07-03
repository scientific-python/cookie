"""
Nox runner for cookie & sp-repo-review.

sp-repo-review checks start with "rr-".
"""


from __future__ import annotations

import difflib
import json
import re
import shutil
import sys
import urllib.request
from pathlib import Path

import nox

nox.needs_version = ">=2022.1.7"
nox.options.sessions = ["rr_lint", "rr_tests", "rr_pylint", "readme"]

DIR = Path(__file__).parent.resolve()
with DIR.joinpath("cookiecutter.json").open() as f:
    BACKENDS = json.load(f)["backend"]

JOB_FILE = """\
default_context:
  project_name: cookie-{backend}
  backend: {backend}
"""


def make_copier(session: nox.Session, backend: str) -> None:
    package_dir = Path(f"copy-{backend}")
    if package_dir.exists():
        shutil.rmtree(package_dir)

    session.run(
        "copier",
        "copy",
        f"{DIR}",
        f"{package_dir}",
        "--defaults",
        "--UNSAFE",
        "--vcs-ref=HEAD",
        f"--data=project_name=cookie-{backend}",
        "--data=org=org",
        f"--data=backend={backend}",
        "--data=full_name=My Name",
        "--data=email=me@email.com",
        "--data=license=BSD",
    )

    init_git(session, package_dir)

    return package_dir


def make_cookie(session: nox.Session, backend: str) -> None:
    package_dir = Path(f"cookie-{backend}")
    if package_dir.exists():
        shutil.rmtree(package_dir)

    Path("input.yml").write_text(JOB_FILE.format(backend=backend), encoding="utf-8")

    session.run(
        "cookiecutter",
        "--no-input",
        f"{DIR}",
        "--config-file=input.yml",
    )

    init_git(session, package_dir)

    return package_dir


def make_cruft(session: nox.Session, backend: str) -> None:
    package_dir = Path(f"cruft-{backend}")
    if package_dir.exists():
        shutil.rmtree(package_dir)

    tmp_dir = Path("tmp_loc")
    tmp_dir.mkdir()

    session.cd(tmp_dir)
    Path("input.yml").write_text(
        JOB_FILE.format(backend=backend, pkg=package_dir), encoding="utf-8"
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
    session.run("git", "-C", f"{package_dir}", "tag", "v0.1.0", external=True)


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


@nox.session()
@nox.parametrize("backend", BACKENDS, ids=BACKENDS)
def lint(session: nox.Session, backend: str) -> None:
    session.install("cookiecutter", "pre-commit")

    tmp_dir = session.create_tmp()
    session.cd(tmp_dir)
    cookie = make_cookie(session, backend)
    session.chdir(cookie)

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

    tmp_dir = session.create_tmp()
    session.cd(tmp_dir)
    cookie = make_cookie(session, backend)
    session.chdir(cookie)

    session.run("pre-commit", "autoupdate")
    session.run("git", "diff", "--exit-code", external=True)


@nox.session()
@nox.parametrize("backend", BACKENDS, ids=BACKENDS)
def tests(session, backend):
    session.install("cookiecutter")

    tmp_dir = session.create_tmp()
    session.cd(tmp_dir)
    cookie = make_cookie(session, backend)
    session.chdir(cookie)

    session.install(".[test]")
    session.run("python", "-m", "pytest", "-ra")


@nox.session()
@nox.parametrize("backend", ("poetry", "pdm", "hatch"), ids=("poetry", "pdm", "hatch"))
def native(session, backend):
    session.install("cookiecutter", backend)

    tmp_dir = session.create_tmp()
    session.cd(tmp_dir)
    cookie = make_cookie(session, backend)
    session.chdir(cookie)

    if backend == "hatch":
        session.run(backend, "env", "create")
    else:
        session.run(backend, "install")

    session.run(backend, "run", "pytest")


@nox.session()
@nox.parametrize("backend", BACKENDS, ids=BACKENDS)
def dist(session, backend):
    session.install("cookiecutter", "build", "twine")

    tmp_dir = session.create_tmp()
    session.cd(tmp_dir)
    cookie = make_cookie(session, backend)
    session.chdir(cookie)

    session.run("python", "-m", "build", silent=True)
    (sdist,) = Path("dist").glob("*.tar.gz")
    (wheel,) = Path("dist").glob("*.whl")

    if "0.1.0" not in str(wheel):
        session.error(f"{wheel} must be version 0.1.0")

    session.run("twine", "check", f"{sdist}", f"{wheel}")

    dist = DIR / "dist"
    dist.mkdir(exist_ok=True)
    sdist.rename(dist / sdist.stem)
    wheel.rename(dist / wheel.stem)


@nox.session(name="nox")
@nox.parametrize("backend", BACKENDS, ids=BACKENDS)
def nox_session(session, backend):
    session.install("cookiecutter", "nox")

    tmp_dir = session.create_tmp()
    session.cd(tmp_dir)
    cookie = make_cookie(session, backend)
    session.chdir(cookie)

    if session.posargs:
        session.run("nox", "-s", *session.posargs)
    else:
        session.run("nox")


@nox.session()
def compare_copier(session):
    # Pydantic 2.0 breaks copier <= 8.0.0
    session.install(
        "cookiecutter", "copier", "copier-templates-extensions", "pydantic<2"
    )

    tmp_dir = session.create_tmp()
    session.cd(tmp_dir)

    for backend in BACKENDS:
        cookie = make_cookie(session, backend)
        copier = make_copier(session, backend)

        if diff_files(cookie, copier):
            session.log(f"{backend} passed")
        else:
            session.error(f"{backend} files are not the same!")


@nox.session()
def compare_cruft(session):
    session.install("cookiecutter", "cruft")

    tmp_dir = session.create_tmp()
    session.cd(tmp_dir)

    for backend in BACKENDS:
        cookie = make_cookie(session, backend)
        copier = make_cruft(session, backend)

        if diff_files(cookie, copier):
            session.log(f"{backend} passed")
        else:
            session.error(f"{backend} files are not the same!")


PC_VERS = re.compile(
    r"""\
^( *)- repo: (.*?)
 *  rev: (.*?)$""",
    re.MULTILINE,
)

PC_REPL_LINE = '''\
{2}- repo: {0}
{2}  rev: "{1}"'''


GHA_VERS = re.compile(r"[\s\-]+uses: (.*?)@([^\s]+)")


@nox.session(reuse_venv=True)
def pc_bump(session: nox.Session) -> None:
    """
    Bump the pre-commit versions.
    """
    session.install("lastversion")
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
                versions[proj] = session.run("lastversion", proj, silent=True).strip()
            new_version = versions[proj]

            if old_version.lstrip("v") == new_version:
                continue

            if old_version.startswith("v"):
                new_version = f"v{new_version}"

            before = PC_REPL_LINE.format(proj, old_version, space)
            after = PC_REPL_LINE.format(proj, new_version, space)

            session.log(f"Bump: {old_version} -> {new_version} ({page})")
            txt = txt.replace(before, after)

            page.write_text(txt)


@nox.session(venv_backend="none")
def gha_bump(session: nox.Session) -> None:
    """
    Bump the GitHub Actions.
    """
    pages = list(Path("docs/pages/guides").glob("gha_*.md"))
    pages.extend(Path("{{cookiecutter.project_name}}/.github/workflows").iterdir())
    pages.append(Path("docs/pages/guides/style.md"))
    full_txt = "\n".join(page.read_text() for page in pages)

    # This assumes there is a single version per action
    old_versions = {m[1]: m[2] for m in GHA_VERS.finditer(full_txt)}
    versions = {}

    for repo, old_version in old_versions.items():
        session.log(f"{repo}: {old_version}")
        if repo not in versions:
            response = urllib.request.urlopen(
                f"https://api.github.com/repos/{repo}/tags"
            )
            versions[repo] = json.loads(response.read())
        tags = [
            x["name"]
            for x in versions[repo]
            if x["name"].count(".") == old_version.count(".")
        ]
        if not tags:
            continue
        new_version = tags[0]
        if new_version != old_version:
            session.log(f"Convert {repo}: {old_version} -> {new_version}")
            for page in pages:
                txt = page.read_text()
                txt = txt.replace(
                    f"uses: {repo}@{old_version}", f"uses: {repo}@{new_version}"
                )
                page.write_text(txt)


# -- Repo review --


@nox.session
def readme(session: nox.Session) -> None:
    """
    Update the readme with cog. Pass --check to check instead.
    """

    args = session.posargs or ["-r"]

    session.install("-e.", "cogapp", "repo-review>=0.8")
    session.run("cog", "-P", *args, "README.md")


@nox.session(reuse_venv=True)
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
    Run PyLint.
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
    session.install("-e.[test,cli]")
    session.run("pytest", *session.posargs)


@nox.session(reuse_venv=True)
def rr_build(session: nox.Session) -> None:
    """
    Build an SDist and wheel for sp-repo-review.
    """

    build_p = DIR.joinpath("build")
    if build_p.exists():
        shutil.rmtree(build_p)

    session.install("build")
    session.run("python", "-m", "build")
