---
layout: page
title: Testing recommendations
permalink: /principles/testing/
nav_order: 2
parent: Principles
---

{% include toc.html %}

# Testing recommendations

## Outside-In Tests

- live outside of source code, in the tests/ directory
- Describe the various types of outsid-in tests (integration, fuzz, e2e, API)
- Reference topical guides
- Provide suggestions for testing categories

## Unit Tests

### Advantages of unit testing:

Unit tests ensure that the code, as written, is correct, and executes properly.
they communicate the intention of the creator of the code, how the code is
expected to behave, in its expected use-case.

Unit tests should be simple, isolated, and run very quickly. Which allows us to
run them quickly, while we make changes to the code (even automatically, each
time we save a file for example) to ensure our changes did not break anything...
or only break what we expected to.

Writing unit tests can reveal weakensses in our implementations, and lead us to
better design decisions:

- If the test requires excessive setup, the unit may be dependent on too many
  external variables.
- If the test requires many assertions, the unit may be doing too many things /
  have too many side-effects.
- If the unit is very difficult to test, it will likely be difficult to
  understand and maintain. Refactoring code to make it easier to test often
  leads us to write better code overall.

### When to write unit tests:

Unit tests are considered "low level", and used for [Isolation Testing](). Not
all projects need full unit test coverage, some may not need unit tests at all.

- When your project matures enough to justify the work! higher-level testing is
  often sufficient for small projects, which are not part of critical
  infrastructure.

- When you identify a critical part of the code-base, parts that are especially
  prone to breaking, Use unit tests to ensure that code continues to behave as
  designed.

- When other projects start to depend heavily on your library, thorough unit
  testing helps ensure the reliability of your code for your users.

- When doing test-driven development, unit tests should be created after
  higher-level 'integration' or 'outside-in' test cases, before writing the code
  to make the tests pass.

### Guidelines for unit testing:

- Unit tests live alongside the code they test, in a /tests folder. They should
  be in a different directory than higher-level tests (integration, e2e,
  behavioral, etc.) So that they can be run quickly before the full test suite,
  and to avoid confusing them.

- Test files should be named `test_{{file under test}}.py`, so that test runners
  can find them easily.

- test\_.py files should match your source files (file-under-test) one-to-one,
  and contain only tests for code in the file-file-under test. The code in
  `mymodule/source.py` is tested by `mymodule/tests/test_source.py`.

- Keep it simple! If a test-case requires extra setup and external tools, It may
  be more appropriate as an external test, instead of in the unit tests

- Avoid the temptation to test edge-cases! Focus your unit tests on the
  "happy-path". The UT should describe the expected and officially supported
  usage of the code under test.

- Isolation: Test single units of code! A single Function, or a single attribute
  or method on a class. If you have two units (classes, functions, class
  attributes) with deeply coupled behavior, it is better to test them
  individually, using mocking and patching, instead of testing both in a single
  test. This makes refactoring easier, helps you understand the interactions
  between units, and will correctly tell you which part is failing if one
  breaks.

#### Importing in test files:

Keep things local! prefer to import only from the file-under-test when possible.
This helps keep the context of the unit tests focused on the file-under-test.

It makes refactoring much smoother; think about factoring a class out of a
source file where many functions operate on it, and tests require it.

```python
# src/project/lib.py
class MyClass: ...


def func(my_class: MyClass): ...


# src/project/tests/test_lib.py
from project.lib import MyClass, func


def test_func():
    ret = func(MyClass())
    ...


class TestMyClass: ...
```

When we move MyClass into another source file, we only need to move its
TestMyClass unit tests along with it. Even moving MyClass to another module, or
swapping it for a drop-in replacement, is minimally disruptive to the tests that
rely on it.

```python
# src/project/lib.py
from .util import MyClass


def func(my_class: MyClass): ...


# src/project/tests/test_lib.py
from project.lib import MyClass, func


def test_func():
    ret = func(MyClass())
    ...
```

- Importing from other source files is a code smell (for unit tests), It
  indicates that the test is not well isolated.

It is worth cultivating a deep understanding of how python's imports work. The
interactions between imports and patches can some times be surprising, and cause
us to write invalid tests... or worse, tests that pass when they should fail.
These are a few of the cases that I have seen cause the most confusion.

- If you import `SomeThing` from your file-under-test, Then patch
  `file.under.test.SomeThing`, it does not patch `SomeThing` in your test file.
  Only in the file-under-test. So, code in your file-under-test which calls
  `SomeThing()`, will use the Mock. But in your test case. `SomeThing()` will
  create a new instance, not call the Mock.

- Prefer to import only the object that you actually use, not the entire
  library.
  - This simplifies mocking/patching in unit tests.
  - Makes using drop-in replacements simpler. Changing
    `from pandas import DataFrame` to `from polars import DataFrame` in your
    file-under-test, should result in all tests passing, with no other changes.

It is common practice to import all of pandas or numpy `import numpy as np`, And
this style is helpful for ensuring that we are using the version of `sum()` we
expect... was it python's builtin `sum` or `np.sum`? However, as we develop our
unit tests, this can cause difficulty with mocking, and complicate refactoring.
consider the benefits of refactoring your imports like so:

```python
from numpy import sum as numeric_sum, Array as NumericArray
```

#### Running unit tests:

- Pytest is great for running tests in your development environments!
- to run unit tests in your source folder, from your package root, use
  `pytest {{path/to/source}}`
- To run tests from an installed package (outside of your source repository),
  use `pytest --pyargs {package name}}`

#### Mocking and Patching to Isolate the code under test:

When the unit you are testing touches any external unit (usually something you
imported, or another unit that has its own tests), the external unit should be
Patched, replacing it with a Mock for the durration of the test.

- Verify that the external unit is called with the expected input
- Verify that any value returned from the external unit is utilized as expected.

```python
import pytest

SRC = "path.to.module.under.test"


def test_myfunction(mocker):
    patchme: Mock = mocker.patch(f"{SRC}.patchme", autospec=True)
    ret = myfunction()
    patchme.assert_called_with("input from myfunction")
    assert ret is patchme.return_value
```

- Consider what needs to be mocked, and the level of isolation your unit test
  really needs.
  - Anything imported into the module you are testing should probably be mocked.
  - external units with side-effects, or which do a lot of computation should
    probably be mocked.
  - Some people prefer to never test `_private` attributes.

- Excessive mocking is a code smell! Consider ways to refactor the code, so that
  it needs fewer mocks, less setup, and fewer assertions in a single test case.
  This frequently leads us to write more readable and maintainable code.

## Diagnostic Tests

Diagnostic tests are used to verify the installation of a package. They should
be runable on production systems, like when we need to ssh into a live server to
troubleshoot problems.

### Advantages of Diagnostic Tests

- Diagnostic tests allow us to verify an installation of a package.
- They can be used to verify system-level dependencies like:
  - Compiled binary dependencies
  - Access to specific hardware, like GPUs

### Guidelines for Diagnostic Tests

- Consider using the stdlib `unittest.TestCase` and other stdlib tools instead
  of pytest. To allow running unit tests for diagnostics in production
  environments, without installing additional packages.

- Test files should be named `test_{{file under test}}.py`, so that stdlib
  unittest can find them easily.

### Mocking and Patching to Isolate the code under test:

Test Isolation is less necessary in diagnostic tests than unit tests. We often
want diagnostic tests to execute compiled code, or run a test on GPU hardware.
In cases where we do need to mock some part of our code, `unittest.mock.patch`
is similar to the pytest mocker module.

```python
from unittest.mock import patch, Mock

SRC = "mymodule.path.to.source"


@patch(f"{SRC}.patchme", autospec=true)
def test_myfunction(t, patchme: Mock):
    ret = myfunction()
    patchme.assert_called_with("input from myfunction")
    t.assertIs(ret, patchme.return_value)
```

### Running Diagnostic Tests:

stdlib's unittest can be used in environments where pytest is not available:

- To use unittest to run tests from an installed package (outside of your source
  repository), use `python -m unittest discover -s {{module.name}}`
- To use unittest to run tests in your source folder, from your package root,
  use
  `python -m unittest discover --start-folder {{source folder}} --top-level-directory .`
