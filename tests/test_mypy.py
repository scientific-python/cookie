from repo_review.testing import compute_check, toml_loads


def test_my100_present():
    toml = toml_loads("""
        [tool.mypy]
        strict = true
        """)
    assert compute_check("MY100", pyproject=toml).result


def test_my100_pyrefly():
    toml = toml_loads("""
        [tool.pyrefly]
        project-includes = ["src"]
        """)
    assert compute_check("MY100", pyproject=toml).result


def test_my100_ty():
    toml = toml_loads("""
        [tool.ty.src]
        include = ["src"]
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


def test_my101_pyrefly_preset():
    toml = toml_loads("""
        [tool.pyrefly]
        preset = "strict"
        """)
    assert compute_check("MY101", pyproject=toml).result


def test_my101_pyrefly_no_preset():
    toml = toml_loads("""
        [tool.pyrefly]
        project-includes = ["src"]
        """)
    assert compute_check("MY101", pyproject=toml).result is False


def test_my101_ty_skipped():
    toml = toml_loads("""
        [tool.ty.src]
        include = ["src"]
        """)
    assert compute_check("MY101", pyproject=toml).result is None


def test_my10x_skipped_without_mypy():
    toml = toml_loads("""
        [tool.ty.src]
        include = ["src"]
        """)
    for name in ("MY102", "MY103", "MY104", "MY105", "MY106"):
        assert compute_check(name, pyproject=toml).result is None


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
