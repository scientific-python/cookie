from __future__ import annotations

import {{ cookiecutter.project_name.replace("-", "_") }} as m


def test_version():
    assert m.__version__
