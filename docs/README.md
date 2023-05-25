# Scikit-HEP Developer pages

## Developer info

To build locally, install rbenv (remember to run `rbenv init` after installing, and `rbenv install 3.1.2`). Then:

```bash
bundle install
bundle exec jekyll serve --livereload
```

The pages are in markdown in `pages/`. Images and datafiles are in `assets/`.

To bump versions, use nox. You can run `nox -s pc_bump` to bump the pre-commit versions, and `nox -s gha_bump` to bump the GitHub Actions versions.
