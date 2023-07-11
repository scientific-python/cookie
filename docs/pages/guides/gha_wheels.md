---
layout: page
title: "GHA: Binary wheels"
permalink: /guides/gha-wheels/
nav_order: 12
parent: Topical Guides
custom_title: GitHub Actions for Binary Wheels
---

{% include toc.html %}

# GitHub Actions: Binary wheels

Building binary wheels is a bit more involved, but can still be done effectively
with GHA. This document will introduce [cibuildwheel][] for use in your project.
The benefits of cibuildwheel are a larger user base, fast fixes from CI and pip,
works on all major CI vendors (no lock-in), and covers cases we were not able to
cover (like ARM). We will focus on GHA below.

## Header

Wheel building should only happen rarely, so you will want to limit it to
releases, and maybe a rarely moving branch or other special tag (such as
`stable` if you mostly update some other branch. You may occasionally want to
trigger wheels manually.

```yaml
name: Wheels

on:
  workflow_dispatch:
  release:
    types:
      - published
```

This will run on releases. If you use a develop branch, you could include
`pull_request: branches: [stable]`, since it changes rarely. GitHub actions also
[has a `workflow_dispatch` option][workflow_dispatch], which will allow you to
click a button in the GUI to trigger a build, which is perfect for testing
wheels before making a release; you can download them from "artifacts". You can
even define variables that you can set in the GUI and access in the CI!

<!-- prettier-ignore-start -->
[workflow_dispatch]: https://github.blog/changelog/2020-07-06-github-actions-manual-triggers-with-workflow_dispatch/

### Useful suggestion:
{: .no_toc }
<!-- prettier-ignore-end -->

Since these variables will be used by all jobs, you could make them available in
your `pyproject.toml` file, so they can be used everywhere (even locally for
Linux and Windows):

```toml
[tool.cibuildwheel]
test-extras = "test"
test-command = "pytest {project}/tests"
# Optional
build-verbosity = 1

# Optional: support Universal2 for Apple Silicon with these two lines:
[tool.cibuildwheel.macos]
archs = ["auto", "universal2"]
test-skip = ["*universal2:arm64"]
```

The `test-extras` will cause the pip install to use `[test]`. The `test-command`
will use pytest to run your tests. You can also set the build verbosity (`-v` in
pip) if you want to. If you support Apple Silicon, you can add the final two
lines, the first of which enables the `universal2` wheel, which has both Intel
and AS architectures in it, and the second explicitly skips testing the AS part
of the wheel, since it can't be tested on Intel. If you use CMake instead of
pure setuptools, you will likely need further customizations for AS
cross-compiling. Only Python 3.8+ supports Apple Silicon.

## Making an SDist

You probably should not forget about making an SDist! A simple job, like before,
will work:

```yaml
make_sdist:
  name: Make SDist
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v3
      with:
        fetch-depth: 0 # Optional, use if you use setuptools_scm
        submodules: true # Optional, use if you have submodules

    - name: Build SDist
      run: pipx run build --sdist

    - uses: actions/upload-artifact@v3
      with:
        path: dist/*.tar.gz
```

You can instead install build via pip and use `python -m build --sdist`. You can
also pin the version with `pipx run --spec build==... build`.

## The core job (3 main OS's)

The core of the work is down here:

{% raw %}

```yaml
build_wheels:
  name: Wheel on ${{ matrix.os }}
  runs-on: ${{ matrix.os }}
  strategy:
    fail-fast: false
    matrix:
      os: [ubuntu-20.04, windows-2019, macos-10.15]

  steps:
    - uses: actions/checkout@v3
      with:
        fetch-depth: 0
        submodules: true

    - uses: pypa/cibuildwheel@v2.14.0

    - name: Upload wheels
      uses: actions/upload-artifact@v3
      with:
        path: wheelhouse/*.whl
```

{% endraw %}

There are several things to note here. First, one of the reasons this works is
because you followed the suggestions in the previous sections, and your package
builds nicely into a wheel without strange customizations (if you _really_ need
them, check out [`CIBW_BEFORE_BUILD`][] and [`CIBW_ENVIRONMENT`][]).

This lists all three OS's; if you do not support Windows, you can remove that
here.

The build step is controlled almost exclusively through environment variables,
which makes it easier (usually) to setup in CI. The main variable needed here is
usually `CIBW_BUILD` to select the platforms you want to build for - see the
[docs here][cibw custom] for all the identifiers. Note that the ARM and other
alternative architectures need emulation, so are not shown here (adds one extra
step).

You can also select different base images (the _default_ is manylinux2010). If
you want manylinux1, just do:

```yaml
env:
  CIBW_MANYLINUX_X86_64_IMAGE: manylinux1
  CIBW_MANYLINUX_I686_IMAGE: manylinux1
```

You can even put any docker image here, as needed by the project. Note that
manylinux1 was discontinued on Jan 1, 2022, and updates will cease whenever they
break. If you always need a specific image, you can set that in the
`pyproject.toml` file instead.

## Publishing

{% tabs %} {% tab oidc Trusted Publishing %}

{% raw %}

```yaml
upload_all:
  needs: [build_wheels, make_sdist]
  environment: pypi
  permissions:
    id-token: write
  runs-on: ubuntu-latest
  if: github.event_name == 'release' && github.event.action == 'published'
  steps:
    - uses: actions/download-artifact@v3
      with:
        name: artifact
        path: dist

    - uses: pypa/gh-action-pypi-publish@release/v1
```

{% endraw %}

When you make a GitHub release in the web UI, we publish to PyPI. You'll just
need to tell PyPI which org, repo, workflow, and set the `pypi` environment to
allow pushes from GitHub. If it's the first time you've published a package, go
to the [PyPI trusted publisher docs] for instructions on preparing PyPI to
accept your initial package publish.

{% endtab %} {% tab token Token %}

{% raw %}

```yaml
upload_all:
  needs: [build_wheels, make_sdist]
  runs-on: ubuntu-latest
  if: github.event_name == 'release' && github.event.action == 'published'
  steps:
    - uses: actions/download-artifact@v3
      with:
        name: artifact
        path: dist

    - uses: pypa/gh-action-pypi-publish@release/v1
      with:
        password: ${{ secrets.pypi_password }}
```

{% endraw %}

When you make a GitHub release in the web UI, we publish to PyPI. You'll need to
go to PyPI, generate a token for your user, and put it into `pypi_password` on
your repo's secrets page. Once you have a project, you should delete your
user-scoped token and generate a new project-scoped token.

{% endtab %} {% endtabs %}

If you have multiple jobs, you will want to collect your artifacts from above.
If you only have one job, you can combine this into a single job like we did for
pure Python wheels, using dist instead of wheelhouse. If you upload from
multiple places, you can set `skip_existing` (but generally it's better to not
try to upload the same file from two places - you can trick Travis into avoiding
the sdist, for example).

{: .note-title }

> Other architectures
>
> On Travis, `cibuildwheel` even has the ability to create ARM and PowerPC
> builds natively. IBM Z builds are also available but in beta. However, due to
> Travis CI's recent dramatic reduction on open source support, emulating these
> architectures on GHA or Azure is probably better. Maybe look into Cirrus CI,
> which has some harder-to-find architectures.

<!-- prettier-ignore-start -->

[`cibw_before_build`]: https://cibuildwheel.readthedocs.io/en/stable/options/#before-build
[`cibw_environment`]: https://cibuildwheel.readthedocs.io/en/stable/options/#environment
[cibw custom]: https://cibuildwheel.readthedocs.io/en/stable/options/#build-skip
[cibuildwheel]: https://cibuildwheel.readthedocs.io/en/stable/
[pypi trusted publisher docs]: https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/

<!-- prettier-ignore-end -->

<script src="{% link assets/js/tabs.js %}"></script>
