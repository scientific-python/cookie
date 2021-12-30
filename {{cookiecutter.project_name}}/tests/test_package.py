from __future__ import annotations

import {{ cookiecutter.project_name.replace("-", "_") }} as m
{% if cookiecutter.project_type == "pybind11" -%}
import {{ cookiecutter.project_name.replace("-", "_") }}._core as cpp


def test_pybind11():
    assert cpp.add(1, 2) == 3
    assert cpp.subtract(1, 2) == -1
{% endif %}

def test_version():
    assert m.__version__
