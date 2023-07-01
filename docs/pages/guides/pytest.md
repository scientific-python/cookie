---
layout: page
title: "Testing with pytest"
permalink: /guides/pytest/
nav_order: 2
parent: Topical Guides
---

{% include toc.html %}

# Testing with pytest

Tests are crucial to writing reliable software. A good test suite allows you to:

- Immediately know if a new platform or software version works,
- Refactor and cleanup your code with confidence,
- Evaluate the effect of additions and changes.

Python used to have three major choices for tests; but now [pytest][] is used
almost exclusively. Testing is never an install requirement, so there's no harm
in using pytest. The goals of writing good tests are:

- Simplicity: the easier / nicer your tests are to write, the more you will
  write.
- Coverage: using as many inputs as possible increases the chances of finding
  something that breaks.
- Performance: the faster the tests, the more situations you can run your tests
  in CI.
- Reporting: when things break, you should get good information about what
  broke.

{: .note-title }

> What about other choices?
>
> The alternative library, `nose`, has been abandoned in favor of `pytest`,
> which can run nose-style tests. The standard library has a test suite as well,
> but it's extremely verbose and complex; and since "developers" run tests, your
> test requirements don't affect users. And `pytest` can run stdlib style
> testing too. So just use `pytest`. All major packages use it too, including
> `NumPy`. Most other choices, like [Hypothesis][], are related to `pytest` and
> just extend it.

### Basic test structure

You should make a folder called "tests" in your repository (probably alongside
your `src` or module folder, but rarely they are placed inside the module
folder). Your files will be called `test_*.py`; pytest's default discovery
expects the word "test" to be in everything (yes, you can place tests alongside
or inside your module because of this). This is an example of a test:

`test_basic.py`:

```python
def test_funct():
    assert 4 == 2**2
```

This looks simple, but it is doing several things:

- The name of the function includes `test`, so it will run as a test.
- The Python `assert` statement is rewritten by pytest to capture exactly what
  happens. If it fails, you will get a clear, detailed report on what each value
  was.

### Configuring pytest

pytest supports configuration in `pytest.ini`, `setup.cfg`, or, since version 6,
`pyproject.toml` {% rr PP301 %}. Remember, pytest is a developer requirement,
not a user one, so always require 6+ (or 7+) and use `pyproject.toml`. This is
an example configuration:

```toml
[tool.pytest.ini_options]
minversion = "6.0"
addopts = ["-ra", "--showlocals", "--strict-markers", "--strict-config"]
xfail_strict = true
filterwarnings = ["error"]
log_cli_level = "info"
testpaths = [
  "tests",
]
```

{% rr PP302 %} The `minversion` will print a nicer error if your `pytest` is too
old (though, ironically, it won't read this is the version is too old, so
setting "6" or less in `pyproject.toml` is rather pointless). The `addopts`
setting will add whatever you put there to the command line when you run;
{% rr PP308 %} `-ra` will print a summary "r"eport of "a"ll results, which gives
you a quick way to review what tests failed and were skipped, and why.
`--showlocals` will print locals in tracebacks. {% rr PP307 %}
`--strict-markers` will make sure you don't try to use an unspecified fixture.
{% rr PP306 %} And `--strict-config` will error if you make a mistake in your
config. {% rr PP305 %} `xfail_strict` will change the default for `xfail` to
fail the tests if it doesn't fail - you can still override locally in a specific
xfail for a flaky failure. {% rr PP309 %} `filter_warnings` will cause all
warnings to be errors (you can add allowed warnings here too, see below).
{% rr PP304 %} `log_cli_level` will report `INFO` and above log messages on a
failure. {% rr PP303 %} Finally, `testpaths` will limit `pytest` to just looking
in the folders given - useful if it tries to pick up things that are not tests
from other directories.
[See the docs](https://docs.pytest.org/en/stable/customize.html) for more
options.

pytest also checks the current and parent directories for a `conftest.py` file.
If it finds them, they will get run outer-most to inner-most. These files let
you add fixtures and other pytest configurations (like hooks for test discovery,
etc) for each directory. For example, you could have a "mock" folder, and in
that folder, you could have a `conftest.py` that has a mock fixture with
`autouse=True`, then every test in that folder will get this mock applied.

In general, do not place a `__init__.py` file in your tests; there's not often a
reason to make the test directory importable, and it can confuse package
discovery algorithms.

Python hides important warnings by default, mostly because it's trying to be
nice to users. If you are a developer, you don't want it to be "nice". You want
to find and fix warnings before they cause user errors! Locally, you should run
with `-Wd`, or set `export PYTHONWARNINGS=d` in your environment. The `pytest`
warning filter "error" will ensure that `pytest` will fail if it finds any
warnings. You can list warnings that should be hidden or just shown without
becoming errors using the syntax
`"<action>:Regex for warning message:Warning:package"`, where `<action>` can
tends to be `default` (show the first time) or `ignore` (never show). The regex
matches at the beginning of the error unless you prefix it with `.*`.

### Running pytest

You can run pytest directly with `pytest` or `python -m pytest`. You can
optionally give a directory or file to run on. You can also select just some
subset of tests with `-k <expression>`, or an exact test with
`filename.py::test_name`.

If a test fails, you have lots of options to save time in debugging. Adding
`-l`/`--showlocals` will print out the local values in the tracebacks (and can
be added by default, see above). You can run `pytest` with `--pdb`, which will
drop you into a debugger on each failure. Or you can use `--trace` which will
drop you into a debugger at the start of each test selected (so probably use the
selection methods above). `pytest` also supports `breakpoint()`. You can also
start out in your debugger at the beginning of the last failed test with
`--trace --lf`. [See the docs](https://docs.pytest.org/en/stable/usage.html) for
more running tips.

## Guidelines for writing good tests

Time spent learning all the powerful tools pytest has to offer will be well
spent! You can make your tests more granular, mock things that aren't available
(or are slow to run), parametrize, and much more.

### Tests should be easy

Always use pytest. The built-in unittest is _very_ verbose; the simpler the
writing of tests, the more tests you will write!

```python
import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        x = 1
        self.assertEquals(x, 2)
```

Contrast this to pytest:

```python
def test_something():
    x = 1
    assert x == 2
```

pytest still gives you clear breakdowns, including what the value of `x`
actually is, even though it seems to use the Python `assert` statement! You
don't need to set up a class (though you can), and you don't need to remember 50
or so different `self.assert*` functions! pytest can also run unittest tests, as
well as the old `nose` package's tests, too.

Approximately equals is normally ugly to check, but pytest makes it easy too:

```python
from pytest import approx


def test_approx():
    0.3333333333333 == approx(1 / 3)
```

This natively works with NumPy arrays, too! Always prefer
`array1 == approx(array2)` over the functions in the `numpy.testing` module if
you can, it is simpler and the reporting is better.

### Tests should test for failures too

You should make sure that expected errors are thrown:

```python
import pytest


def test_raises():
    with pytest.raises(ZeroDivisionError):
        1 / 0
```

You can check for warnings as well, with `pytest.warns` or
`pytest.deprecated_call`.

### Tests should stay easy when scaling out

pytest [uses fixtures](https://docs.pytest.org/en/stable/fixture.html) to
represent complex ideas, like setup/teardown, temporary resources, or
parameterization.

A fixture looks like a function argument; pytest recognizes them by name:

```python
def test_printout(capsys):
    print("hello")

    captured = capsys.readouterr()
    assert "hello" in captured.out
```

Making a new fixture is not too hard, and can be placed in the test file or in
`conftest.py`:

```python
@pytest.fixture(params=[1, 2, 3], ids=["one", "two", "three"])
def ints(request):
    return request.param
```

We could have left off `ids`, but for complex inputs, this lets the tests have
beautiful names.

Now, you can use it:

```python
def test_on_ints(ints):
    assert ints**2 == ints * ints
```

Now you will get three tests, `test_on_ints-one`, `test_on_ints-two`, and
`test_on_ints-three`!

Fixtures can be scoped, allowing simple setup/teardown (use `yield` if you need
to run teardown). You can even set `autouse=True` to use a fixture always in a
file or module (via `conftest.py`). You can have `conftest.py`'s in nested
folders, too!

Here's an advanced example, which also uses `monkeypatch`, which is a great way
for making things hard to split into units into unit tests. Let's say you wanted
to make a test that "tricked" your code into thinking that it was running on
different platforms:

```python
import platform
import pytest


@pytest.fixture(params=["Linux", "Darwin", "Windows"], autouse=True)
def platform_system(request, monkeypatch):
    monkeypatch.setattr(platform, "system", lambda _: request.param)
```

Now every test in the file this is in (or the directory that this is in if in
conftest) will run three times, and each time will identify as a different
`platform.system()`! Leave `autouse` off, and it becomes opt-in; adding
`platform_system` to the list of arguments will opt in.

### Tests should be organized

You can use `pytest.mark.*` to
[mark](https://docs.pytest.org/en/stable/mark.html) tests, so you can easily
turn on or off groups of tests, or do something else special with marked tests,
like tests marked "slow", for example. Just add `-m <marker>` when running
pytest to run a group of marked tests. This is an expression; you can use
`not <marker>` as well.

Probably the most useful built-in mark is `skipif`:

```python
@pytest.mark.skipif("sys.version_info >= (3, 8)")
def test_only_on_38plus():
    x = 3
    assert f"{x = }" == "x = 3"
```

Now this test will only run on Python 3.8 or newer, and will be skipped on
earlier versions. You don't have to use a string for the condition, but if you
don't, add a `reason=` so there will still be a nice printout explaining why the
test was skipped.

You can also use `xfail` for tests that are expected to fail (you can even
strictly test them as failing if you want). You can use `parametrize` to make a
single parameterized test instead of sharing them (with fixtures). There's a
`filterwarnings` mark, too.

Many pytest plugins support new marks too, like `pytest-parametrize`. You can
also use custom marks to enable/disable groups of tests, or to pass data into
fixtures.

### Tests should test the installed version, not the local version

Your tests should run against an _installed_ version of your code. Testing
against the _local_ version might work while the installed version does not (due
to a missing file, changed paths, etc). This is one of the big reasons to use
`/src/package` instead of `/package`, as `python -m pytest` will pick up local
directories and `pytest` does not. Also, there may come a time when someone
(possibly you) needs to run your tests off of a wheel or a conda package, or in
a build system, and if you are unable to test against an installed version, you
won't be able to run your tests! (It happens more than you might think).

### Mock expensive or tricky calls

If you have to call something that is expensive or hard to call, it is often
better to mock it. To isolate parts of your own code for "unit" testing, mocking
is useful too. Combined with monkey patching (shown in an earlier example), this
is a very powerful tool!

Say we want to write a function that calls matplotlib. We could use `pytest-mpl`
to capture images and compare them in our test, but that's an integration test,
not a unit test; and if something does go wrong, we are stuck comparing
pictures, and we don't know how our usage of matplotlib changed from the test
report. Let's see how we could mock it. We will use the `pytest-mock` plugin for
pytest, which simply adapts the built-in `unittest.mock` in a more native pytest
fashion as fixtures and such.

```python
@pytest.fixture
def mock_matplotlib(mocker):
    fig = mocker.Mock(spec=matplotlib.pyplot.Figure)
    ax = mocker.Mock(spec=matplotlib.pyplot.Axes)
    line2d = mocker.Mock(name="step", spec=matplotlib.lines.Line2D)
    ax.plot.return_value = (line2d,)

    # Patch the main library if used directly
    mpl = mocker.patch("matplotlib.pyplot", autospec=True)
    mocker.patch("matplotlib.pyplot.subplots", return_value=(fig, ax))

    return SimpleNamespace(fig=fig, ax=ax, mpl=mpl)
```

Here, we've just mocked the parts we touch in our plot function that we need to
test. We use `spec=` to get the mock to just respond to the same things that the
original object would have responded to. We can set return values so that our
objects behave like the real thing. Using it is simple:

```python
def test_my_plot(mock_matplotlib):
    ax = mock_matplotlib.ax
    my_plot(ax=ax)

    assert len(ax.mock_calls) == 6

    ax.plot.assert_called_once_with(
        approx([1.0, 3.0, 2.0]),
        label=None,
        linewidth=1.5,
    )
```

If this changes, we immediately know exactly what changed - and this runs
instantly, we aren't making any images! While this is a little work to set up,
it pays off in the long run.

The documentation at [pytest-mock][] is helpful, though most of it just
redirects to the standard library [unittest.mock][].

[hypothesis]: https://hypothesis.readthedocs.io
[pytest]: https://docs.pytest.org
[pytest-mock]: https://pypi.org/project/pytest-mock/
[unittest.mock]: https://docs.python.org/3/library/unittest.mock.html
