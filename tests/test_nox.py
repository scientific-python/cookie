import inspect

from repo_review.testing import compute_check

from sp_repo_review.checks.noxfile import Noxfile


def test_nox101():
    noxfile = inspect.cleandoc("""
        import nox

        nox.needs_version = ">=2025.10.14"

        @nox.session
        def tests(session):
            session.run("pytest", "tests")
    """)
    result = compute_check("NOX101", noxfile=Noxfile.from_str(noxfile))
    assert result.result


def test_nox101_invalid():
    noxfile = inspect.cleandoc("""
        import nox

        @nox.session
        def tests(session):
            session.run("pytest", "tests")
    """)
    result = compute_check("NOX101", noxfile=Noxfile.from_str(noxfile))
    assert result.result is False


def test_nox102():
    noxfile = inspect.cleandoc("""
        import nox

        nox.options.default_venv_backend = "uv|virtualenv"
        @nox.session
        def tests(session):
            session.run("pytest", "tests")
    """)
    result = compute_check("NOX102", noxfile=Noxfile.from_str(noxfile))
    assert result.result


def test_nox102_invalid():
    noxfile = inspect.cleandoc("""
        import nox

        @nox.session
        def tests(session):
            session.run("pytest", "tests")
    """)
    result = compute_check("NOX102", noxfile=Noxfile.from_str(noxfile))
    assert result.result is False


def test_nox103():
    noxfile = inspect.cleandoc("""
        import nox

        @nox.session
        def tests(session):
            session.run("pytest", "tests")
    """)
    result = compute_check("NOX103", noxfile=Noxfile.from_str(noxfile))
    assert result.result is True


def test_nox103_invalid():
    noxfile = inspect.cleandoc("""
        import nox

        nox.options.sessions = ["tests"]

        @nox.session
        def tests(session):
            session.run("pytest", "tests")
    """)
    result = compute_check("NOX103", noxfile=Noxfile.from_str(noxfile))
    assert result.result is False


def test_nox201():
    noxfile = inspect.cleandoc("""
        #!/usr/bin/env python

        # /// script
        # dependencies = ["nox"]
        # ///

        import nox
    """)
    result = compute_check("NOX201", noxfile=Noxfile.from_str(noxfile))
    assert result.result


def test_nox201_invalid():
    noxfile = inspect.cleandoc("""
        import nox
    """)
    result = compute_check("NOX201", noxfile=Noxfile.from_str(noxfile))
    assert result.result is False


def test_nox202():
    noxfile = inspect.cleandoc("""
        #!/usr/bin/env python

        import nox
    """)
    result = compute_check("NOX202", noxfile=Noxfile.from_str(noxfile))
    assert result.result


def test_nox202_invalid():
    noxfile = inspect.cleandoc("""
        import nox
    """)
    result = compute_check("NOX202", noxfile=Noxfile.from_str(noxfile))
    assert result.result is False


def tests_nox203():
    noxfile = inspect.cleandoc("""
        import nox

        @nox.session
        def tests(session):
            session.run("pytest", "tests")

        if __name__ == "__main__":
            nox.main()
    """)
    result = compute_check("NOX203", noxfile=Noxfile.from_str(noxfile))
    assert result.result


def tests_nox203_invalid():
    noxfile = inspect.cleandoc("""
        import nox

        @nox.session
        def tests(session):
            session.run("pytest", "tests")
    """)
    result = compute_check("NOX203", noxfile=Noxfile.from_str(noxfile))
    assert result.result is False
