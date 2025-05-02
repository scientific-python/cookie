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
We will focus on GHA below.

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
    pull_request:
      paths:
        - .github/workflows/cd.yml
```

This will run on releases. If you use a develop branch, you could include
`pull_request: branches: [stable]`, since it changes rarely. GitHub actions also
[has a `workflow_dispatch` option][workflow_dispatch], which will allow you to
click a button in the GUI to trigger a build, which is perfect for testing
wheels before making a release; you can download them from the "artifacts". You
can even define variables that you can set in the GUI and access in the CI!
Finally, if you change the workflow itself in a PR, then rebuild the wheels too.

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
test-groups = ["test"]
test-command = "pytest {project}/tests"
build-frontend = "build[uv]"
# Optional
build-verbosity = 1
```

The build frontend is set to `build[uv]`, which is faster than the default build
backend; you just need uv installed, but that's easy to do. The `test-extras`
will cause the pip install to use the dependency-group(s) specified. The
`test-command` will use pytest to run your tests. You can also set the build
verbosity (`-v` in pip) if you want to.

## Making an SDist

You probably should not forget about making an SDist! A simple job, like before,
will work:

```yaml
make_sdist:
  name: Make SDist
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0 # Optional, use if you use setuptools_scm
        submodules: true # Optional, use if you have submodules

    - name: Build SDist
      run: pipx run build --sdist

    - uses: actions/upload-artifact@v4
      with:
        name: cibw-sdist
        path: dist/*.tar.gz
```

You can instead install build via pip and use `python -m build --sdist`. You can
also pin the version with `pipx run build==<version>`.

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
      os: [ubuntu-latest, windows-latest, macos-13, macos-14]

  steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0
        submodules: true

    - uses: astral-sh/setup-uv@v6

    - uses: pypa/cibuildwheel@v2.23

    - name: Upload wheels
      uses: actions/upload-artifact@v4
      with:
        name: cibw-wheels-${{ matrix.os }}
        path: wheelhouse/*.whl
```

{% endraw %}

There are several things to note here. First, one of the reasons this works is
because you followed the suggestions in the previous sections, and your package
builds nicely into a wheel without strange customizations (if you _really_ need
them, check out [`CIBW_BEFORE_BUILD`][] and [`CIBW_ENVIRONMENT`][]).

This lists all three OS's; if you do not support Windows, you can remove that
here. If you would rather make universal2 wheels for macOS, you can remove
either the Intel (`macos-13`) or Apple Silicon (`macos-14`) job and set
`CIBW_ARCHS_MACOS` to `"universal2"`. You can also set `CIBW_TEST_SKIP` to
`"*universal2:arm64"` if building from Intel to acknowledge you understand that
you can't test Apple Silicon from Intel. You can do this from the
`pyproject.toml` file instead if you want.

The build step is controlled almost exclusively through environment variables,
which makes it easier (usually) to setup in CI. The main variable needed here is
usually `CIBW_BUILD` to select the platforms you want to build for - see the
[docs here][cibw custom] for all the identifiers. Note that the ARM and other
alternative architectures need emulation, so are not shown here (adds one extra
step).

You can also select different base images (the default is `manylinux2014`). If
you want a different supported image, set `CIBW_MANYLINUX_X86_64_IMAGE`,
`CIBW_MANYLINUX_I686_IMAGE`, etc. If you always need a specific image, you can
set that in the `pyproject.toml` file instead.

You can skip specifying the `build[uv]` build-frontend option and pre-installing
`uv` on the runners, but it will be a slower.

## Publishing

{% tabs %} {% tab oidc Trusted Publishing %}

{% raw %}

```yaml
upload_all:
  needs: [build_wheels, make_sdist]
  environment: pypi
  permissions:
    id-token: write
    attestations: write
    contents: read

  runs-on: ubuntu-latest
  if: github.event_name == 'release' && github.event.action == 'published'
  steps:
    - uses: actions/download-artifact@v4
      with:
        pattern: cibw-*
        path: dist
        merge-multiple: true

    - name: Generate artifact attestations
      uses: actions/attest-build-provenance@v2
      with:
        subject-path: "dist/*"

    - uses: pypa/gh-action-pypi-publish@release/v1
```

{% endraw %}

When you make a GitHub release in the web UI, we publish to PyPI. You'll just
need to tell PyPI which org, repo, workflow, and set the `pypi` environment to
allow pushes from GitHub. If it's the first time you've published a package, go
to the [PyPI trusted publisher docs] for instructions on preparing PyPI to
accept your initial package publish.

We are also generating artifact attestations, which can allow users to verify
that the artifacts were built on your actions.

{% endtab %} {% tab token Token %}

{% raw %}

```yaml
upload_all:
  needs: [build_wheels, make_sdist]
  runs-on: ubuntu-latest
  if: github.event_name == 'release' && github.event.action == 'published'
  steps:
    - uses: actions/download-artifact@v4
      with:
        pattern: cibw-*
        path: dist
        merge-multiple: true

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
> GitHub Actions supports ARM on Linux and Windows as well. On Travis,
> `cibuildwheel` even has the ability to create rarer architectures like PowerPC
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
