=====================
Writing Documentation
=====================

In this section you will:

* Generate HTML documentation using Sphinx, starting from a working example
  provided by the cookiecutter template.
* Edit ``usage.rst`` to add API documentation and narrative documentation.
* Learn how to incorporate code examples, IPython examples, matplotlib plots,
  and typeset math.

Build the docs
--------------

Almost all scientific Python projects use the
`Sphinx documentation generator <http://www.sphinx-doc.org/>`_.
The cookiecutter template provided a working example with some popular
extensions installed and some sample pages.

.. code-block:: none

      example/
      (...)
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
      (...)

The ``.rst`` files are source code for our documentation. To build HTML pages
from this source, run:

.. code-block:: bash

   make -C docs html

You should see some log message ending in ``build succeeded.``

This output HTML will be located in ``docs/build/html``. In your Internet
browser, open ``file://.../docs/build/html/index.html``, where ``...`` is the
path to your project directory. If you aren't sure sure where that is, type
``pwd``.

Update the docs
---------------

The source code for the documentation is located in ``docs/source/``.
Sphinx uses a markup language called ReStructured Text (.rst). We refer you to
`this primer <http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`_
to learn how to denote headings, links, lists, cross-references, etc.

Sphinx formatting is sensitive to whitespace and generally quite picky. We
recommend running ``make -C docs html`` often to check that the documentation
builds successfully. Remember to commit your changes to git periodically.

Good documentation includes both:

* API (Application Programming Interface) documentation, listing every public
  object in the library and its usage
* Narrative documentation interleaving prose and code examples to explain how
  and why a library is meant to be used

API Documentation
-----------------

Most the work of writing good API documentation goes into writing good,
accurate docstrings. Sphinx can scrape that content and generate HTML from it.
Again, most scientific Python libraries use the
`numpydoc standard <https://numpydoc.readthedocs.io/en/latest/format.html>`_,
which looks like this:

.. literalinclude:: refraction.py

Autodoc
^^^^^^^

In an rst file, such as ``docs/source/usage.rst``, we can write:

.. code-block:: rst

   .. autofunction:: example.refraction.snell

which renders in HTML like so:

.. autofunction:: example.refraction.snell
   :noindex:

From here we refer you to the
`sphinx autodoc documentation <http://www.sphinx-doc.org/en/stable/ext/autodoc.html>`_.

Autosummary
^^^^^^^^^^^

If you have many related objects to document, it may be better to display them
in a table. Each row will include the name, the signature (optional), and the
one-line description from the docstring.

In rst we can write:

.. code-block:: rst

   .. autosummary::
      :toctree: generated/
   
      example.refraction.snell

which renders in HTML like so:

.. autosummary::
   :toctree: generated/

   example.refraction.snell

It links to the full rendered docstring on a separate page that is
automatically generated.

From here we refer you to the
`sphinx autosummary documentation <http://www.sphinx-doc.org/en/stable/ext/autosummary.html>`_.

Narrative Documentation
-----------------------

Code Blocks
^^^^^^^^^^^

Code blocks can be interspersed with narrative text like this:

.. code-block:: rst

   Scientific libraries conventionally use radians. Numpy provides convenience
   functions for converting between radians and degrees.

   .. code-block:: python

      import numpy as np
    
    
      np.deg2rad(90)  # pi / 2
      np.rad2deg(np.pi / 2)  # 90.0

which renders in HTML as:

Scientific libraries conventionally use radians. Numpy provides convenience
functions for converting between radians and degrees.

.. code-block:: python

    import numpy as np


    np.deg2rad(90)  # pi / 2
    np.rad2deg(np.pi / 2)  # 90.0

To render short code expressions inline, surround them with back-ticks. This:

.. code-block:: rst

    Try ``snell(0, 1, 1.33)``.

renders in HTML as:


Try ``snell(0, 1, 1.33)``.

Embedded Scripts
^^^^^^^^^^^^^^^^

For lengthy examples with tens of lines or more, it can be convenient to embed
the content of a .py file rather than writing it directly into the
documentation.

This can be done using the directive

.. code-block:: rest

   .. literalinclude:: examples/some_example.py

where the path is given relative to the current file's path. Thus, relative to
the repository's root directory, the path to this example script would be
``docs/source/examples/some_example.py``.

From here we refer you to the
`sphinx code example documentation <http://www.sphinx-doc.org/en/stable/markup/code.html>`_.

To go beyond embedded scripts to a more richly-featured example gallery that
shows scripts and their outputs, we encourage you to look at
`sphinx-gallery <https://sphinx-gallery.github.io/>`_.

IPython Examples
^^^^^^^^^^^^^^^^

IPython's sphinx extension, which is included by the cookiecutter template,
makes it possible to execute example code and capture its output when the
documentation is built. This rst code:

.. code-block:: rst

   .. ipython:: python

      1 + 1

renders in HTML as:

.. ipython:: python

    1 + 1

From here we refer you to the
`IPython sphinx directive documentation <https://ipython.org/ipython-doc/rel-0.13.2/development/ipython_directive.html>`_.

Plots
^^^^^

Matplotlib's sphinx extension, which is included by the cookiecutter template,
makes it possible to display matplotlib figures in line. This rst code:

.. code-block:: rst

   .. plot::
    
      import matplotlib.pyplot as plt
      fig, ax = plt.subplots()
      ax.plot([1, 1, 2, 3, 5, 8])

renders in HTML as:

.. plot::

    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    ax.plot([1, 1, 2, 3, 5, 8])
    
From here we refer you to the
`matplotlib plot directive documentation <https://matplotlib.org/devel/plot_directive.html>`_.

Math (LaTeX)
^^^^^^^^^^^^

Sphinx can render LaTeX typeset math in the browser (using
`MathJax <https://www.mathjax.org/>`_). This rst code:

.. code-block:: rst

   .. math::

       \int_0^a x\,dx = \frac{1}{2}a^2

renders in HTML as:

.. math::

    \int_0^a x\,dx = \frac{1}{2}a^2

This notation can also be used in docstrings. For example, we could add
the equation of Snell's Law to the docstring of
:func:`~example.refraction.snell`.

Math can also be written inline. This rst code:

.. code-block:: rst

   The value of :math:`\pi` is 3.141592653....

renders in HTML as:

   The value of :math:`\pi` is 3.141592653....

Referencing Documented Objects
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can create links to documented functions like so:

.. code-block:: rst

   The :func:`example.refraction.snell` function encodes Snell's Law.

The :func:`example.refraction.snell` function encodes Snell's Law.

Adding a ``~`` omits the module path from the link text.

.. code-block:: rst

   The :func:`~example.refraction.snell` function encodes Snell's Law.

The :func:`~example.refraction.snell` function encodes Snell's Law.

See `the Sphinx documentation <http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`_ for more.
