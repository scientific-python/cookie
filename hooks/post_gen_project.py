from pathlib import Path

project_name = "{{ cookiecutter.project_name }}"
project_type = "{{ cookiecutter.project_type }}"
project_types = {"setuptools", "pybind11", "poetry", "flit", "flit621", "trampolim"}
other_project_types = project_types - {project_type}

project_underscore_name = project_name.replace("-", "_")
project_dash_name = project_name.replace("_", "-")

src = Path("src")

if project_name != project_underscore_name:
    (src / project_name).rename(src / project_underscore_name)

files = [p for p in Path(".").rglob("*") if p.is_file() and "-" in p.stem]

for f in files:
    base, current = f.stem.rsplit("-", 1)
    currents = set(current.split(","))
    if project_type in currents:
        # with_stem requires python 3.9
        f.replace(f.with_name(f"{base}{f.suffix}"))
    elif currents & other_project_types:
        f.unlink()

# Hackaround lack of "src/" support in trampolim - remove when proper support
# is added (and maybe after editable support is added?)
# Also remove if clause in .pre-commit-config.yaml
if project_type == "trampolim":
    for f in Path("src").iterdir():
        f.rename(f.stem)
