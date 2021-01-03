import {{ cookiecutter.project_name.replace("-", "_") }}


def test_version():
    assert {{ cookiecutter.project_name.replace("-", "_")}}.__version__
