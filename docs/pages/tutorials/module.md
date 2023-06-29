---
layout: page
title: Inline documentation
permalink: /tutorials/module/
nav_order: 2
parent: Tutorials
---

{% include toc.html %}

# Inline documentation

In this section you will:

- Place some code in a module.
- Provide inline documentation (a "docstring").

## Module

As a concrete example, let's suppose we have a simple function that encodes
[Snell's Law][]. Perhaps this function currently lives in a Jupyter notebook or
a `.py` file in an email attachment. We want to put into some more lasting,
maintainable, reusable, and/or shareable form.

Here is the code:

```py
# contents of refraction.py

import numpy as np


def snell(theta_inc: float, n1: float, n2: float) -> float:
    """
    Compute the refraction angle using Snell's Law.

    See https://en.wikipedia.org/wiki/Snell%27s_law

    Parameters
    ----------
    theta_inc : float
        Incident angle in radians.
    n1, n2 : float
        The refractive index of medium of origin and destination medium.

    Returns
    -------
    theta : float
        refraction angle

    Examples
    --------
    A ray enters an air--water boundary at pi/4 radians (45 degrees).
    Compute exit angle.

    >>> snell(np.pi/4, 1.00, 1.33)
    0.5605584137424605
    """
    return np.arcsin(n1 / n2 * np.sin(theta_inc))
```

Notice that this example includes inline documentation --- a "docstring". This
is extremely useful for collaborators, and the most common collaborator is
Future You! It also includes type hints; this tells a programmer, type checker,
or IDE what types are expected in an out of the function.

Further, by following the [numpydoc standard][], we will be able to
automatically generate nice-looking HTML documentation later. Notable features:

- At the top, there is a succinct, one-line summary of the function's purpose.
  It must one line.

- (Optional) There is an paragraph elaborating on that summary.

- There is a section listing input parameters, with the structure

  ```
  parameter_name : parameter_type
      optional description
  ```

  Note that space before the `:`. That is part of the standard.

- Similar parameters may be combined into one entry for brevity's sake, as we
  have done for `n1, n2` here.

- There is a section describing what the function returns.

- (Optional) There is a section of one or more examples.

We will revisit docstrings in the section on writing documentation [TODO: link
once this section exists].

[snell's law]: https://en.wikipedia.org/wiki/Snell%27s_law
[numpydoc standard]: https://numpydoc.readthedocs.io/en/latest/format.html
