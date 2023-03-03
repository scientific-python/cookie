from cookiecutter.utils import simple_filter


@simple_filter
def normalize(v: str) -> str:
    return v.lower().replace("-", "_").replace(".", "_")
