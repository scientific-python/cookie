# Scientific Python Library Development Guide

This is maintained by the scientific Python community for the benefit of fellow
scientists and research software engineers. The repository contains:

- A guide
- A copier/cookiecutter template that generates a template for a scientific
  Python library
- sp-repo-review, a plugin for [repo-review](https://repo-review.readthedocs.io)

## Contributing to the documentation

To build locally, install rbenv (remember to run `rbenv init` after installing,
and `rbenv install 3.1.2`). Then:

```bash
bundle install
bundle exec jekyll serve --livereload
```

The pages are in markdown in `pages/`. Images and data files are in `assets/`.

To bump versions, use nox. You can run `nox -s pc_bump` to bump the pre-commit
versions, and `nox -s gha_bump` to bump the GitHub Actions versions.
