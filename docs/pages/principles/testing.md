---
layout: page
title: Testing recommendations
permalink: /principles/testing/
nav_order: 2
parent: Principles
---

{% include toc.html %}

# Testing recommendations

In this guide, we will provide a roadmap and best-practices for creating test
suites for python projects.

We will describe the most important types of test suites, the purposes they
serve and differences between them. They will be presented in OutSide -> In
order, which is our recommend approach. Starting with
[Public Interface tests](#public-interface-tests), which test your code from the
perspective of your users, focusing on the behavior of the public interface and
the Features that your project provides. Then we will cover
[Project Level Integration tests](#project-level-integration-tests), which test
that the various parts of your package work together, and work with the other
packages it depends on. Finally we will cover the venrable
[Unit Test](#unit-tests), which test the correctness of your code from a
perspective internal to your codebase, tests individual units in isolation, and
are optimized to run quickly and often.

These 3 test suites will cover the bulk of your testing needs and help get your
project to a reliable and maintainable state. We will also discuss some more
specialized and advanced types of test cases in our
[Taxonomy of Test Cases](#additional-types-of-test-suites) section.

## Advantages of Testing

- Trustworthy code: Well tested code, is code that you can trust to behave as
  expected.
- Living Documentation: A good test is a form of documentation, which tells us
  how the code is expected to behave, communicates the intent of the author, and
  is validated every time the test is run.
- Preventing Failure: Tests provide safety against many ways code can fail, from
  errors in implementation, to unexpected changes in upstream dependencies.
- Confidence when making changes: A thorough suite of tests allows developers to
  add features, fix bugs, and refactor code, with a degree of confidence that
  their changes do not break existing features, or cause unexpected
  side-effects.

## Any test case is better than none

When in doubt, write the test that makes sense at the time.

- Test critical behaviors, features, and logic
- Write clear, expressive, well documented tests
  - Tests are documentation of the developer's intentions
  - Good tests make it clear what they are testing and how

While you are learning, and writing your first test suites, try not to get
bogged down in the taxonomy of test types. As you write and use your test suite,
the reason for classifying and sorting some types of tests into different test
suites will become apparent.

## As long as that test is correct...

It can be surprisingly easy to write a test that passes when it should fail,
especially when using complicated mocks and fixtures. The best way to avoid this
is to deliberately break the code you are testing, hard-code a failure, and run
the test-case to make sure it fails when the code is broken.

- Check that your test fails when it should!
- Keep It Simple: Excessive use of mocks and fixtures can make it difficult to
  know if our test is running the code we expect it to.
- Test one thing at a time: A single test should test a single behavior, and it
  is better to write many test cases for a single function or class, than one
  giant case.

## Public Interface Tests

A good place to start writing tests is from the perspective of a user of your
module or library, as described in the [Test
Tutorial]({% link pages/tutorials/test.md %}), and [Testing with pytest
guide]({% link pages/guides/pytest.md %}). These tests follow the "Detroit
School", focusing on behavior, avoiding testing of private attributes,
minimizing the use of mocks/patches/test-doubles.

- These test cases live outside of your source code.
- Test the code as you expect your users to interact with it.
- Keep these tests simple, and easily readable, so that they provide good
  documentation when a user asks "how should I use this feature"
- Focus on the supported use-case, and avoid extensive edge-case testing
  (edge-case and exhaustive input testing will be handled in a separate test
  suite)

{: .highlight-title }

> A note to new test developers:
>
> This is a good place to pause and go write some tests. The rest of these
> principles apply to more advanced test development. As you gain experience and
> your test suite(s) grow, taxonomy of test cases, the and the use/need for
> different kinds of tests will become more clear.

## Test Suites

Not all test cases are the same. In the following sections we will discuss many
kinds of tests, which serve different purposes and provide different benefits.
Tests should be divided up into different Suites, which can be run independently
of one another.

Tests which "Fail Fast" save both developer and compute time. Some tests are by
necessity very slow. [Unit Tests](#unit-tests) should run extremely quickly in
just a few seconds at most, while [end-to-end](#end-to-end-tests) require time
to set up and may depend on slow and unreliable external services. By organizing
tests into suites based on execution time, you can run fast suites first and
stop if an error is encountered before running slower suites.

### Advantages of Test Suites

- Developers can run relevant tests quickly and frequently.
- Tests can 'Fail Fast', while still reporting all failures within that suite.
- Test cases can be divided up conceptually, making them easier to read and
  reason about.
- We can avoid false positives, by not running tests we expect to fail due to
  external factors.

### Guidelines for Test Suites

- Organize test cases into suites based on the type of test and execution time.
- Set up test-runners (Make, shell scripts, CI/CD) to run fast suites first, and
  stop when a suite reports a failure.
- Use markers to enable developers to run the sub-sets of test which are most
  relevant to their work, with minimal time spent waiting.

### Creating Test Suites

The simplest way to start, is separating tests into directories inside of the
`tests/` directory:

```
tests/
    |- unit/
    |- integration/
    |- e2e/
```

These suites can be run directly with pytest `pytest tests/unit/`.

[Markers](https://docs.pytest.org/en/stable/example/markers.html) provide an
additional layer of organization, by labeling individual tests. This lets us
create specialized suites based on markers, independent of directory structure
or type of test. For example we can mark extremely slow or flakey tests that are
conceptually part of a larger suite, and skip them when needed.

First, define a new marker in `pyproject.toml`:

```toml
[tool.pytest]
markers = [
    "unit: marks unit tests",
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "online: tests which require internet access",
]
```

To mark an individual test, decorate the test case:

```python
import pytest


@pytest.mark.slow
def test_somthing_slow(): ...
```

To mark every test in a directory, add the following to the `conftest.py` in the
target folder:

```python
# tests/unit/conftest.py
import pytest


def pytest_collection_modifyitems(session, config, items):
    for item in items:
        item.add_marker(pytest.mark.unit)
```

## Project Level Integration Tests

The term "Integration Test" is unfortunately overloaded, and used to describe
testing that various components integrate with each other, at many levels of the
system. These tests will loosely follow the "Detroit School" of test design,
focusing on behavior, and the way components and dependencies interact.

- Write tests which view the code from an outside-in perspective, like
  [Public Interface](#public-interface-tests) tests
- Avoid Mocks/Fakes/Patches as much as possible
- Test that the components of your code all work together (inner-package
  integration)
- Test that your code works with its dependencies (dependency integration)

These tests can be a good place for more extensive edge-case and fuzzy input
testing. Which may include "private" functions/classes/attributes, which require
more extensive validation.

The intended audience for these tests is developers working on the project.

## Unit Tests

Unit tests loosely follow the "London School" of testing, where the smallest
unit of code is tested in isolation.

These tests are written from an internal perspective, so they are a good place
to test aspects of the codebase which are "private" (not directly exposed to
users), but which still need to be tested. Some examples of units are: a single
function, an attribute of an object, a method or property of a class.

They test only the code in the project, not code imported from other projects
(or even other modules within the same project).

### Advantages of unit testing

Unit tests ensure that the code, as written, is correct, and executes properly.
They communicate the intention of the creator of the code, how the code is
expected to behave, in its expected use-case.

Unit tests should be simple, isolated, and run very quickly. This allows us to
run them frequently, while we make changes to the code (even automatically, each
time we save a file for example) to ensure our changes did not break anything...
or only break what we expected to.

Writing unit tests can reveal weaknesses in our implementations, and lead us to
better design decisions:

- If the test requires excessive setup, the unit may be dependent on too many
  external variables.
- If the test requires many assertions, the unit may be doing too many things /
  have too many side-effects.
- If the unit is very difficult to test, it will likely be difficult to
  understand and maintain. Refactoring code to make it easier to test often
  leads us to write better code overall.

### When to write unit tests

- When your project matures enough to justify the work! Higher-level testing is
  often sufficient for small projects which are not part of critical
  infrastructure.

- When you identify a critical part of the code-base, or parts that are
  especially prone to breaking, use unit tests to ensure that code continues to
  behave as designed.

- When other projects start to depend heavily on your library, thorough unit
  testing helps ensure the reliability of your code for your users.

- When doing test-driven development, unit tests should be created after
  higher-level 'integration' or 'outside-in' test cases, before writing any code
  to make the tests pass.

Not all projects need full unit test coverage, some may not need unit tests at
all.

### Guidelines for unit testing

- Unit tests live alongside the code they test, in a /tests folder. They should
  be in a different directory than higher-level tests (integration, e2e,
  behavioral, etc) so that they can be run quickly before the full test suite,
  and to avoid confusing them with other types of tests.

- Test files should be named `test_{file under test}.py`, so that test runners
  can find them easily.

- `test_*.py` files should match your source files (file-under-test) one-to-one,
  and contain only tests for code in the file-under-test. The code in
  `mymodule/source.py` is tested by `mymodule/tests/test_source.py`.

- Keep it simple! If a test-case requires extra setup and external tools, It may
  be more appropriate as an external test, instead of in the unit tests

- Avoid the temptation to test edge-cases! Focus your unit tests on the
  "happy-path". The Unit test should describe the expected and officially
  supported usage of the code under test.

- Isolation: Test single units of code! A single function, or a single attribute
  or method on a class. If you have two units (classes, functions, class
  attributes) with deeply coupled behavior, it is better to test them
  individually using mocking and patching, instead of testing both in a single
  test. This makes refactoring easier, helps you understand the interactions
  between units, and will correctly tell you which part is failing if one
  breaks.

#### Importing in test files

Keep things local! Prefer to import only from the file-under-test when possible.
This helps keep the context of the unit tests focused on the file-under-test.

Consider what happens when code we rely on from other modules is refactored and
moved.

```python
# src/project/lib.py
from project.cursed_utils import MyClass


def func(my_class: MyClass): ...


# src/project/tests/test_lib.py
from project.lib import MyClass, func


def test_func():
    ret = func(MyClass())
    ...
```

If our test file imported `MyClass` directly from cursed_utils, but the
file-under-test was updated to import it from bettername, the test would fail on
import and need to be updated. The test case does not care where `MyClass` is
defined, or imported from, it only cares about the `MyClass` symbol that is used
in the source code that it is testing. This way, when unrelated code is
refactored, the test does not need to change at all.

```python
# src/project/lib.py
from project.bettername import MyClass


def func(my_class: MyClass): ...


# src/project/tests/test_lib.py
from project.lib import MyClass, func


def test_func():
    ret = func(MyClass())
    ...
```

Importing from other source files is a code smell (for unit tests), It indicates
that the test is not well isolated.

Prefer to import only the object that you actually use, not the entire library.

- This simplifies mocking/patching in unit tests.
- Makes using drop-in replacements simpler. Changing
  `from pandas import DataFrame` to `from polars import DataFrame` in your
  file-under-test, should result in all tests passing, with no other changes.

It is common practice to import and alias all of a library, such as
`import numpy as np`. However, as we develop our unit tests, this can cause
difficulty with mocking, and complicate refactoring.

To patch out `numpy.sum` in your test, you either need to patch the _global_
numpy module, which can have unintended side-effects, or specifically patch
numpy.sum within the module namespace, which can result in absurdly long
namespace paths, and logical breaks in the path when we transition from the
local module namespace into an imported dependency's namespace, like so:

```python
def test_func(mocker):
    mock_sum = mocker.patch(
        "project.lib.np.sum",
        autospec=True,
    )  # you'll need to patch the alias'd namespace
    ...
```

Consider the benefits of refactoring your imports like so:

```python
from numpy import sum as np_sum, Array as NpArray
```

now you simply need to patch the imported function in the context of the
file-under-test:

```python
def test_func(mocker):
    np_sum = mocker.patch("project.lib.np_sum", autospec=True)
    ...
```

Finally consider giving the imported symbols aliases that are meaningful to your
code, regardless of the module they are imported from:

```python
# from numpy import sum as numeric_sum
from bettermath import superfast_numeric_sum as numeric_sum

total = numeric_sum(some_numeric_values)
```

#### Running unit tests

We recommend using Pytest for running tests in your development environments. To
run unit tests in your source folder, from your package root, use
`pytest {path/to/source}`. To run tests from an installed package (outside of
your source repository), use `pytest --pyargs {package name}`.

You can set the default test path in `pyproject.toml`, see: [Configuring
pytest]({% link pages/guides/pytest.md %}#configuring-pytest)

We recommend configuring pytest to run ONLY your fastest, least demanding test
suite by default.

#### Mocking and Patching to Isolate the code under test

When the unit you are testing touches any external unit (usually something you
imported, or another unit that has its own tests), the external unit should be
Patched, replacing it with a Mock for the durration of the test. The unit test
will:

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

Consider what needs to be mocked, and the level of isolation your unit test
really needs.

- Anything imported into the module you are testing should probably be mocked.
- External units with side-effects, or which do a lot of computation should
  probably be mocked.

Excessive mocking is a code smell! Consider ways to refactor the code, so that
it needs fewer mocks, less setup, and fewer assertions in a single test case.
This frequently leads us to write more readable and maintainable code.

It is worth cultivating a deep understanding of how python's imports work. The
interactions between imports and patches can sometimes be surprising, and cause
us to write invalid tests... or worse, tests that pass when they should fail.
These are a few of the cases that cause the most confusion.

When patches and imports are both used in a test case, the patch only applies to
the specific context in which it is called, and does not override the import
used elsewhere in the test file. In the following example:

- You import `dangerous_sideffects` from project.lib, then patch
  `project.lib.dangerous_sideffects`. If your source code calls
  `dangerous_sideffects` (when you run `say_hello`) it will use the Mock
  provided by the patch. But if your test case calls `dangerous_sideffects`, it
  will not use the Mock, and instead will execute the function
- The behavior is the same when using stdlib.mock.patch, and pytest-mocker

```python
# project.lib
def dangerous_sideffects():
    raise RuntimeError("BOOM")


def say_hello():
    dangerous_sideffects()
    return "hello world"
```

```python
from project.lib import say_hello, dangerous_sideffects


def test_pytest(mocker):
    # Given this context
    mock_dangerous_sideffects = mocker.patch("project.lib.dangerous_sideffects")
    # When we run the code
    ret = say_hello()
    # Then we expect the result
    assert ret == "hello world"
    mock_dangerous_sideffects.assert_called_once()

    # But this will still raise an exception!
    dangerous_sideffects()
```

## Extensive Input Testing

The range of inputs that test cases validate is an important decision.

When the need for extensive testing starts to conflict with the readability of
test cases and their usefulness as documentation for users and other developers,
the tests should be re-organized into public-facing (concise, expressive, easily
readable), and technical (complex, extensive) test files.

- To maintain readability:
  - tests may need to include fewer inputs
  - extensive edgecase testing may be moved into different sections or files
  - the code itself may need to be refactored
- Avoid testing invalid input; the range of invalid input is infinite, and is
  the programming equivalent of trying to prove a negative.
- Focus on inputs relevant to the code under test, and avoid testing the code in
  dependencies. Some integration testing of specific behaviors your code relies
  on is justifiable.
- [Fuzz Tests](#fuzz-tests) are the best place to handle extensive and
  exhaustive input testing.

### In Public Interface Tests

These are the most appropriate place to test certain invalid inputs and
dependencies. Public Interface tests act like a contract with users; each
behavior that is tested is like a promise that users can rely on, and expect
that it will not change without warning (and probably a major version bump). So
any input/output and side-effects included in these tests should be considered
_officially supported behavior_ and given careful consideration.

### In project level integration tests

These are a good place to handle more extensive input testing. Integration tests
already tend to be more verbose, with a lot of setup and teardown, and much more
behavior to cover than other kinds of tests. These are the kinds of tests that
should focus on edgecases.

### In Unit Tests

Unit Tests should focus on the "happy-path" of execution. In most cases one
representative example of the _expected_ input is sufficient. The test case
should illustrate how the unit is expected to be used.

Invalid input should only be tested when the unit itself includes logic to
handle that invalid input.

for example, this code:

```python
def foo(x: int):
    return x + 1
```

should not test its behavior when passed a string (the type annotation already
covers that).

This code should be tested with a string, to cover the exception path.

```python
def bar(x):
    if type(x) is str:
        raise RuntimeError("invalid input")
    return x + 1
```

## Additional Types of Test Suites

A non-exhaustive discussion of some common types of tests.

Dont Panic!

Depending on your project, you may not need many, or most of these kinds of
tests.

### Behavioral, Feature, or Functional Tests

High-level tests, which ensure a specific feature works. These are placed in a
location like 'project_root/tests/behavioral/'. Used for testing things like:

- Loading a file works
- Setting a debug flag results in debug messages being printed
- A configuration option affects the behavior of the code as expected

### Fuzz Tests

Fuzz tests attempt to test the full range of possible inputs to a function. They
are good for finding edge-cases, where what should be valid input causes a
failure. [Hypothesis](https://hypothesis.readthedocs.io/en/latest/) is an
excellent tool for this, and a lot of fun to use.

- SLOW TESTS: fuzz tests can take a very long time to run, and should usually be
  placed in a test suite which is run separately from faster tests.
  [see: fail fast](https://en.wikipedia.org/wiki/Fail-fast_system)
- Reserve fuzz testing for the few critical functions, where it really matters.

### Integration Tests

The word "Integration" is a bit overloaded, and can refer to many levels of
interaction between your code, its dependencies, and external systems.

- Code level
  - Test the integration between your software and external / 3rd party
    dependencies.
  - Utilize the code imported from dependencies without mocking it.

- Environment level
  - Testing that your software works in the environments you plan to run it in.
    - Running inside of a docker container
    - Using GPU's or other specialized hardware
    - Deploying it to cloud servers

- System level
  - Testing that it interacts with other software in a larger system.
    - Interactions with other services, on local or cloud-based platforms
    - Micro-service, Database, or API connections and interactions

### End to End Tests

The slowest, and most brittle, of all tests. Here, you set up an entire
production-like system, and run tests against it. Some examples are:

- Create a Dev / Testing / Staging environment, and run tests against it to make
  sure everything works together
- Fake user input, using tools like
  [Selenium](https://www.selenium.dev/documentation/)
- Processing data from a pre-loaded test database
- Manual QA testing

### Fuzz Tests and other slow tests

Testing random input, using tools like Hypothesis, is similar to testing edge
cases, but running these tests can take a very long time, and they can often be
much more complex and difficult to read for new developers.

- Place them in their own test files, distinct from other edgecase tests.
- [mark them](https://docs.pytest.org/en/stable/how-to/mark.html) so that they
  can be run as a separate test suite, once all of the faster test suites have
  succeeded.
- These can take an arbitrarily long time to run, and you will need to set
  reasonable limits for your project.

## Diagnostic Tests

Diagnostic tests are used to verify the installation of a package. They should
be runable on production systems, like when we need to ssh into a live server to
troubleshoot problems.

A diagnostic test suite may contain any combination of tests you deem pertinent.
You could include all the unit tests, or a specific subset of them. You may want
to include some integration tests, and feature tests. Consider them Smoke Tests,
a select sub-set of tests meant to catch critical errors quickly, not to perform
a full system check of the package. Good diagnostic tests:

- Respect the user's environment!
  - Diagnostic tests should not require additional dependencies beyond what the
    package requires.
  - Do not create files, alter a database, or change the state of the system
- Run quickly: select tests that can be run in a few moments
- Provide meaningful feedback

### Advantages of Diagnostic Tests

- Diagnostic tests allow us to verify an installation of a package.
- They can be used to verify system-level dependencies like:
  - Compiled binary dependencies
  - Access to specific hardware, like GPUs

### Guidelines for Diagnostic Tests

- Consider using the stdlib `unittest.TestCase` and other stdlib tools instead
  of pytest. To allow running unit tests for diagnostics in production
  environments, without installing additional packages.

- Test files should be named `test_<file under test>.py`, so that stdlib
  unittest can find them easily.

### Mocking and Patching to Isolate the code under test

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

### Running Diagnostic Tests

stdlib's unittest can be used in environments where pytest is not available:

- To use unittest to run tests from an installed package (outside of your source
  repository), use `python -m unittest discover -s <module.name>`
- To use unittest to run tests in your source folder, from your package root,
  use
  `python -m unittest discover --start-folder <source folder> --top-level-directory .`
