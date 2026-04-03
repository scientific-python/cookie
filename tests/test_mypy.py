from repo_review.testing import compute_check, toml_loads


def test_my100_present():
    toml = toml_loads("""
        [tool.mypy]
        strict = true
        """)
    assert compute_check("MY100", pyproject=toml).result


def test_my100_missing():
    assert not compute_check("MY100", pyproject={}).result


def test_my101_present_bool():
    toml = toml_loads("""
        [tool.mypy]
        strict = false
        """)
    assert compute_check("MY101", pyproject=toml).result


def test_my101_missing():
    toml = toml_loads("""
        [tool.mypy]
        warn_unreachable = true
        """)
    assert not compute_check("MY101", pyproject=toml).result


def test_my102_pass_without_show_error_codes():
    toml = toml_loads("""
        [tool.mypy]
        strict = true
        """)
    assert compute_check("MY102", pyproject=toml).result


def test_my102_fail_with_show_error_codes():
    toml = toml_loads("""
        [tool.mypy]
        show_error_codes = true
        """)
    assert not compute_check("MY102", pyproject=toml).result


def test_my103_present():
    toml = toml_loads("""
        [tool.mypy]
        warn_unreachable = true
        """)
    assert compute_check("MY103", pyproject=toml).result


def test_my103_missing():
    toml = toml_loads("""
        [tool.mypy]
        strict = true
        """)
    assert not compute_check("MY103", pyproject=toml).result


def test_my104_present():
    toml = toml_loads("""
        [tool.mypy]
        enable_error_code = ["ignore-without-code", "redundant-expr", "truthy-bool"]
        """)
    assert compute_check("MY104", pyproject=toml).result


def test_my104_missing():
    toml = toml_loads("""
        [tool.mypy]
        enable_error_code = ["redundant-expr", "truthy-bool"]
        """)
    assert not compute_check("MY104", pyproject=toml).result


def test_my105_present():
    toml = toml_loads("""
        [tool.mypy]
        enable_error_code = ["ignore-without-code", "redundant-expr", "truthy-bool"]
        """)
    assert compute_check("MY105", pyproject=toml).result


def test_my105_missing():
    toml = toml_loads("""
        [tool.mypy]
        enable_error_code = ["ignore-without-code", "truthy-bool"]
        """)
    assert not compute_check("MY105", pyproject=toml).result


def test_my106_present():
    toml = toml_loads("""
        [tool.mypy]
        enable_error_code = ["ignore-without-code", "redundant-expr", "truthy-bool"]
        """)
    assert compute_check("MY106", pyproject=toml).result


def test_my106_missing():
    toml = toml_loads("""
        [tool.mypy]
        enable_error_code = ["ignore-without-code", "redundant-expr"]
        """)
    assert not compute_check("MY106", pyproject=toml).result
