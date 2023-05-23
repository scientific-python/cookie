# example/tests/test_examples.py

import numpy as np
from ..refraction import snell
# (The above is equivalent to `from example.refraction import snell`.
# Read on for why.)


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
