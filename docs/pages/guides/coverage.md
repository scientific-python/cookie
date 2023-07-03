---
layout: page
title: "Code coverage"
permalink: /guides/coverage/
nav_order: 3
parent: Topical Guides
---

{% include toc.html %}

# Code Coverage

The "Code coverage" value of a codebase indicates how much of the
production/development code is covered by the running unit tests. Maintainers
try their best to keep this percentage high, and this process is often automated
using tools such as `GitHub Actions` and `Codecov`. Hence, code coverage becomes
a good metric (not always) to check if a particular codebase is well tested and
reliable.

Tools and libraries used to calculate, read, and visualize coverage reports:

- `pytest-cov`: allows developers to calculate and visualize the coverage value
- `Codecov`: integrates with remote repositories, allowing developers to see and
  compare coverage value with each CI run
- `GitHub Actions`: allows users to automatically upload coverage reports to
  `Codecov`

{: .note-title }

> Are there any alternatives?
>
> `coverage.py` is a popular Python library used to calculate coverage values,
> but it is usually paired with python's `unittest`. On the other hand,
> `pytest-cov` is built to integrate with `pytest` with minimal extra
> configurations. Further, Coveralls is an alternative coverage platform, but we
> recommend using Codecov because of its ease of use and integration with GitHub
> Actions.

{: .highlight-title }

> Should increasing the coverage value be my top priority?
>
> A low coverage percentage will definitely motivate you to add more tests, but
> adding weak tests just for coverage's sake is not a good idea. The tests
> should test your codebase thoroughly and should not be unreliable.

### Calculating code coverage locally

`pytest` allows users to pass the `--cov` option to automatically invoke
`pytest-cov`, which then generates a `.coverage` file with the calculated
coverage value. The value of `--cov` option should be set to the name of your
package. For example, run the following command to run tests to generate a
`.coverage` file for the vector package -

```bash
python -m pytest -ra --cov=vector --cov-branch tests/
```

`--cov` option will also print a minimal coverage report in the terminal itself!
See the [docs](https://pytest-cov.readthedocs.io/en/latest/) for more options.
The `--cov-branch` option will enable
[branch coverage](https://linearb.io/blog/what-is-branch-coverage/).

### Calculating code coverage in your workflows

Your workflows should also run tests with the `--cov` option, which must be set
to your package name. For example -

```yaml
- name: Test package
  run: python -m pytest --cov=vector tests/
```

This will automatically invoke `pytest-cov`, and generate a `.coverage` file,
which can then be uploaded to `Codecov` using the [codecov/codecov-action][]
action.

### Configuring Codecov and uploading coverage reports

Interestingly, `Codecov` does not require any initial configurations for your
project, given that you have already signed up for the same using your GitHub
account. `Codecov` requires you to push or upload your coverage report, after
which it automatically generates a `Codecov` project for you.

`Codecov` maintains the [codecov/codecov-action][] GitHub Action to make
uploading coverage reports easy for users. A minimal working example for
uploading coverage reports through your workflow, which should be more than
enough for a simple testing suite, can be written as follows:

```yaml
- name: Upload coverage report
  uses: codecov/codecov-action@v3.1.0
```

The lines above should be added after the step that runs your tests with the
`--cov` option. See the [docs](https://github.com/codecov/codecov-action#usage)
for all the optional options.

### Using codecov.yml

One can also configure `Codecov` and coverage reports passed to `Codecov` using
`codecov.yml`. `codecov.yml` should be placed inside the `.github` folder, along
with your `workflows` folder. Additionally, `Codecov` allows you to create and
edit this `YAML` file directly through your `Codecov` project's settings!

A recommended configuration for `.github/codecov.yml`:

```yaml
codecov:
  notify:
    after_n_builds: x
coverage:
  status:
    project:
      default:
        target: auto
        threshold: 5%
    patch:
      default:
        informational: true
```

where `x` is the number of uploaded reports `Codecov` should wait to receive
before sending statuses. This would ensure that the `Codecov` checks don't fail
before all the coverage reports are uploaded. You can control the levels which
are considered failing; the config above sets a loss of up to 5% as okay, and
avoids patch coverage reporting a failure (otherwise, just changing a single
uncovered line could cause a "failure" report on the PR). If you have 100%
coverage, then you can remove the coverage failure settings, as you want any
loss of coverage to fail. See the
[docs](https://docs.codecov.com/docs/codecov-yaml) for all the options.

<!-- ### Coverage for projects written in Python and C++

TODO -->

[codecov/codecov-action]: https://github.com/codecov/codecov-action
