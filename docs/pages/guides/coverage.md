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

- `coverage` (AKA `coverage.py`): a tool to calculate and visualize Python
  coverage
- `pytest-cov`: an integration of `coverage` with `pytest`
- `Codecov`: integrates with remote repositories, allowing developers to see and
  compare coverage value with each CI run
- `GitHub Actions`: allows users to automatically upload coverage reports to
  `Codecov`

{: .note-title }

> Are there any alternatives?
>
> Coveralls is an alternative coverage platform, but we recommend using Codecov
> because of its ease of use and integration with GitHub Actions.

{: .highlight-title }

> Should increasing the coverage value be my top priority?
>
> A low coverage percentage will definitely motivate you to add more tests, but
> adding weak tests just for coverage's sake is not a good idea. The tests
> should test your codebase thoroughly and should not be unreliable.

### Running your tests with coverage

There are two common ways to calculate coverage: using `coverage` or using
`pytest-cov`. While `pytest-cov` is simpler on the command line, and it promises
nice integration with features like `pytest-xdist`, in practice it tends to be
more rigid and have more issues than running `coverage` directly. If you are
using a task runner like `nox`, the extra complexity of running coverage
directly is hidden away from normal use, so we recommend that, but will show
both methods below. If you are not running `pytest`, but instead are running an
example or a script, you have to use `coverage` directly.

{% tabs %} {% tab cov coverage %}

Make sure you install `coverage[toml]`.

`coverage` has several commands; the most important one is `coverage run`. This
will run any Python process and collect coverage, generating a `.coverage` file
with the calculated coverage value. Running it usually looks like this:

```bash
coverage run -m pytest
```

You should configure `coverage` through your pyproject.toml.

To see a coverage report, run:

```bash
coverage report
```

This looks for a `.coverage` file and displays the result. There are many output
formats for reports.

{% endtab %} {% tab pycov pytest-cov %}

Make sure you install `pytest-cov`.

`pytest` allows users to pass the `--cov` option to automatically invoke
`pytest-cov`, which then generates a `.coverage` file with the calculated
coverage value. The value of `--cov` option should be set to the name of your
package. For some reason, pytest-cov also has a hard time finding the coverage
configuration in your pyproject.toml, so you should also hard-code that with
`--cov-config=pyproject.toml`. For example, run the following command to run
tests to generate a `.coverage` file for the vector package:

```bash
python -m pytest -ra --cov=vector --cov-config=pyproject.toml
```

`--cov` option will also print a minimal coverage report in the terminal itself!
See the [docs](https://pytest-cov.readthedocs.io/en/latest/) for more options.

Coverage pytest arguments can be placed in your pytest configuration file or in
your task runner. It also will (mostly) respect the coverage configuration,
shown below.

{% endtab %} {% endtabs %}

### Configuring coverage

There is a configuration section in `pyproject.toml` for coverage. Here are some
common options
[(see the docs for more)](https://coverage.readthedocs.io/en/latest/config.html):

```toml
[tool.coverage]
run.core = "sysmon"
run.disable_warnings = ["no-sysmon"]
run.relative_files = true
run.source_pkgs = [ "package" ]
report.show_missing = true
```

Setting `run.core` to `sysmon` will make coverage much faster on 3.12+ without
branch coverage, or 3.14+ if yyou are using branch coverage (see below). To
avoid a warning on older Pythons without `sysmon`, you need to add the
`no-sysmon` code to `run.disable_warnings`. If you want relative paths reported,
`relative_files=true` does that. And `source_pkgs` is one way to tell coverage
which packages are to be monitored for coverage. You can also set
`run.source_dirs`. You can use `report.show_missing` to show the missing line
number ranges.

If you want to include branches in your coverage, set `run.branch = true`. If
you are using subprocess calls, you can add the subprocess patching mechanism
with `run.patch = [ "subprocess" ]`; though keep in mind, this behaves like (and
enables) `parallel=True`; you'll need to combine coverage files after running.
`pytest-cov` sort of does this combine for you, sometimes.

There are also useful reporting options. `report.exclude_lines = [...]` allows
you to exclude lines from coverage. `report.fail_under` can trigger a failure if
coverage is below a percent (like 100).

### Calculating code coverage in your workflows

Your workflows should produce a `.coverage` file as outlined above. This file
can be uploaded to `Codecov` using the [codecov/codecov-action][] action.

If you would rather do it yourself, you should collect coverage files from all
your jobs and combine them into one `.coverage` file before running
`coverage report`, so that you get a combined score.

#### Manually combining coverage

If you are running in parallel, either with `pytest-xdist`, you can set
`run.parallel` to `true`, which will add a unique suffix to the coverage file(s)
produced. If you are using the multiprocessing patch, that also will generate a
unique suffix for each process launch.

You can control the prefix with the environment variable `COVERAGE_FILE`, which
defaults to `.coverage`. This is mostly commonly used to add your own custom
suffixes, like `COVERAGE_FILE=.coverage.win32.py312`. This is how you can
manually produce multiple files from task runner jobs.

Here's an example nox job:

{% tabs %} {% tab cov coverage %}

```python
@nox.session(python=ALL_PYTHONS)
def tests(session: nox.Session) -> None:
    env = {"COVERAGE_FILE": coverage_file}
    session.install("-e.", "--group=cov")
    session.run(
        "coverage",
        "run",
        "-m",
        "pytest",
        *session.posargs,
        env=env,
    )
```

{% endtab %} {% tab pycov pytest-cov %}

```python
@nox.session(python=ALL_PYTHONS)
def tests(session: nox.Session) -> None:
    env = {"COVERAGE_FILE": coverage_file}
    session.install("-e.", "--group=cov")
    session.run(
        "pytest",
        "--cov",
        "--cov-config=pyproject.toml",
        *session.posargs,
        env=env,
    )
```

{% endtab %} {% endtabs %}


#### Merging and reporting

If you are running in multiple jobs, you should use upload/download artifacts so
they are all available in a single combine job at the end. Each one should have
a unique suffix. Then you just need `coverage combine`, which will combine all
the files into a single `.coverage` file which you can use with
`coverage report`. You can even report in markdown format and write it to the
GitHub Actions summary if you want.

Here's an example in nox:

```python
@nox.session(default=False, requires=["tests"])
def coverage(session: nox.Session) -> None:
    session.install("coverage[toml]")
    session.run("coverage", "combine")
    session.run("coverage", "report")
    session.run("coverage", "erase")
```


#### Configuring Codecov and uploading coverage reports

Interestingly, `Codecov` does not require any initial configurations for your
project, given that you have already signed up for the same using your GitHub
account. `Codecov` requires you to push or upload your coverage report, after
which it automatically generates a `Codecov` project for you.

`Codecov` maintains the [codecov/codecov-action][] GitHub Action to make
uploading coverage reports easy for users. A minimal working example for
uploading coverage reports through your workflow, which should be more than
enough for a simple testing suite, can be written as follows:

{% raw %}

```yaml
- name: Upload coverage report
  uses: codecov/codecov-action@v5
  with:
    token: ${{ secrets.CODECOV_TOKEN }}
```

{% endraw %}

The lines above should be added after the step that runs your tests with the
`--cov` option. See the [docs](https://github.com/codecov/codecov-action#usage)
for all the optional options. You'll need to specify a `CODECOV_TOKEN` secret,
as well.

#### Using codecov.yml

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

<script src="{% link assets/js/tabs.js %}"></script>
