{% set project_slug = cookiecutter.project_name | lower | replace("-", "_") | replace(".", "_") %}
{% set _ = cookiecutter.__setattr__('project_slug', project_slug) %}
