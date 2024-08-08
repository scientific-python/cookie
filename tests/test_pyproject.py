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
