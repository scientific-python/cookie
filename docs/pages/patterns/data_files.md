---
layout: page
title: Including data files
permalink: /patterns/data-files/
nav_order: 3
parent: Patterns
---

{% include toc.html %}

# Including data files

In this section you will:

- Understand the importance of keeping large files out of your package.
- Learn some alternative approaches.
- Learn how to include small data files in your package.

## Consider Alternatives

**Never include large binary files in your Python package or git repository.**
Once committed, the file lives in git history forever. Git will become sluggish,
because it is not designed to operate on large binary files, and your package
will become an annoyingly large download.

Removing accidentally-committed files after the fact is _possible_ but
destructive, so it's important to avoid committing large files in the first
place.

Alternatives:

- Can you generate the file using code instead? This is a good approach for test
  data: generate the test data files as part of the test. Of course it's
  important to test against _real_ data from time to time, but for automated
  tests, simulated data is just fine. If you don't understand your data well
  enough to simulate it accurately, you don't know enough to write useful tests
  against it.
- Can you write a Python function that fetches the data on demand from some
  public URL? This is the approach used by projects such as scikit-learn that
  need to download large datasets for their examples and tests.

If you use one these alternatives, add the names of the generated or downloaded
files to the project's `.gitignore` file, which is provided by the
[copier][]/[cookiecutter][] template. This helps protect you against
accidentally committing the file to git.

If the file in question is a text file and not very large (\< 100 kB) than it's
reasonable to just bundle it with the package. If not, see the recommendation at
the end.

## How to Package Data Files

What's the problem we are solving here? If your Python program needs to access a
data file, the naïve solution is just to hard-code the path to that file.

```python
from pathlib import Path

spacings_txt = Path("peak_spacings/LaB6.txt").read_text(encoding="utf=8")
```

But this is not a good solution because:

- The data file won't be included in the distribution: users who `pip install`
  your package will find it's missing!
- The path to the data file depends on the platform and on how the package is
  installed. We need Python to handle those details for us.
- Your package might not even be installed on a file system, it might be in a
  zip file or database.

As an example, suppose we have text files with Bragg peak spacings of various
crystalline structures, and we want to use these files in our Python package.
Let's put them in a new directory in our package, such as
`src/package/peak_spacings/`.

```text
# src/package/peak_spacings/LaB6.txt

4.15772
2.94676
2.40116
```

```text
# src/package/peak_spacings/Si.txt

3.13556044
1.92013079
1.63749304
1.04518681
```

To make these available to the Python loading mechanism, the easiest way is to
add an `__init__.py` in `src/package/peak_spacing`. This can be an empty file;
it's purpose is to tell Python that this can be loaded.

You'll want to make sure your Python building backend is placing these files in
the SDist and wheel. If you are using anything other than setuptools, this
should be automatic.

{% details Setuptools-specific instructions %}

There are two ways to include data files in setuptools. You can either list the
package data explicitly:

```ini
# setup.cfg
[options.package_data]
package.peak_spacings =
    *.txt
```

**Or**, you can use automatic data inclusion (this is the default if you use
`pyproject.toml` `[project]` config in Setuptools 61+):

```ini
[options]
include_package_data = True
```

But then you'll need to _also_ make sure the files are in the SDist, too:

```text
# MANIFEST.in
include src/package/peak_spacings/*.txt
```

{% enddetails %}

Finally, wherever we actually use the files in our scientific code, we can
access them using `importlib_resources`. For users with Python >= 3.9 the
standard library `importlib.resources` module can be used directly instead of
relying on `importlib_resources`.

```python
# from importlib import resources   # Python >= 3.9 only
import importlib_resources as resources


ref = resources.files("package.peak_spacings") / "LaB6.txt"

spacings_txt = ref.read_text(encoding="utf=8")

# If you have an API that requires an on-disk file, you can do this instead:
with resources.as_file(ref) as path:
    # Now path is guaranteed to live somewhere on disk
    with path.open(encoding="utf-8") as f:
        spacings_txt = f.read()
```

### Using the init

Instead of having an empty init, you can instead move the `files(...)` into the
`__init__.py`. That would look like this:

```python
import importlib_resources as resources

files = resources.files(__name__)
LaB6 = files / "LaB6.txt"
# Provide whatever is useful for your project here
```

Now, a user can simply import and use `package.peakspacing.LaB6` and such
directly.

## Downloading larger files on demand

A common use case is that a project may have example notebooks or demo scripts
which require data not distributed with the project itself. One approach in
these cases is to provide a download script that the user can run to retrieve
their data from a provided URL. There are free data hosting options such as
[Zenodo][], [osf.io][] or a data-specific repository on a service like GitHub or
GitLab.

Some projects have multiple larger datasets used for examples or testing that
can be automatically downloaded on demand to a local cache on first use in a way
that is transparent to the user of the package. For example, the datasets under
`scipy.datasets` do not live in the main SciPy repository, but instead are
stored in independent repositories under the SciPy GitHub organization. A tool
called [Pooch][] is used to handle fetching these datasets from an external
repository URL for the user the first time they are requested. Pooch takes care
of comparing hash values of the downloaded data to verify its content and then
caches the downloaded files for future reuse.

The `scipy.datasets` module of SciPy and `skimage.data` module of scikit-image
are two concrete examples of how to use Pooch in this way in a project. It is
also possible to use Pooch in a simpler download script to just fetch a single
file as in the following small example:

```py
import pooch

file_path = pooch.retrieve(
    # URL to my data
    url="https://github.com/org/project/raw/v1.0.0/data/test_image.jpg",
    known_hash="sha256:50ef9a52c621b7c0c506ad1fe1b8ee8a158a4d7c8e50ddfce1e273a422dca3f9",
)
```

On repeated runs of this command, the locally cached filename would be used
instead of downloading the data again.

<!-- prettier-ignore-start -->
[importlib_resources]: https://importlib-resources.readthedocs.io/en/latest/
[osf.io]: https://osf.io/
[pooch]: https://www.fatiando.org/pooch/latest/
[zenodo]: https://zenodo.org/
[copier]: https://copier.readthedocs.io
[cookiecutter]: https://cookiecutter.readthedocs.io
<!-- prettier-ignore-end -->
