import configparser
import inspect

from repo_review.testing import compute_check, toml_loads


def test_PP002_okay():
    toml = toml_loads("""
        [build-system]
        requires = ["setuptools"]
        build-backend = "setuptools.build_meta"
        """)
    assert compute_check("PP002", pyproject=toml).result


def test_PP002_not_list():
    toml = toml_loads("""
        [build-system]
        requires = "setuptools"
        build-backend = "setuptools.build_meta"
        """)
    assert not compute_check("PP002", pyproject=toml).result


def test_PP002_missing():
    toml = toml_loads("""
        [project]
        name = "hi"
        version = "1.0.0"
        """)
    assert not compute_check("PP002", pyproject=toml).result


def test_PP003_no_wheel():
    toml = toml_loads("""
        [build-system]
        requires = ["setuptools"]
        build-backend = "setuptools.build_meta"
        """)
    assert compute_check("PP003", pyproject=toml).result


def test_PP003_has_wheel():
    toml = toml_loads("""
        [build-system]
        requires = ["setuptools", "wheel"]
        build-backend = "setuptools.build_meta"
        """)
    assert not compute_check("PP003", pyproject=toml).result


def test_PP004_no_cap_pyproject():
    toml = toml_loads("""
       [project]
       requires-python = ">=3.10"
       """)

    assert compute_check("PP004", pyproject=toml, setupcfg=None).result


def test_PP004_cap_pyproject():
    toml = toml_loads("""
        [project]
        requires-python = ">=3.10, <4"
        """)

    assert compute_check("PP004", pyproject=toml, setupcfg=None).result is False


def test_PP004_cap_tilde_pyproject():
    toml = toml_loads("""
        [project]
        requires-python = "~=3.10"
        """)

    assert compute_check("PP004", pyproject=toml, setupcfg=None).result is False


def test_PP004_cap_caret_pyproject():
    toml = toml_loads("""
        [tool.poetry.dependencies]
        python = "^3.10"
       """)

    assert compute_check("PP004", pyproject=toml, setupcfg=None).result is False


def test_PP004_setup_cfg_no_cap():
    contents = inspect.cleandoc("""
        [options]
        python_requires = >=3.10
        """)
    config = configparser.ConfigParser()
    config.read_string(contents)

    assert compute_check("PP004", pyproject={}, setupcfg=config).result


def test_PP004_setup_cfg_cap():
    contents = inspect.cleandoc("""
        [options]
        python_requires = >=3.10,<4
        """)
    config = configparser.ConfigParser()
    config.read_string(contents)

    assert compute_check("PP004", pyproject={}, setupcfg=config).result is False


def test_PP004_setup_cfg_no_section():
    contents = inspect.cleandoc("""
        [other]
        python_requires = >=3.10
        """)
    config = configparser.ConfigParser()
    config.read_string(contents)

    assert not compute_check("PP004", pyproject={}, setupcfg=config).result


def test_PP004_setup_cfg_no_value():
    contents = inspect.cleandoc("""
        [options]
        other = >=3.10
        """)
    config = configparser.ConfigParser()
    config.read_string(contents)

    assert not compute_check("PP004", pyproject={}, setupcfg=config).result


def test_PP004_not_present():
    assert compute_check("PP004", pyproject={}, setupcfg=None).result is None


def test_PP005_no_license():
    toml = toml_loads("""
        [project]
        license.text = "MIT"
        classifiers = ["License :: OSI Approved :: MIT License"]
        """)

    assert compute_check("PP005", pyproject=toml).result is None


def test_PP005_pass():
    toml = toml_loads("""
        [project]
        license = "MIT"
        """)

    assert compute_check("PP005", pyproject=toml).result


def test_PP005_pass_empty_classifiers():
    toml = toml_loads("""
        [project]
        license = "MIT"
        classifiers = []
        """)

    assert compute_check("PP005", pyproject=toml).result


def test_PP005_pass_other_classifiers():
    toml = toml_loads("""
        [project]
        license = "MIT"
        classifiers = ["Something :: Else"]
        """)

    assert compute_check("PP005", pyproject=toml).result


def test_PP005_both():
    toml = toml_loads("""
        [project]
        license = "MIT"
        classifiers = ["License :: OSI Approved :: MIT License"]
        """)

    assert not compute_check("PP005", pyproject=toml).result


def test_PP302_okay_intstr():
    toml = toml_loads("""
        [tool.pytest.ini_options]
        minversion = "7"
        """)
    assert compute_check("PP302", pyproject=toml).result


def test_PP302_okay_verstr():
    toml = toml_loads("""
        [tool.pytest.ini_options]
        minversion = "7.0.2"
        """)
    assert compute_check("PP302", pyproject=toml).result


def test_PP302_okay_rawint():
    toml = toml_loads("""
        [tool.pytest.ini_options]
        minversion = 7
        """)
    assert compute_check("PP302", pyproject=toml).result


def test_PP302_okay_rawfloat():
    toml = toml_loads("""
        [tool.pytest.ini_options]
        minversion = 7.0
        """)
    assert compute_check("PP302", pyproject=toml).result


def test_PP302_missing():
    toml = toml_loads("""
        [tool.pytest]
        ini_options = {}
        """)
    assert not compute_check("PP302", pyproject=toml).result


def test_PP302_too_low():
    toml = toml_loads("""
        [tool.pytest.ini_options]
        minversion = "5"
        """)
    assert not compute_check("PP302", pyproject=toml).result


def test_PP308_list_okay():
    toml = toml_loads("""
        [tool.pytest.ini_options]
        addopts = ["-ra"]
        """)
    assert compute_check("PP308", pyproject=toml).result


def test_PP308_list_missing():
    toml = toml_loads("""
        [tool.pytest.ini_options]
        addopts = ["-otther"]
        """)
    assert not compute_check("PP308", pyproject=toml).result


def test_PP308_string_okay():
    toml = toml_loads("""
        [tool.pytest.ini_options]
        addopts = "--stuff -ra --morestuff"
        """)
    assert compute_check("PP308", pyproject=toml).result


def test_PP308_string_missing():
    toml = toml_loads("""
        [tool.pytest.ini_options]
        addopts = "--stuff --morestuff"
        """)
    assert not compute_check("PP308", pyproject=toml).result
