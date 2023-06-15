---
layout: page
title: Topical Guides
permalink: /guides/
nav_order: 2
has_children: true
---

The pages here are intended for developers who are making or maintaining a
package and want to follow modern best practices in Python.

New developers are encouraged to read the following pages. Veteran developers
should still check out the [tutorials][], as it has a guide on recommendations
for your `CONTRIBUTING.md`, and at least glance through other sections.

Following that, there are recommendations for [style][], intended to promote
good practices and to ensure continuity across the packages. There is a
[dedicated page for static type checking with MyPy][mypy]. There is then a guide
on [simple packaging][] or [classic packaging][], which should help in ensuring
a consistent developer and user experience when working with distribution.

A section on CI follows, with a [general setup guide][gha_basic], and then two
choices for using CI to distribute your package, on for [pure Python][gha_pure],
and one for [compiled extensions][gha_wheels]. You can read about setting up
good tests on the [pytest page][pytest].

Once you have completed the guidelines, there is a [copier][]/[cookiecutter][]
project, [scientific-python/cookie][], that implements these guidelines and lets
you setup a new package from a template in less than 60 seconds!

You can also evaluate your repository against the guidelines by using
[scientific-python-repo-review][]!

<!-- prettier-ignore-start -->

[tutorials]: {% link pages/tutorials/index.md %}
[style]: {% link pages/guides/style.md %}
[mypy]: {% link pages/guides/mypy.md %}
[simple packaging]: {% link pages/guides/packaging_simple.md %}
[classic packaging]: {% link pages/guides/packaging_classic.md %}
[gha_basic]: {% link pages/guides/gha_basic.md %}
[gha_pure]: {% link pages/guides/gha_pure.md %}
[gha_wheels]: {% link pages/guides/gha_wheels.md %}
[pytest]: {% link pages/guides/pytest.md %}
[scientific-python-repo-review]: {% link pages/guides/repo_review.md %}

[cookiecutter]: https://cookiecutter.readthedocs.io
[copier]: https://copier.readthedocs.io
[scientific-python/cookie]: https://github.com/scientific-python/cookie

<!-- prettier-ignore-end -->
