===============
The Code Itself
===============

In this section you will:

* Put some scientific code in your new Python package.
* Update your package's list of dependencies in ``requirements.txt``.
* Write a test and run the test suite.
* Use a "linter" and style-checker.
* Commit your changes to git and sync your changes with GitHub.

A simple function with inline documentation
-------------------------------------------

Let's write a simple function that encodes
`Snell's Law <https://en.wikipedia.org/wiki/Snell%27s_law>`_ and include it in
our Python package.

Look again at the directory structure.

.. code-block:: none

   example/
   ├── .flake8
   ├── .gitattributes
   ├── .gitignore
   ├── .travis.yml
   ├── AUTHORS.rst
   ├── CONTRIBUTING.rst
   ├── LICENSE
   ├── MANIFEST.in
   ├── README.rst
   ├── docs
   │   ├── Makefile
   │   ├── build
   │   ├── make.bat
   │   └── source
   │       ├── _static
   │       │   └── .placeholder
   │       ├── _templates
   │       ├── conf.py
   │       ├── index.rst
   │       ├── installation.rst
   │       ├── release-history.rst
   │       └── usage.rst
   ├── example
   │   ├── __init__.py
   │   ├── _version.py
   │   └── tests
   │       └── test_examples.py
   ├── requirements-dev.txt
   ├── requirements.txt
   ├── setup.cfg
   ├── setup.py
   └── versioneer.py

Our scientific code should go in the ``example/`` subdirectory, next to
``__init__.py``. Let's make a new file in that directory named
``refraction.py``, meaning our new layout will be:

.. code-block:: none

   ├── example
   │   ├── __init__.py
   │   ├── _version.py
   │   ├── refraction.py
   │   └── tests
   │       └── test_examples.py

This is our new file. You may follow along exactly or, instead, make a file
with a different name and your own scientific function.

.. literalinclude:: refraction.py

Notice that this example includes inline documentation --- a "docstring". This
is extremely useful for collaborators, and the most common collaborator is
Future You!

Further, by following the
`numpydoc standard <https://numpydoc.readthedocs.io/en/latest/format.html>`_,
we will be able to automatically generate nice-looking HTML documentation
later. Notable features:

* There is a succinct, one-line summary of the function's purpose. It must one
  line.
* (Optional) There is an paragraph elaborating on that summary.
* There is a section listing input parameters, with the structure

  .. code-block :: none

     parameter_name : parameter_type
         optional description

  Note that space before the ``:``. That is part of the standard.
* Similar parameters may be combined into one entry for brevity's sake, as we
  have done for ``n1, n2`` here.
* There is a section describing what the function returns.
* (Optional) There is a section of one or more examples.

We will revisit docstrings in the section on :doc:`writing-docs`.

Update Requirements
-------------------

Notice that our package has a third-party dependency, numpy. We should
update our package's ``requirements.txt``.

.. code-block:: text

   # requirements.txt

   # List required packages in this file, one per line.
   numpy

Our cookiecutter configured ``setup.py`` to read this file. It will ensure that
numpy is installed when our package is installed.

We can test it by reinstalling the package.

.. code-block:: bash

   python3 -m pip install -e .

Try it
------

Try importing and using the function.


.. code-block:: python

    >>> from example.refraction import snell
    >>> import numpy as np
    >>> snell(np.pi/4, 1.00, 1.33)
    1.2239576240104186

The docstring can be viewed with :func:`help`.

.. code-block:: python

    >>> help(snell)

Or, as a shortcut, use ``?`` in IPython/Jupyter.

.. ipython:: python
   :verbatim:

   snell?

Run the Tests
-------------

You should add a test right away while the details are still fresh in mind.
Writing tests encourages you to write modular, reusable code, which is easier
to test.

The cookiecutter template included an example test suite with one test:

.. code-block:: python

   # example/tests/test_examples.py

   def test_one_plus_one_is_two():
       assert 1 + 1 == 2

Before writing our own test, let's practice running that test to check that
everything is working.

.. important::

   We assume you have installed the "development requirements," as covered
   in :doc:`preliminaries`. If you are not sure whether you have, there is no
   harm in running this a second time:

   .. code-block:: bash

      python3 -m pip install --upgrade -r requirements-dev.txt

.. code-block:: bash

   python3 -m pytest

This walks through all the directories and files in our package that start with
the word 'test' and collects all the functions whose name also starts with
``test``. Currently, there is just one, ``test_one_plus_one_is_two``.
``pytest`` runs that function. If no exceptions are raised, the test passes.

The output should look something like this:

.. code-block:: bash

   ======================================== test session starts ========================================
   platform darwin -- Python 3.6.4, pytest-3.6.2, py-1.5.4, pluggy-0.6.0
   benchmark: 3.1.1 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
   rootdir: /private/tmp/test11/example, inifile:
   plugins: xdist-1.22.2, timeout-1.2.1, rerunfailures-4.0, pep8-1.0.6, lazy-fixture-0.3.0, forked-0.2, benchmark-3.1.1
   collected 1 item

   example/tests/test_examples.py .                                                              [100%]

   ===================================== 1 passed in 0.02 seconds ======================================

.. note:: 

   The output of ``pytest`` is customizable. Commonly useful command-line
   arguments include:

   * ``-v`` verbose
   * ``-s`` Do not capture stdout/err per test.
   * ``-k EXPRESSION`` Filter tests by pattern-matching test name.

   Consult the `pytest documentation <https://docs.pytest.org/en/latest/>`_
   for more.

Write a Test
------------

Let's add a test to ``test_examples.py`` that exercises our ``snell`` function.
We can delete ``test_one_plus_one_is_two`` now.

.. literalinclude:: test_examples.py

Things to notice:

* It is sometime useful to put multiple ``assert`` statements in one test. You
  should make a separate test for each *behavior* that you are checking. When a
  monolithic, multi-step tests fails, it's difficult to figure out why.
* When comparing floating-point numbers (as opposed to integers) you should not
  test for exact equality. Use :func:`numpy.allclose`, which checks for
  equality within a (configurable) tolerance. Numpy provides several
  `testing utilities <https://docs.scipy.org/doc/numpy-1.13.0/reference/routines.testing.html>`_,
  which should always be used when testing numpy arrays.
* Remember that the names of all test modules and functions must begin with
  ``test`` or they will not be picked up by pytest!

See :doc:`advanced-testing` for more.

"Lint": Check for suspicious-looking code
-----------------------------------------

A `linter <https://en.wikipedia.org/wiki/Lint_(software)>`_ is a tool that
analyzes code to flag potential errors. For example, it can catch variables you
defined by never used, which is likely a spelling error.

The cookiecutter configured ``flake8`` for this purpose. Flake8 checks for
"lint" and also enforces the standard Python coding style,
`PEP8 <https://www.python.org/dev/peps/pep-0008/?#introduction>`_. Enforcing
consistent style helps projects stay easy to read and maintain as they grow.
While not all projects strictly enfore PEP8, we generally recommend it.

.. important::

   We assume you have installed the "development requirements," as covered
   in :doc:`preliminaries`. If you are not sure whether you have, there is no
   harm in running this a second time:

   .. code-block:: bash

      python3 -m pip install --upgrade -r requirements-dev.txt

.. code-block:: bash

    python3 -m flake8

This will list linting or stylistic errors. If there is no output, all is well.
See the `flake8 documentation <http://flake8.pycqa.org/en/latest/>`_ for more.

Commit and Push Changes
-----------------------

Remember to commit your changes to version control and push them up to GitHub.

.. important::

   The following is a quick reference that makes some assumptions about your
   local configuration and workflow.

   This usage is part of a workflow named *GitHub flow*. See
   `this guide <https://guides.github.com/introduction/flow/>`_ for more.

Remember that at any time you may use ``git status`` to check which branch
you are currently on and which files have uncommitted changes. Use ``git diff``
to review the content of those changes.

1. If you have not already done so, create a new "feature branch" for this work
   with some descriptive name.

   .. code-block:: bash

      git checkout master  # Starting from the master branch...
      git checkout -b add-snell-function  # ...make a new branch.

2. Stage changes to be committed. In our example, we have created one new file
   and changed an existing one. We ``git add`` both.

   .. code-block:: bash

      git add example/refraction.py
      git add example/tests/test_examples.py

3. Commit changes.

   .. code-block:: bash

      git commit -m "Add snell function and tests."

4. Push changes to remote repository on GitHub.

   .. code-block:: bash

      git push origin add-snell-function

5. Repeat steps 2-4 until you are happy with this feature.

6. Create a Pull Request --- or merge to master.

   When you are ready for collaborators to review your work and consider merging
   the ``add-snell-function`` branch into the ``master`` branch,
   `create a pull request <https://help.github.com/articles/creating-a-pull-request>`_.
   Even if you presently have no collaborators, going through this process is a
   useful way to document the history of changes to the project for any *future*
   collaborators (and Future You).

   However, if you are in the early stages of just getting a project up and you
   are the only developer, you might skip the pull request step and merge the
   changes yourself.

   .. code-block:: bash

      git checkout master
      # Ensure local master branch is up to date with remote master branch.
      git pull --ff-only origin master
      # Merge the commits from add-snell-function into master.
      git merge add-snell-function
      # Update the remote master branch.
      git push origin master

Multiple modules
----------------

We created just one module, ``example.refraction``. We might eventually grow a
second module --- say, ``example.utils``. Some brief advice:

* When in doubt, resist the temptation to grow deep taxonomies of modules and
  sub-packages, lest it become difficult for users and collaborators to
  remember where everything is. The Python built-in libraries are generally
  flat.

* When making intra-package imports, we recommend relative imports.

  This works:

  .. code-block:: bash

     # example/refraction.py

     from example import utils
     from example.utils import some_function

  but this is equivalent, and preferred:

  .. code-block:: bash

     # example/refraction.py

     from . import utils
     from .utils import some_function

  For one thing, if you change the name of the package in the future, you won't
  need to update this file.

* Take care to avoid circular imports, wherein two modules each import the
  other.
