---
layout: page
title: Simple packaging
permalink: /guides/packaging-simple/
nav_order: 5
parent: Topical Guides
---

{% include toc.html %}

# Simple packaging

Python packages can now use a modern build system instead of the classic but
verbose setuptools and `setup.py`. The one you select doesn't really matter that
much; they all use a [standard configuration language][metadata] introduced in
[PEP 621][]. The PyPA's Flit is a great option. [scikit-build-core][] and
[meson-python][] are being developed to support this sort of configuration,
enabling binary extension packages to benefit too. These [PEP 621][] tools
currently include [Hatch][], [PDM][], [Flit][], [Trampolim][], [Whey][], and
[Setuptools][]. [Poetry][] will eventually gain support in 2.0.

{: .note-title }

> Classic files
>
> These systems do not use or require `setup.py`, `setup.cfg`, or `MANIFEST.in`.
> Those are for setuptools. Unless you are using setuptools, of course, which
> still uses `MANIFEST.in`. You can convert the old files using
> `pipx run hatch new --init` or with
> [ini2toml](https://ini2toml.readthedocs.io/en/latest/).

{: .highlight-title }

> Selecting a backend
>
> Backends handle metadata the same way, so the choice comes down to how you
> specify what files go into an SDist and extra features, like getting a version
> from VCS. If you don't have an existing preference, hatchling is an excellent
> choice, balancing speed, configurability, and extendability.

## pyproject.toml: build-system

{% rr PY001 %} Packages must have a `pyproject.toml` file {% rr PP001 %} that
selects the backend:

{% tabs %} {% tab hatch Hatchling %}

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

{% endtab %} {% tab flit Flit-core %}

```toml
[build-system]
requires = ["flit_core>=3.3"]
build-backend = "flit_core.buildapi"
```

{% endtab %} {% tab pdm PDM-backend %}

```toml
[build-system]
requires = ["pdm-backend"]
build-backend = "pdm.backend"
```

{% endtab %} {% tab setuptools Setuptools %}

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"
```

{% endtab %} {% endtabs %}

{% include pyproject.md %}

## Package structure

All packages _should_ have a `src` folder, with the package code residing inside
it, such as `src/<package>/`. This may seem like extra hassle; after all, you
can type "`python`" in the main directory and avoid installing it if you don't
have a `src` folder! However, this is a bad practice, and it causes several
common bugs, such as running `pytest` and getting the local version instead of
the installed version - this obviously tends to break if you build parts of the
library or if you access package metadata.

This sadly is not part of the standard metadata in `[project]`, so it depends on
what backend you you use. Hatchling, Flit, PDM, and setuptools use automatic
detection, while Trampolim and whey do not, requiring a `tool` setting.

If you don't match your package name and import name (which you should except
for very special cases), you will likely need extra configuration here.

You should have a `README` {% rr PY002 %} and a `LICENSE` {% rr PY003 %} file.
You should have a `docs/` folder {%
rr PY003 %}. You should have a `/tests` folder (recommended) and/or a `src/<package>/tests`
folder.

## Versioning

You can specify the version manually (as shown in the example), but the backends
usually provide some automatic features to help you avoid this. Flit will pull
this from a file if you ask it to. Hatchling and PDM can be instructed to look
in a file or use git.

You will always need to specify that the version will be supplied dynamically
with:

```toml
dynamic = ["version"]
```

Then you'll configure your backend to compute the version.

{% details Hatchling dynamic versioning %}

You can tell hatchling to get the version from VCS. Add `hatch-vcs` to your
`build-backend.requires`, then add the following configuration:

```toml
[tool.hatch]
version.source = "vcs"
build.hooks.vcs.version-file = "src/<package>/version.py"
```

Or you can tell it to look for it in a file (see docs for arbitrary regex's):

```toml
[tool.hatch]
version.path = "src/<package>/__init__.py"
```

(replace `<package>` with the package path).

You should also add these two files:

`.git_archival.txt`:

```text
node: $Format:%H$
node-date: $Format:%cI$
describe-name: $Format:%(describe:tags=true,match=*[0-9]*)$
ref-names: $Format:%D$
```

And `.gitattributes` (or add this line if you are already using this file):

```text
.git_archival.txt  export-subst
```

This will allow git archives (including the ones generated from GitHub) to also
support versioning.

{% enddetails %}

## Including/excluding files in the SDist

This is tool specific.

- [Hatchling info here](https://hatch.pypa.io/latest/config/build/#file-selection).
  Hatchling uses your VCS ignore file by default, so make sure it is accurate
  (which is a good idea anyway).
- [Flit info here](https://flit.readthedocs.io/en/latest/pyproject_toml.html#sdist-section).
  Flit requires manual inclusion/exclusion in many cases, like using a dirty
  working directory.
- [PDM info here](https://pdm-backend.fming.dev/build_config/#include-or-exclude-files).
- Setuptools still uses `MANIFEST.in`.

{: .warning }

> Flit will not use VCS (like git) to populate the SDist if you use standard
> tooling, even if it can do that using its own tooling. So make sure you list
> explicit include/exclude rules, and test the contents:
>
> ```bash
> # Show SDist contents
> tar -tvf dist/*.tar.gz
> # Show wheel contents
> unzip -l dist/*.whl
> ```

<!-- prettier-ignore-start -->

[flit]: https://flit.readthedocs.io
[poetry]: https://python-poetry.org
[pdm]: https://pdm.fming.dev
[trampolim]: https://github.com/FFY00/trampolim
[whey]: https://whey.readthedocs.io
[hatch]: https://hatch.pypa.io/latest
[setuptools]: https://setuptools.readthedocs.io
[pep 621]: https://www.python.org/dev/peps/pep-0621
[scikit-build-core]: https://scikit-build-core.readthedocs.io
[meson-python]: https://meson-python.readthedocs.io

<!-- prettier-ignore-end -->

<script src="{% link assets/js/tabs.js %}"></script>
