from pathlib import Path

project_name = "{{ cookiecutter.project_name }}"
project_type = "{{ cookiecutter.project_type }}"
project_types = {"setuptools", "pybind11", "skbuild", "mesonpy", "poetry", "flit", "trampolim", "whey", "pdm", "maturin", "hatch", "setuptools621"}
other_project_types = project_types - {project_type}

files = (p for p in Path(".").rglob("*") if p.is_file() and "-" in p.stem)

for f in files:
    base, current = f.stem.rsplit("-", 1)
    currents = set(current.split(","))
    if project_type in currents:
        # with_stem requires python 3.9
        f.replace(f.with_name(f"{base}{f.suffix}"))
    elif currents & other_project_types:
        f.unlink()

files = (p for p in Path(".").rglob("*") if p.is_file() and "^" in p.stem)

for f in files:
    base, current = f.stem.rsplit("^", 1)
    currents = set(current.split(","))
    if project_type in currents:
        f.unlink()
    else:
        # with_stem requires python 3.9
        f.replace(f.with_name(f"{base}{f.suffix}"))
