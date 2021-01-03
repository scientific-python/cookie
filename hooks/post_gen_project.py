from pathlib import Path

module_name = "{{ cookiecutter.project_name }}"

module_underscore_name = module_name.replace("-", "_")
module_dash_name = module_name.replace("_", "-")

if module_name != module_underscore_name:
    Path(f"src/{module_name}").rename(f"src/{module_underscore_name}")
