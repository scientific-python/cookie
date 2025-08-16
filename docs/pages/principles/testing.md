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
[Public Interface tests](#user-interface-or-public-api-testing), which test your
code from the perspective of your users, focusing on the behavior of the public
interface and the Features that your project provides. Then we will cover
[Package Level Integration tests](#package-level-integration-tests), which test
that the various parts of your package work together, and work with the other
packages it depends on. Finally we will cover the venrable
[Unit Test](#unit-tests), which test the correctness of your code from a
perspective internal to your codebase, tests individual units in isolation, and
are optimized to run quickly and often.

These 3 test suites will cover the bulk of your testing needs and help get your
project to a reliable and maintainable state. We will also discuss some more
specialized and advanced types of test cases in our
[Taxonomy of Test Cases](#a-brief-taxonomy-of-test-suites) section.

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

## User Interface and Public API testing

A good place to start writing tests is from the perspective of a user of your
module or library, as described in the [Test
Tutorial]({% link pages/tutorials/test.md %}), and [Testing with pytest
guide]({% link pages/guides/pytest.md %}).

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

## Project Level Integration Testing

The term "Integration Test" is unfortunately overloaded, and used to describe
testing that various components integrate with each other, at many levels of the
system. These tests will loosely follow the "Detroit School" of test design.

- Write tests which view the code from an outside-in perspective, like
  [Public Interface]() tests
- Avoid Mocks/Fakes/Patches as much as possible
- Test that the components of your code all work together (inner-package
  integration)
- Test that your code works with its dependencies (dependency integration)

These tests can be a good place for more extensive edge-case, and fuzzy input
testing.

The intended audience for these tests developers working on the project, or
debugging issues they encounter as opposed to Public Interface tests, which
should be helpful for users of the package.

## Unit Tests

Unit tests loosely follow the "London School" of testing, where the smallest
unit of code is tested in isolation.

These tests are written from an internal perspective, so they are a good place
to test aspects of the codebase which are "private" not directly exposed to
users, but which still need to be tested. Some examples of units are: A single
function, an attribute of an object, a method or property of a class.

### Advantages of unit testing

Unit tests ensure that the code, as written, is correct, and executes properly.
They communicate the intention of the creator of the code, how the code is
expected to behave, in its expected use-case.

Unit tests should be simple, isolated, and run very quickly. This allows us to
run them quickly, while we make changes to the code (even automatically, each
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

Unit tests are considered "low level", and used for [Isolation Testing](). Not
all projects need full unit test coverage, some may not need unit tests at all.

- When your project matures enough to justify the work! Higher-level testing is
  often sufficient for small projects which are not part of critical
  infrastructure.

- When you identify a critical part of the code-base, or parts that are
  especially prone to breaking, use unit tests to ensure that code continues to
  behave as designed.

- When other projects start to depend heavily on your library, thorough unit
  testing helps ensure the reliability of your code for your users.

- When doing test-driven development, unit tests should be created after
  higher-level 'integration' or 'outside-in' test cases, before writing the code
  to make the tests pass.

### Guidelines for unit testing

- Unit tests live alongside the code they test, in a /tests folder. They should
  be in a different directory than higher-level tests (integration, e2e,
  behavioral, etc) so that they can be run quickly before the full test suite,
  and to avoid confusing them with other types of tests.

- Test files should be named `test_{{file under test}}.py`, so that test runners
  can find them easily.

- test\_.py files should match your source files (file-under-test) one-to-one,
  and contain only tests for code in the file-under test. The code in
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

#### Running unit tests

- Pytest is great for running tests in your development environments!
- to run unit tests in your source folder, from your package root, use
  `pytest {{path/to/source}}`
- To run tests from an installed package (outside of your source repository),
  use `pytest --pyargs {package name}}`

#### Mocking and Patching to Isolate the code under test

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

It is worth cultivating a deep understanding of how python's imports work. The
interactions between imports and patches can sometimes be surprising, and cause
us to write invalid tests... or worse, tests that pass when they should fail.
These are a few of the cases that cause the most confusion.

- When patches and imports are both used in a test case, the patch only applies
  to the specific context in which it is called, and does not override the
  import used elsewhere in the test file.
  - You import `say_hello` from your file-under-test, then patch
    `src.lib.say_hello`. If your source code calls `say_hello` it will use the
    Mock provided by the patch. But if your test case calls `say_hello`, it will
    not use the Mock, and instead will execute the function
  - The behavior is the same when using stdlib.mock.patch, and pytest-mocker

```python
# src.lib
def dangerous_sideffects():
    raise RuntimeError("BOOM")


def say_hello():
    dangerous_sideffects()
    return "hello world"
```

```python
from src.lib import say_hello, dangerous_sideffects


def test_pytest(mocker):
    # Given this context
    mock_say_hello = mocker.patch("src.lib.dangerous_sideffects")
    # When we run the code
    ret = say_hello()
    # Then we expect the result
    assert ret == "hello world"
    mock_dangerous_sideffects.assert_called_once()

    # But this will still raise an exception!
    dangerous_sideffects()
```

## A Brief Taxonomy of Test Suites

A non-exhaustive discussion of some common types of tests.

^_^ Dont Panic ^_^

Depending on your project, you may not need many, or most of these kinds of
tests.

- A library project probably does not need to test integration with
  microservices.
- A library with no 3rd party dependencies, does not need test them.
- Fuzz testing is for critical code, that many users rely on.

### Behavioral, Feature, or Functional Tests

High-level tests, which ensure a specific feature works. Used for testing things
like:

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
  - Low-level testing of your code-base, where you run the code imported from
    dependencies without mocking it.

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
production-like system, and run tests against it.

- Create a Dev / Testing / Staging environment, and run tests against it to make
  sure everything works together
- Fake user input, using tools like
  [Selenium](https://www.selenium.dev/documentation/)
- Processing data from a pre-loaded test database
- Manual QA testing

## Testing Edgecases

While writing unit tests, you may be tempted to test edgecases. You may have a
critical private function or algorithm, which is not part of the public API, so
not a good candidate for External tesing, and you are concerned about many
edgecases that you want to defend against using tests.

It is perfectly valid to write extensive edgecase testing for private code, but
these tests should be kept separate from the unit test suite. Extensive edgecase
testing makes tests long, and difficult to read (tests are documentation). They
can slow down execution, we want unit tests to run first, fast, and often.

- Place them in separate files from unit tests, to improve readability
- [mark them](https://docs.pytest.org/en/stable/how-to/mark.html) so that they
  can be run as a separate test suite, after your unit test pass

### Fuzz Tests and other slow tests

Testing random input, using tools like Hypothesis, is similar to testing edge
cases, but running these tests can take a very long time, and they can often be
much more complex and difficult to read for new developers.

- Place them in their own test files
- [mark them](https://docs.pytest.org/en/stable/how-to/mark.html) so that they
  can be run as a separate test suite, once all of the faster test suites have
  succeeded.

## Diagnostic Tests

Diagnostic tests are used to verify the installation of a package. They should
be runable on production systems, like when we need to ssh into a live server to
troubleshoot problems.

A diagnostic test suite may contain any combination of tests you deem pertinent.
You could include all the unit tests, or a specific subset of them. You may want
to include some integration tests, and feature tests. Consider them Smoke Tests,
a select sub-set of tests, meant to catch critical errors quickly, not perform a
full system check of the package.

- Respect the user's environment!
  - Diagnostic tests should not require additional dependencies beyond what the
    package requires.
  - Do not create files, alter a database, or change the state of the system
- Run quickly, select tests that can be run in a few moments
- provide meaningful feedback

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
  repository), use `python -m unittest discover -s {{module.name}}`
- To use unittest to run tests in your source folder, from your package root,
  use
  `python -m unittest discover --start-folder {{source folder}} --top-level-directory .`
