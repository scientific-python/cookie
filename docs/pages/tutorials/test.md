---
layout: page
title: Test
permalink: /tutorials/test/
nav_order: 4
parent: Tutorials
---

In this section you will:

- Write a test to verify the correctness of the code.

# Test

You should add a test right away while the details are still fresh in mind.
Writing tests lets you make future improvements with confidence that
any unintended changes or breakage with not go unnoticed. Writing tests also
tends to encouraging you to write modular, reusable code, because it is easier
to test.

## Write some tests

Make a directory for tests. We recommend to put it next to the `src` directory.

```
mkdir tests
```

Make a file to put your first test in. The name of the file should begin with `test`.

```
touch tests/test_snell.py
```

Your package directory structure should now look like:

```bash
.
├── noxfile.py
├── pyproject.toml
├── src
│   └── package
│   │   ├── __init__.py
│   │   └── rescale.py
└── tests
    └── test_rescale.py
```

(You may also see some `__pycache__` directories, which contain compiled Python
bytecode that was generated when calling your package. You may ignore them.)

Write some example tests into `tests/test_snell.py`, such as the following.

```py
# contents of tests/test_snell.py

import numpy as np
from example.refraction import snell


def test_perpendicular():
    # For any indexes, a ray normal to the surface should not bend.
    # We'll try a couple different combinations of indexes....

    actual = snell(0, 2.00, 3.00)
    expected = 0
    assert actual == expected

    actual = snell(0, 3.00, 2.00)
    expected = 0
    assert actual == expected


def test_air_water():
    n_air, n_water = 1.00, 1.33
    actual = snell(np.pi/4, n_air, n_water)
    expected = 0.5605584137424605
    assert np.allclose(actual, expected)
```

Things to notice:

- It is sometime useful to put multiple assert statements in one test. You
  should make a separate test for each behavior that you are checking. When a
  monolithic, multi-step tests fails, it’s difficult to figure out why.
- When comparing floating-point numbers (as opposed to integers) you should not
  test for exact equality. Use `numpy.allclose()`, which checks for equality
  within a (configurable) tolerance. NumPy provides several testing utilities,
  which should always be used when testing NumPy arrays.
- The names of all test modules and functions must begin with `test`.
  (Otherwise, they will not be picked up by the automatic test-running we will
  be using below.)

## Run the tests

Scientific Python packages generally use a program called `pytest` to run
their tests and report successes and failures. Install `pytest`.

```bash
pip install pytest
```

Run `pytest`

```bash
pytest
```

This walks through all the directories and files in our package that start with
the word `test` and collects all the functions whose name also starts with
`test`. `pytest` runs each function. If no exceptions are raised, the test
passes.

The output should look something like this:

```bash
======================================== test session starts ========================================
platform darwin -- Python 3.6.4, pytest-3.6.2, py-1.5.4, pluggy-0.6.0
benchmark: 3.1.1 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
rootdir: /private/tmp/test11/example, inifile:
plugins: pep8-1.0.6, lazy-fixture-0.3.0, forked-0.2, benchmark-3.1.1
collected 1 item

example/tests/test_snell.py ..                                                                 [100%]

===================================== 2 passed in 0.02 seconds ======================================
```

The output of `pytest` is customizable. Commonly useful command-line
arguments include:

- `-v` verbose
- `-s` Display output to stdout/stderr (e.g. output of `print`). By default, it is hidden.
- `-k EXPRESSION` Filter tests by pattern-matching test name.
- `--lf` Run only tests that failed on the previous run.

Consult the [pytest documentation][] for more.

[pytest documentation]: https://docs.pytest.org/en/latest/
