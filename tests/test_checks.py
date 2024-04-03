from sp_repo_review._compat import tomllib
from sp_repo_review.checks import pyproject


def test_PP002_okay():
    toml = tomllib.loads("""
        [build-system]
        requires = ["setuptools"]
        build-backend = "setuptools.build_meta"
        """)
    assert pyproject.PP002.check(toml)


def test_PP002_not_list():
    toml = tomllib.loads("""
        [build-system]
        requires = "setuptools"
        build-backend = "setuptools.build_meta"
        """)
    assert not pyproject.PP002.check(toml)


def test_PP002_missing():
    toml = tomllib.loads("""
        [project]
        name = "hi"
        version = "1.0.0"
        """)
    assert not pyproject.PP002.check(toml)


def test_PP003_no_wheel():
    toml = tomllib.loads("""
        [build-system]
        requires = ["setuptools"]
        build-backend = "setuptools.build_meta"
        """)
    assert pyproject.PP003.check(toml)


def test_PP003_has_wheel():
    toml = tomllib.loads("""
        [build-system]
        requires = ["setuptools", "wheel"]
        build-backend = "setuptools.build_meta"
        """)
    assert not pyproject.PP003.check(toml)


def test_PP302_okay_intstr():
    toml = tomllib.loads("""
        [tool.pytest.ini_options]
        minversion = "7"
        """)
    assert pyproject.PP302.check(toml)


def test_PP302_okay_verstr():
    toml = tomllib.loads("""
        [tool.pytest.ini_options]
        minversion = "7.0.2"
        """)
    assert pyproject.PP302.check(toml)


def test_PP302_okay_rawint():
    toml = tomllib.loads("""
        [tool.pytest.ini_options]
        minversion = 7
        """)
    assert pyproject.PP302.check(toml)


def test_PP302_okay_rawfloat():
    toml = tomllib.loads("""
        [tool.pytest.ini_options]
        minversion = 7.0
        """)
    assert pyproject.PP302.check(toml)


def test_PP302_missing():
    toml = tomllib.loads("""
        [tool.pytest]
        ini_options = {}
        """)
    assert not pyproject.PP302.check(toml)


def test_PP302_too_low():
    toml = tomllib.loads("""
        [tool.pytest.ini_options]
        minversion = "5"
        """)
    assert not pyproject.PP302.check(toml)
