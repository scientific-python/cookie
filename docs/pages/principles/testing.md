## Unit Tests

### Advantages of unit testing:

- Unit tests ensure that the code, as written, is correct, and executes
  properly.
- They communicate the intention of the creator of the code, how the code is
  expected to behave, in its expected use-case.

- Writing unit tests can reveal weakensses in our implementations, and lead us
  to better design decisions:
  - If the test requires excessive setup, the unit may be dependent on too many
    external variables.
  - If the test requires many assertions, the unit may be doing too many things
    / have too many side-effects.
  - If the unit is very difficult to test, it will likely be difficult to
    understand and maintain. Refactoring code to make it easier to test often
    leads us to write better code overall.

### Guidelines for unit testing:

- Unit tests live alongside the code they test, in a /tests folder.
  - It looks like `unittest discover` cannot find TestCase classes within source
    files.

- Test files should be named `test_{{file under test}}.py`, so that stdlib
  unittest can find them easily.

- test\_.py files should match your source files (file-under-test) one-to-one,
  and contain only tests for code in the file-file-under test.

- Consider using the stdlib `unittest.TestCase` and other stdlib tools instead
  of pytest.
  - Allows running unit tests for diagnostics in production environments,
    without installing additional packages.

- Keep it simple! If a test-case requires extra setup and external tools, It may
  be more appropriate as an external test, instead of in the unit tests

- Test single units of code! A single Function, or a single attribute or method
  on a class. Not the interactions between them. (see mocking and patching)

#### Importing in test files:

- Use relative imports, from the file under test:

  ```
  from ..file_under_test import MyClass
  ```

  - This ensures that the test file always imports from its source file, and
    does not accidentally import from an installed module.

- Only import from the file-under-test, unless absolutely necessary:
  - If your source runs `from pandas import DataFrame` and you need a DataFrame
    for a test, import it `from ..file_under_test import DataFrame` NOT
    `from pandas import DataFrame` in the test file.
    - This has some important implications for mocking/patching to elaborate on.

#### Running unit tests:

- Pytest is great for running tests in your development environments!
  `pytest {{path/to/source}}`
- stdlib's unittest can be used in environments where pytest is not available:
  - To use unittest to run tests in your source folder, from your package root,
    use
    `python -m unittest discover --start-folder {{source folder}} --top-level-directory .`
  - To use unittest to run tests from an installed package (outside of your
    source repository), use `python -m unittest discover -s {{module.name}}`

#### Mocking and Patching to Isolate the code under test:

- When the unit you are testing touches any external unit (usually something you
  imported, or another unit that has its own tests), the external unit should be
  Patched, replacing it with a Mock for the durration of the test.

- Verify that the external unit is called with the expected input
- Verify that any value returned from the external unit is utilized as expected.

  ```
  @patch(f'{SRC}.otherfunction', autospec=true)
  def test_myfunction(t, external_unit: Mock):
      ret = myfunction()
      external_unit.assert_called_with('input from myfunction')
      t.assertIs(ret, external_unit.return_value)

  ```

- Consider what needs to be mocked, and the level of isolation your unit test
  really needs.
  - Anything imported into the module you are testing should probably be mocked.
  - external units with side-effects, or which do a lot of computation should
    probably be mocked.
  - Some people prefer to never test `_private` attributes.
