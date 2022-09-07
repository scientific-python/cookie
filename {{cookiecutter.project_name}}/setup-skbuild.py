#!/usr/bin/env python
# Copyright (c) {{ cookiecutter.year }}, {{ cookiecutter.full_name }}
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or {{ cookiecutter.url }} for details.

from __future__ import annotations

from setuptools import find_packages
from skbuild import setup

setup(
    name="{{ cookiecutter.project_name.replace("-","_") }}",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    cmake_install_dir="src/{{ cookiecutter.project_name.replace("-", "_") }}",
    package_data={"{{ cookiecutter.project_name.replace("-", "_") }}":"py.typed"},
)
