---
layout: home
title: Home
permalink: /
nav_order: 0
---

# Scientific Python Library Development Guide

This guide is maintained by the scientific Python community for the benefit of
fellow scientists and research software engineers.

**Start at the basics.** Do you have a pile of scientific Python scripts or
Jupyter notebooks that are becoming unwieldy? Are changes to some parts of your
code accidentally breaking other parts of your code? Do you want to more
maintainable, reusable, and shareable form? Start at the
[tutorial]({% link pages/tutorials/index.md %}).

**Learn recommended tools and best practices.** [Topical guides]({% link
pages/guides/index.md %}) provide task-based instruction on topics that scientists
and research software engineers may encounter as their projects evolve and grow.
This covers modern packaging([simple][] or [compiled][]), [style checking][], [testing][],
[documentation][], [static typing][], [CI][], and much more!

{: .highlight-title }

> New project template
>
> This guide comes with a [copier][]/[cookiecutter][]/[cruft][] template for
> making new repos, [scientific-python/cookie][]. Twelve build backends
> including compiled backends, generation tested in Nox, and kept in-sync with
> the guide.

{: .important-title }

> Checking an existing project
>
> We provide [sp-repo-review][], a set of [repo-review][] checks for comparing
> your repository with the guidelines, runnable right in the guide via
> WebAssembly! All checks point to a linked badge in the guide.

**Learn to write better research code.** A high-level document on
[principles]({% link pages/principles/index.md %}) provides advice based on the
community's collective experience building code that is easier for researchers
to use successfully and easier to maintain over time.

**Use our solutions for common tasks.** A growing collection of
[patterns]({% link pages/patterns/index.md %}) provides tested approaches for
tasks and can be tricky to get exactly right, such as including data files with
Python packages.

## Related Resources

This guide does _not_ cover the basics of Python itself or the scientific Python
libraries; it focuses on making or maintaining a package. We recommend the
[SciPy Lecture Notes](https://scipy-lectures.org/) if you want info.

This guide also does not cover version control, but it is essential to have a
basic facility with git to use these tools successfully. We recommend the
[Software Carpentry lesson on git](https://swcarpentry.github.io/git-novice/).

{: .note-title }

> History
>
> This guide (along with cookie & repo-review) started in [Scikit-HEP][]
> in 2020. It was merged with the [NSLS-II][] guidelines and moved to Scientific
> Python at the [2023 Scientific Python Developer Summit][2023 spdev], along
> with many updates. Improved support for compiled components supported in part
> by NSF cooperative agreement [OAC-2209877][].

<!-- prettier-ignore-start -->
[scientific-python/cookie]: https://github.com/scientific-python/cookie
[simple]:                   {% link pages/guides/packaging_simple.md %}
[compiled]:                 {% link pages/guides/packaging_compiled.md %}
[style checking]:           {% link pages/guides/style.md %}
[testing]:                  {% link pages/guides/pytest.md %}
[documentation]:            {% link pages/guides/docs.md %}
[static typing]:            {% link pages/guides/mypy.md %}
[ci]:                       {% link pages/guides/gha_pure.md %}
[sp-repo-review]:           {% link pages/guides/repo_review.md %}
[repo-review]:              https://repo-review.readthedocs.io
[copier]:                   https://copier.readthedocs.io
[cookiecutter]:             https://cookiecutter.readthedocs.io
[cruft]:                    https://cruft.github.io/cruft
[2023 spdev]:               https://scientific-python.org/summits/developer/2023
[scikit-hep]:               https://scikit-hep.org
[OAC-2209877]:              https://www.nsf.gov/awardsearch/showAward?AWD_ID=2209877&HistoricalAwards=false
[nsls-ii]:                  https://nsls-ii.github.io
<!-- prettier-ignore-end -->
