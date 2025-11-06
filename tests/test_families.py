from sp_repo_review.families import get_families


def test_backend():
    pyproject = {
        "build-system": {
            "requires": ["setuptools"],
            "build-backend": "setuptools.build_meta",
        },
    }
    families = get_families(pyproject, {})
    assert families["general"].get("description") == (
        "- Detected build backend: `setuptools.build_meta`"
    )


def test_spdx_license():
    pyproject = {
        "project": {
            "license": "MIT",
            "classifiers": [
                "License :: OSI Approved :: MIT License",
                "License :: OSI Approved :: BSD License",
            ],
        },
    }
    families = get_families(pyproject, {})
    assert families["general"].get("description") == (
        "- Detected build backend: `MISSING`\n- SPDX license expression: `MIT`"
    )


def test_classic_license():
    pyproject = {
        "project": {
            "license": {"text": "Free-form"},
            "classifiers": [
                "License :: OSI Approved :: MIT License",
                "License :: OSI Approved :: BSD License",
            ],
        },
    }
    families = get_families(pyproject, {})
    assert families["general"].get("description") == (
        "- Detected build backend: `MISSING`\n"
        "- Detected license(s): MIT License, BSD License"
    )


def test_python_requires():
    pyproject = {
        "project": {"requires-python": ">=3.13"},
    }
    families = get_families(pyproject, {})
    assert families["general"].get("description") == (
        "- Detected build backend: `MISSING`\n- Python requires: `>=3.13`"
    )


ALL_RULES = [
    "ARG",
    "B",
    "C4",
    "DTZ",
    "EM",
    "EXE",
    "FA",
    "FURB",
    "G",
    "I",
    "ICN",
    "NPY",
    "PD",
    "PERF",
    "PGH",
    "PIE",
    "PL",
    "PT",
    "PTH",
    "PYI",
    "RET",
    "RUF",
    "SIM",
    "SLOT",
    "T20",
    "TC",
    "UP",
    "YTT",
]


def test_ruff_all_rules_selected():
    """Test when all recommended rules are selected."""
    ruff = {"lint": {"select": ALL_RULES}}
    families = get_families({}, ruff)
    assert families["ruff"].get("description") == "All mentioned rules selected"


def test_ruff_all_keyword():
    """Test when 'ALL' keyword is used."""
    ruff = {"lint": {"select": ["ALL"]}}
    families = get_families({}, ruff)
    assert families["ruff"].get("description") == "All mentioned rules selected"


def test_ruff_missing_rules():
    """Test when some recommended rules are missing."""
    ruff = {"lint": {"select": ["B", "I", "UP"]}}
    families = get_families({}, ruff)
    description = families["ruff"].get("description", "")
    assert description.startswith("Rules mentioned in guide but not here:")
    # Check that some missing rules are mentioned
    assert "ARG" in description or "C4" in description or "DTZ" in description


def test_ruff_extend_select():
    """Test with extend-select instead of select."""
    ruff = {"lint": {"extend-select": ["B", "I", "UP", "RUF"]}}
    families = get_families({}, ruff)
    description = families["ruff"].get("description", "")
    assert description.startswith("Rules mentioned in guide but not here:")
    # Verify that some rules are listed as missing
    assert "ARG" in description or "C4" in description


def test_ruff_root_level_select():
    """Test with select at root level (not under lint)."""
    ruff = {"select": ALL_RULES}
    families = get_families({}, ruff)
    assert families["ruff"].get("description") == "All mentioned rules selected"


def test_ruff_empty_config():
    """Test with empty ruff config."""
    ruff: dict[str, object] = {}
    families = get_families({}, ruff)
    assert families["ruff"].get("description") == ""


def test_ruff_no_select():
    """Test ruff config without select or extend-select."""
    ruff = {"lint": {"ignore": ["E501"]}}
    families = get_families({}, ruff)
    assert families["ruff"].get("description") == ""
