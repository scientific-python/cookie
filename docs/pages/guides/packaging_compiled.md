---
layout: page
title: Compiled packaging
permalink: /guides/packaging-compiled/
nav_order: 6
parent: Topical Guides
---

{% include toc.html %}

# Packaging Compiled Projects

There are a variety of ways to package compiled projects. In the past, the only
way to do it was to use setuptools/distutils, which required using lots of
fragile internals - distutils was intended primarily to compile CPython, and
setuptools tried to stay away from changing the compile portions except as
required. Now, however, we have several very nice options for compiled packages!

The most exciting developments have been new native build backends:

- [scikit-build-core][]: Builds C/C++/Fortran using CMake.
- [meson-python][]: Builds C/C++/Fortran using Meson.
- [maturin][]: Builds Rust using Cargo. Written entirely in Rust!
- [enscons][]: Builds C/C++ using SCONs. (Aging now, but this was the first
  native backend!)

{: .note }

You should be familiar with [packing a pure Python
project]({% link pages/guides/packaging_compiled.md %}) - the metadata
configuration is the same.

There are also classic setuptools plugins:

- [scikit-build][]: Builds C/C++/Fortran using CMake.
- [setuptools-rust][]: Builds Rust using Cargo.

{: .important }

If you have a really complex build, the newer native build backends might not
support your use case yet, but if that's the case, ask - development is driven
by community needs. The older, more fragile setuptools based plugins are still a
bit more flexible if you really need that flexibility for a feature not yet
implemented in the native backends.

## pyproject.toml: build-system

{% rr PY001 %} Packages must have a `pyproject.toml` file {% rr PP001 %} that
selects the backend:

{% tabs %} {% tab skbc Scikit-build-core %}

```toml
[build-system]
requires = ["scikit-build-core"]
build-backend = "scikit_build_core.build"
```

{% endtab %} {% tab meson Meson-python %}

```toml
[build-system]
requires = ["meson-python"]
build-backend = "mesonpy"
```

{% endtab %} {% tab maturin Maturin %}

```toml
[build-system]
requires = ["maturin"]
build-backend = "maturin"
```

{% endtab %} {% endtabs %}

{% include pyproject.md %}

## Tool section in pyproject.toml

These tools all read the project table. They also have extra configuration
options in `tool.*` settings.

<!-- [[[cog
from cog_helpers import render_cookie
with render_cookie(backend="skbuild") as skbuild:
    skbuild_cmakelists_txt = skbuild.joinpath("CMakeLists.txt").read_text(encoding="utf-8").strip()
    skbuild_src_main_cpp = skbuild.joinpath("src/main.cpp").read_text(encoding="utf-8").strip()
with render_cookie(backend="mesonpy") as mesonpy:
    mesonpy_meson_build = mesonpy.joinpath("meson.build").read_text(encoding="utf-8").strip()
    mesonpy_src_main_cpp = mesonpy.joinpath("src/main.cpp").read_text(encoding="utf-8").strip()
with render_cookie(backend="maturin") as maturin:
    maturin_cargo_toml = maturin.joinpath("Cargo.toml").read_text(encoding="utf-8").strip()
    maturin_src_lib_rs = maturin.joinpath("src/lib.rs").read_text(encoding="utf-8").strip()
]]] -->
<!-- [[[end]]] -->

## Backend specific files

{% tabs %} {% tab skbc Scikit-build-core %}

Example `CMakeLists.txt` file:

<!-- prettier-ignore-start -->
<!-- [[[cog
print("```cmake")
print(skbuild_cmakelists_txt)
print("```")
]]] -->
```cmake
cmake_minimum_required(VERSION 3.15...3.26)
project(${SKBUILD_PROJECT_NAME} LANGUAGES CXX)

set(PYBIND11_FINDPYTHON ON)
find_package(pybind11 CONFIG REQUIRED)

pybind11_add_module(_core MODULE src/main.cpp)
install(TARGETS _core DESTINATION ${SKBUILD_PROJECT_NAME})
```
<!-- [[[end]]] -->
<!-- prettier-ignore-end -->

{% endtab %} {% tab meson Meson-python %}

Example `meson.build` file:

<!-- prettier-ignore-start -->
<!-- [[[cog
print("```meson")
print(mesonpy_meson_build)
print("```")
]]] -->
```meson
project(
  'package',
  'cpp',
  version: '0.1.0',
  license: 'BSD',
  meson_version: '>= 0.64.0',
  default_options: [
    'buildtype=debugoptimized',
    'cpp_std=c++11',
  ],
)
name = 'package'

py_mod = import('python')
py = py_mod.find_installation(pure: false)

pybind11_config = find_program('pybind11-config')
pybind11_config_ret = run_command(pybind11_config, ['--includes'], check: true)
pybind11 = declare_dependency(
    include_directories: [pybind11_config_ret.stdout().split('-I')[-1].strip()],
)

install_subdir('src' / name, install_dir: py.get_install_dir() / name, strip_directory: true)

py.extension_module('_core',
    'src/main.cpp',
    subdir: 'package',
    install: true,
    dependencies : [pybind11],
    link_language : 'cpp',
    override_options: [
        'cpp_rtti=true',
    ]
)
```
<!-- [[[end]]] -->
<!-- prettier-ignore-end -->

{% endtab %} {% tab maturin Maturin %}

<!-- prettier-ignore-start -->
<!-- [[[cog
print("```toml")
print(maturin_cargo_toml)
print("```")
]]] -->
```toml
[package]
name = "package"
version = "0.1.0"
edition = "2018"

[lib]
name = "_core"
# "cdylib" is necessary to produce a shared library for Python to import from.
crate-type = ["cdylib"]

[package.metadata.maturin]
name = "package._core"
python-packages = ["package"]
python-source = "src"

[dependencies]
rand = "0.8.3"

[dependencies.pyo3]
version = "0.18.1"
# "extension-module" tells pyo3 we want to build an extension module (skips linking against libpython.so)
# "abi3-py38" tells pyo3 (and maturin) to build using the stable ABI with minimum Python version 3.8
features = ["extension-module", "abi3-py38"]
```
<!-- [[[end]]] -->
<!-- prettier-ignore-end -->

{% endtab %} {% endtabs %}

## Example compiled file

{% tabs %} {% tab skbc Scikit-build-core %}

Example `src/main.cpp` file:

<!-- prettier-ignore-start -->
<!-- [[[cog
print("```cpp")
print(skbuild_src_main_cpp)
print("```")
]]] -->
```cpp
#include <pybind11/pybind11.h>

int add(int i, int j) { return i + j; }

namespace py = pybind11;

PYBIND11_MODULE(_core, m) {
  m.doc() = R"pbdoc(
      Pybind11 example plugin
      -----------------------
      .. currentmodule:: python_example
      .. autosummary::
         :toctree: _generate
         add
         subtract
  )pbdoc";

  m.def("add", &add, R"pbdoc(
      Add two numbers
      Some other explanation about the add function.
  )pbdoc");

  m.def(
      "subtract", [](int i, int j) { return i - j; }, R"pbdoc(
      Subtract two numbers
      Some other explanation about the subtract function.
  )pbdoc");
}
```
<!-- [[[end]]] -->
<!-- prettier-ignore-end -->

{% endtab %} {% tab meson Meson-python %}

Example `src/main.cpp` file:

<!-- prettier-ignore-start -->
<!-- [[[cog
print("```cpp")
print(mesonpy_src_main_cpp)
print("```")
]]] -->
```cpp
#include <pybind11/pybind11.h>

int add(int i, int j) { return i + j; }

namespace py = pybind11;

PYBIND11_MODULE(_core, m) {
  m.doc() = R"pbdoc(
      Pybind11 example plugin
      -----------------------
      .. currentmodule:: python_example
      .. autosummary::
         :toctree: _generate
         add
         subtract
  )pbdoc";

  m.def("add", &add, R"pbdoc(
      Add two numbers
      Some other explanation about the add function.
  )pbdoc");

  m.def(
      "subtract", [](int i, int j) { return i - j; }, R"pbdoc(
      Subtract two numbers
      Some other explanation about the subtract function.
  )pbdoc");
}
```
<!-- [[[end]]] -->
<!-- prettier-ignore-end -->

{% endtab %} {% tab maturin Maturin %}

<!-- prettier-ignore-start -->
<!-- [[[cog
print("```rs")
print(maturin_src_lib_rs)
print("```")
]]] -->
```rs
use pyo3::prelude::*;

#[pyfunction]
fn add(x: i64, y: i64) -> i64 {
    x + y
}

#[pyfunction]
fn subtract(x: i64, y: i64) -> i64 {
    x - y
}

/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[pymodule]
fn _core(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(add, m)?)?;
    m.add_function(wrap_pyfunction!(subtract, m)?)?;
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;

    Ok(())
}
```
<!-- [[[end]]] -->
<!-- prettier-ignore-end -->

{% endtab %} {% endtabs %}

## Package structure

The recommendation (followed above) is to have source code in `/src`, and the
Python package files in `/src/<package>`.

## Versioning

Check the documentation for the tools above to see what forms of dynamic
versioning the tool supports.

## Including/excluding files in the SDist

Each tool uses a different mechanism to include or remove files from the SDist,
though the defaults are reasonable.

## Distributing

Unlike pure Python, you'll need to build redistributable wheels for each
platform and supported Python version if you want to avoid compilation on the
user's system. See [the CI page on wheels][gha_wheels] for a suggested workflow.

<!-- prettier-ignore-start -->

[scikit-build-core]: https://scikit-build-core.readthedocs.io
[scikit-build]: https://scikit-build.readthedocs.io
[meson-python]: https://meson-python.readthedocs.io
[cmake]: https://cmake.org
[meson]: https://mesonbuild.com
[enscons]: https://pypi.org/project/enscons
[scons]: https://scons.org/
[setuptools-rust]: https://setuptools-rust.readthedocs.io/en/latest/
[maturin]: https://www.maturin.rs
[gha_wheels]: {% link pages/guides/gha_wheels.md %}

<!-- prettier-ignore-end -->

<script src="{% link assets/js/tabs.js %}"></script>
