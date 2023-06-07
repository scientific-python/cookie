# sp-repo-review

[![Actions Status][actions-badge]][actions-link]
[![GitHub Discussion][github-discussions-badge]][github-discussions-link]
[![Live ReadTheDocs][rtd-badge]][rtd-link]

[![PyPI version][pypi-version]][pypi-link]
[![PyPI platforms][pypi-platforms]][pypi-link]

`sp-repo-review` provides checks based on the [Scientific-Python Development
Guide][] at [scientific-python/cookie][].

This tool can check the style of a repository. Use like this:

```bash
pipx run 'sp-repo-review[cli]' <path to repository>
```

This will produce a list of results - green checkmarks mean this rule is
followed, red x’s mean the rule is not. A yellow warning sign means that the
check was skipped because a previous required check failed. Some checks will
fail, that’s okay - the goal is bring all possible issues to your attention, not
to force compliance with arbitrary checks. Eventually there might be a way to
mark checks as ignored.

For example, `GH101` expects all your action files to have a nice `name:` field.
If you are happy with the file-based names you see in CI, you should feel free
to simply ignore this check (just visually ignore it for the moment, a way to
specify ignored checks will likely be added eventually).

All checks are mentioned at least in some way in the [Scientific-Python
Development Guide][]. You should read that first - if you are not attempting to
follow them, some of the checks might not work. For example, the guidelines
specify pytest configuration be placed in `pyproject.toml`. If you place it
somewhere else, then all the pytest checks will be skipped.

<!-- prettier-ignore-start -->

[actions-badge]: https://github.com/scientific-python/cookie/workflows/CI/badge.svg
[actions-link]: https://github.com/scientific-python/cookie/actions
[pypi-link]: https://pypi.org/project/sp-repo-review/
[pypi-platforms]: https://img.shields.io/pypi/pyversions/sp-repo-review
[pypi-version]: https://badge.fury.io/py/sp-repo-review.svg
[docs-badge]: https://readthedocs.org/projects/scientific-python-cookie/badge/?version=latest
[docs-link]: https://scientific-python-cookie.readthedocs.io/en/latest/?badge=latest
[scientific-python development guide]: https://learn.scientific-python.org/development
[scientific-python/cookie]: https://github.com/scientific-python/cookie
[scikit-hep]: https://scikit-hep.org

<!-- prettier-ignore-end -->
