# Topical Guides

The pages here are intended for developers who are making or maintaining a
package and want to follow modern best practices in Python.

New developers are encouraged to read the following pages. Veteran developers
should still check out the [tutorials][], as it has a guide on recommendations
for your `CONTRIBUTING.md`, and at least glance through other sections.

Following that, there are recommendations for [style][], intended to promote
good practices and to ensure continuity across the packages. There is a
[dedicated page for static type checking with MyPy][mypy]. There is then a guide
on [simple packaging][], [compiled packaging][], or even [classic packaging][],
which should help in ensuring a consistent developer and user experience when
working with distribution.

A section on CI follows, with a [general setup guide][gha_basic], and then two
choices for using CI to distribute your package, one for
[pure Python][gha_pure], and one for [compiled extensions][gha_wheels]. You can
read about setting up good tests on the [pytest page][pytest], with
[coverage][]. There's also a page on setting up [docs][], as well as a page on
[security][] best practices.

:::{tip} New project template
Once you have completed the guidelines, there is a
[copier][]/[cookiecutter][]/[cruft][] project, [scientific-python/cookie][],
that implements these guidelines and lets you setup a new package from a
template in less than 60 seconds! Nine build backends including compiled
backends, generation tested in Nox, and kept in-sync with the guide.
:::

:::{important} Checking an existing project
We provide [sp-repo-review][], a set of [repo-review][] checks for comparing
your repository with the guidelines, runnable [right in the guide][] via
WebAssembly! All checks point to a linked badge in the guide.
:::

[tutorials]:          tutorials/index
[style]:              guides/style
[mypy]:               guides/mypy
[docs]:               guides/docs
[simple packaging]:   guides/packaging-simple
[compiled packaging]: guides/packaging-compiled
[classic packaging]:  guides/packaging-classic
[coverage]:           guides/coverage
[gha_basic]:          guides/gha-basic
[gha_pure]:           guides/gha-pure
[gha_wheels]:         guides/gha-wheels
[security]:           guides/security
[pytest]:             guides/pytest
[right in the guide]: guides/repo-review

[cookiecutter]:             https://cookiecutter.readthedocs.io
[copier]:                   https://copier.readthedocs.io
[cruft]:                    https://cruft.github.io/cruft
[repo-review]:              https://repo-review.readthedocs.io
[sp-repo-review]:           https://pypi.org/project/sp-repo-review
[scientific-python/cookie]: https://github.com/scientific-python/cookie


```{tableofcontents}
```
