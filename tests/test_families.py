from sp_repo_review.families import get_families


def test_backend():
    pyproject = {
        "build-system": {
            "requires": ["setuptools"],
            "build-backend": "setuptools.build_meta",
        },
    }
    families = get_families(pyproject)
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
    families = get_families(pyproject)
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
    families = get_families(pyproject)
    assert families["general"].get("description") == (
        "- Detected build backend: `MISSING`\n"
        "- Detected license(s): MIT License, BSD License"
    )
