---
layout: page
title: "GHA: Pure Python wheels"
permalink: /guides/gha-pure/
nav_order: 11
parent: Topical Guides
custom_title: GitHub Actions for pure Python wheels
---

{% include toc.html %}

# GitHub Actions: Pure Python wheels

We will cover binary wheels [on the next page][], but if you do not have a
compiled extension, this is called a universal (pure Python) package, and the
procedure to make a "built" wheel is simple. At the end of this page, there is a
recipe that can often be used exactly for pure Python wheels (if the previous
recommendations were followed).

{: .note }

> Why make a wheel when there is nothing to compile? There are a multitude of
> reasons that a wheel is better than only providing an sdist:
>
> - Wheels do not run `setup.py`, but simply install files into locations
>   - Lower install requirements - users don't need your setup tools
>   - Faster installs
>   - Safer installs - no arbitrary code execution
>   - Highly consistent installs
> - Wheels pre-compile bytecode when they install
>   - Initial import is not slower than subsequent import
>   - Less chance of a permission issue
> - You can look in the `.whl` (it's a `.zip`, really) and see where everything
>   is going to go

[on the next page]: {% link pages/guides/gha_wheels.md %}

## Job setup

```yaml
name: CD

on:
  workflow_dispatch:
  release:
    types:
      - published

jobs:
```

This will run when you manually trigger a build ([`workflow_dispatch`][]), or
when you publish a release. Later, we will make sure that the actual publish
step requires the event to be a publish event, so that manual triggers (and
branches/PRs, if those are enabled).

If you want tags instead of releases, you can add the `on: push: tags: "v*"` key
instead of the releases - however, _please_ remember to make a GitHub release of
your tag! It shows up in the GUI and it notifies anyone watching
releases(-only). You will also need to change the event filter below.

You can merge the CI job and the CD job if you want. To do that, preferably with
the name "CI/CD", you can just combine the two `on` dicts.

## Distribution: Pure Python wheels

{% raw %}

```yaml
dist:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v3
      with:
        fetch-depth: 0

    - name: Build SDist and wheel
      run: pipx run build

    - uses: actions/upload-artifact@v3
      with:
        path: dist/*

    - name: Check metadata
      run: pipx run twine check dist/*
```

{% endraw %}

We use [PyPA-Build](https://pypa-build.readthedocs.io/en/latest/), a new build
tool designed to make building wheels and SDists easy. It run a [PEP 517][]
backend and can get [PEP 518][] requirements even for making SDists.

By default this will make an SDist and a wheel from the package in the current
directory, and they will be placed in `./dist`. You can only build SDist (`-s`),
only build wheel (`-w`), change the output folder (`-o <dir>`) or give a
different input folder if you want.

You could use the setup-python action, install `build` and `twine` with `pip`,
and then use `python -m build` or `pyproject-build`, but it's better to use
`pipx` to install and run python applications. Pipx is provided by default by
GitHub Actions (in fact, they use it to setup other applications).

We upload the artifact just to make it available via the GitHub PR/Checks API.
You can download a file to test locally if you want without making a release.

We also add an optional check using twine for the metadata (it will be tested
later in the upload action for the release job, as well).

{: .highlight-title }

> All-in-one action
>
> There is an
> [all-in-one action](https://github.com/hynek/build-and-inspect-python-package)
> that does all the work for you for a pure Python package, including extra
> pre-upload checks & nice GitHub summaries.
>
> ```yaml
> steps:
>   - uses: actions/checkout@v3
>   - uses: hynek/build-and-inspect-python-package@v1
> ```
>
> The artifact it produces is named `Packages`, so that's what you need to use
> later to publish.

And then, you need a release job:

{% tabs %} {% tab oidc Trusted Publishing %}

{% raw %}

```yaml
publish:
  needs: [dist]
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
publish:
  needs: [dist]
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

{% details Complete recipe %}

This can be used on almost any package with a standard
`.github/workflows/cd.yml` recipe. This works because `pyproject.toml` describes
exactly how to build your package, hence all packages build exactly via the same
interface:

{% tabbodies %} {% tab oidc Trusted Publishing %}

{% raw %}

```yaml
name: CD

on:
  workflow_dispatch:
  push:
    branches:
      - main
  release:
    types:
      - published

jobs:
  dist:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - uses: hynek/build-and-inspect-python-package@v1

  publish:
    needs: [dist]
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

{% endtab %} {% tab token Token %}

{% raw %}

```yaml
name: CD

on:
  workflow_dispatch:
  push:
    branches:
      - main
  release:
    types:
      - published

jobs:
  dist:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - uses: hynek/build-and-inspect-python-package@v1

  publish:
    needs: [dist]
    runs-on: ubuntu-latest
    if: github.event_name == 'release' && github.event.action == 'published'

    steps:
      - uses: actions/download-artifact@v3
        with:
          name: Packages
          path: dist

      - uses: pypa/gh-action-pypi-publish@release/v1
        with:
          password: ${{ secrets.pypi_password }}
```

{% endraw %}

{% endtab %} {% endtabbodies %}

{% enddetails %}

<!-- prettier-ignore-start -->

[pep 517]: https://www.python.org/dev/peps/pep-0517/
[pep 518]: https://www.python.org/dev/peps/pep-0518/
[pypi trusted publisher docs]: https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/
[`workflow_dispatch`]: https://github.blog/changelog/2020-07-06-github-actions-manual-triggers-with-workflow_dispatch/


<!-- prettier-ignore-end -->

<script src="{% link assets/js/tabs.js %}"></script>
