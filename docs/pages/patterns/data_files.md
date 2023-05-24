---
layout: page
title: Including data files
permalink: /patterns/data_files
nav_order: 30
parent: Patterns
---

{% include toc.html %}

# Including Data Files

In this section you will:

- Understand the importance of keeping large files out of your package.
- Learn some alternative approaches.
- Learn how to include small data files in your package.

## Consider Alternatives

**Never include large binary files in your Python package or git repository.**
Once committed, the file lives in git history forever. Git will become
sluggish, because it is not designed to operate on large binary files, and your
package will become an annoyingly large download.

Removing accidentally-committed files after the fact is *possible* but
destructive, so it's important to avoid committing large files in the first
place.

Alternatives:

- Can you generate the file using code instead? This is a good approach for
  test data: generate the test data files as part of the test. Of course it's
  important to test against *real* data from time to time, but for automated
  tests, simulated data is just fine. If you don't understand your data well
  enough to simulate it accurately, you don't know enough to write useful tests
  against it.
- Can you write a Python function that fetches the data on demand from some
  public URL? This is the approach used by projects such as scikit-learn that
  need to download large datasets for their examples and tests.

If you use one these alternatives, add the names of the generated or downloaded
files to the project's `.gitignore` file, which was provided by the
cookiecutter template. This helps protect you against accidentally committing
the file to git.

If the file in question is a text file and not very large (\< 100 kB) than it's
reasonable to just bundle it with the package.

## How to Package Data Files

What's the problem we are solving here? If your Python program needs to access
a data file, the naïve solution is just to hard-code the path to that file.

```python
data_file = open('peak_spacings/LaB6.txt')
```

But this is not a good solution because:

- The data file won't be included in the distribution: users who `pip
  install` your package will find it's missing!
- The path to the data file depends on the platform and on how the package is
  installed. We need Python to handle those details for us.

As an example, suppose we have text files with Bragg peak spacings of various
crystalline structures, and we want to use these files in our Python package.
Let's put them in a new directory named `peak_spacings/`.

```text
# peak_spacings/LaB6.txt

4.15772
2.94676
2.40116
```

```text
# peak_spacings/Si.txt

3.13556044
1.92013079
1.63749304
1.04518681
```

To access these files from the Python package, you need to edit the code in
three places:

1. Include the data files' paths to `setup.py` to make them accessible from
   the package.

   ```python
   # setup.py (excerpt)

   package_data={
       'YOUR_PACKAGE_NAME': [
           # When adding files here, remember to update MANIFEST.in as well,
           # or else they will not be included in the distribution on PyPI!
           'peak_spacings/*.txt',
           ]
       },
   ```

   We have used the wildcard `*` to capture *all* filenames that end in
   `.txt`. We could alternatively have listed the specific filenames.

2. Add the data files' paths to `MANIFEST.in` to include them in the source
   distribution. By default the distribution omits extraneous files that are
   not `.py` files, so we need to specifically include them.

   ```text
   # MANIFEST.in (excerpt)

   include peak_spacings/*.txt
   ```

3. Finally, wherever we actually use the files in our scientific code, we can
   access them using `importlib_resources`. For users with Python >= 3.9 the
   standard library `importlib.resources` module can be used directly instead
   of relying on `importlib_resources`.

   ```python
   # from importlib import resources   # Python >= 3.9 only
   import importlib_resources as resources


   ref = resources.files('peak_spacings') / 'LaB6.txt'

   # `ref` is a traversible object representing the package and its resources
   # as_file is a context manager providing a pathlib.Path object
   with resources.as_file(ref) as path:
       with open(path) as f:
           # Read in each line and convert the string to a number.
           spacings = [float(line) for line in f.read().splitlines()]
   ```

## Downloading larger files on demand

A common use case is that a project may have example notebooks or demo scripts
which require data not distributed with the project itself. One approach in
these cases is to provide a download script that the user can run to retrieve
their data from a provided URL. There are free data hosting options such as
[Zenodo][], [osf.io][] or a data-specific repository on a service like GitHub
or GitLab. 

Some projects have multiple larger datasets used for examples or testing that
can be automatically downloaded on demand to a local cache on first use in a
way that is transparent to the user of the package. For example, the datasets
under `scipy.datasets` do not live in the main SciPy repository, but instead
are stored in independent repositories under the SciPy Github organization.
A tool called [Pooch][] is used to handle fetching these datasets from an
external repository URL for the user the first time they are requested. Pooch
takes care of comparing hash values of the downloaded data to verify its
content and then caches the downloaded files for future reuse.

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

On repeated runs of this command, the locally cached filename would be used instead of
downloading the data again.

[importlib_resources]: https://importlib-resources.readthedocs.io/en/latest/
[osf.io]: https://osf.io/
[Pooch]: https://www.fatiando.org/pooch/latest/
[Zenodo]: https://zenodo.org/


