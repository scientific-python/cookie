from __future__ import annotations

{%- if cookiecutter.project_type != "maturin" %}

import {{ cookiecutter.project_name.replace("-", "_") }}._core as m
{%- else %}

import {{ cookiecutter.project_name.replace("-", "_") }} as m
{%- endif %}


def test_add():
    assert m.add(2, 3) == 5


def test_subtract():
    assert m.subtract(7, 5) == 2
