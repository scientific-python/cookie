---
layout: page
title: "GHA: GitHub Actions intro"
permalink: /guides/gha-basic/
nav_order: 10
parent: Topical Guides
custom_title: GitHub Actions introduction
---

{% include toc.html %}

# GitHub Actions: Intro

{% rr GH100 %} The recommended CI for scientific Python projects is GitHub
Actions (GHA), although its predecessor Azure is also in heavy usage, and other
popular services (Travis, Appveyor, and Circle CI) may be found in a few
packages. GHA is preferred due to the flexible, extensible design and the tight
integration with the GitHub permissions model (and UI). Here is a guide in
setting up a new package with GHA.

GHA is made up of
[workflows](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
which consist of actions. Here are some of the workflows you will probably want
in your package. These should be in a file named `.github/workflows/main.yml` or
similar.

## Header

Your main CI workflow file should begin something like this:

```yaml
name: CI

on:
  pull_request:
  push:
    branches:
      - main

jobs:
```

This gives the workflow a nice name {% rr GH101 %}, and defines the conditions
under which it runs. This will run on all pull requests, or pushes to main. If
you use a develop branch, you probably will want to include that. You can also
specify specific branches for pull requests instead of running on all PRs (will
run on PRs targeting those branches only).

## Pre-commit

If you use [pre-commit](https://pre-commit.com) (and you should), and you don't
want to / can't use [pre-commit.ci](https://pre-commit.ci) yet, then this is a
job that will check pre-commit for you:

{% raw %}

```yaml
lint:
  name: Lint
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: "3.x"
    - uses: pre-commit/action@v3.0.0
```

{% endraw %}

If you do use [pre-commit.ci](https://pre-commit.ci), but you need this job to
run a manual check, like check-manifest, then you can keep it but just use
`with: extra_args: --all-files --hook-stage manual check-manifest` to run just
this one check. You can also use `needs: lint` in your other jobs to keep them
from running if the lint check does not pass.

## Unit tests

Implementing unit tests is also easy. Since you should be following best
practices listed in the previous sections, this becomes an almost directly
copy-and-paste formula, regardless of the package details. You might need to
adjust the Python versions to suit your taste; you can also test on different
OS's if you'd like by adding them to the matrix and inputting them into
`runs-on`.

{% raw %}

```yaml
tests:
  runs-on: ubuntu-latest
  strategy:
    fail-fast: false
    matrix:
      python-version:
        - "3.8"
        - "3.11"
        - "3.12"
  name: Check Python ${{ matrix.python-version }}
  steps:
    - uses: actions/checkout@v3
      with:
        fetch-depth: 0 # Only needed if using setuptools-scm

    - name: Setup Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
        allow-prereleases: true

    - name: Install package
      run: python -m pip install -e .[test]

    - name: Test package
      run: python -m pytest
```

{% endraw %}

A few things to note from above:

The matrix should contain the versions you are interested in. You can also test
on other OS's if you are building any extensions or are worried about your
package on macOS or Windows. Fail-fast is optional.

The formula here for installing should be identical for all users; and using
[PEP 517](https://www.python.org/dev/peps/pep-0517/)/[518](https://www.python.org/dev/peps/pep-0518/)
builds, you are even guaranteed a consistent wheel will be produced just as if
you were building a final package.

## Updating

{% rr GH200 %} {% rr GH210 %} If you use non-default actions in your repository
(you will see some in the following pages), then it's a good idea to keep them
up to date. GitHub provided a way to do this with dependabot. Just add the
following file as `.github/dependabot.yml`:

```yaml
version: 2
updates:
  # Maintain dependencies for GitHub Actions
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

This will check to see if there are updates to the action weekly, and will make
a PR if there are updates, including the changelog and commit summary in the PR.
If you select a name like `v1`, this should only look for updates of the same
form (since April 2022) - there is no need to restrict updates for "moving tag"
updates anymore {% rr PY006 %}. You can also use SHA's and dependabot will
respect that too.

You can use this for other ecosystems too, including Python.

## Common needs

### Single OS steps

If you need to have a step run only on a specific OS, use an if on that step
with `runner.os`:

```yaml
if: runner.os != 'Windows' # also 'macOS' and 'Linux'
```

Using `runner.os` is better than `matrix.<something>`. You also have an
environment variable `$RUNNER_OS` as well. Single quotes are required here.

### Changing the environment in a step

If you need to change environment variables for later steps, such combining with
an if condition for only for one OS, then you add it to a special file:

```yaml
- run: echo "MY_VAR=1" >> $GITHUB_ENV
```

Later steps will see this environment variable.

### Communicating between steps

You can also directly communicate between steps, by setting `id:`'s. Some
actions have outputs, and bash actions can manually write to output:

```yaml
- id: someid
  run: echo "something=true" >> $GITHUB_OUTPUT
```

{% raw %}

You can now refer to this step in a later step with
`${{ steps.someid.something }}`. You also can get it from another job by using
`${{ needs.<jobname>.outputs.something }}`. The `toJson()` function is useful
for inputing JSON - you can even generate matrices dynamically this way!

{% endraw %}

### Pretty output

You can write GitHub flavored markdown to `$GITHUB_STEP_SUMMARY`, and it will be
shown on the summary page.

You can output annotations, as well; these show up inline on the code in the PR.
This can be done by
[setting special double-colon outputs](https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#setting-an-error-message),
like `echo "::error file=app.js,line=1::Missing semicolon"`. See
[pytest-github-actions-annotate-failures](https://github.com/pytest-dev/pytest-github-actions-annotate-failures)
for a plugin to do this with pytest.

You can also do this
[by supplying matchers](https://github.com/actions/toolkit/blob/main/docs/problem-matchers.md),
which tell GitHub to look for certain patterns, such as
`echo "::add-matcher::$GITHUB_WORKSPACE/.github/matchers/pylint.json"`. Do keep
in mind you can only see up to 10 matches per type per step, and a total of 50
matchers.

### Common useful actions

There are a variety of useful actions. There are GitHub supplied ones:

- [actions/checkout](https://github.com/actions/checkout): Almost always the
  first action. v2+ does not keep Git history unless `with: fetch-depth: 0` is
  included (important for SCM versioning). v1 works on very old docker images.
- [actions/setup-python](https://github.com/actions/setup-python): v4+ requires
  a Python version to be selected (`"3.x"` is valid, however), also supports
  multiple versions with a range and `allow-prereleases`.
- [actions/cache](https://github.com/actions/cache): Can store files and restore
  them on future runs, with a settable key.
- [actions/upload-artifact](https://github.com/actions/upload-artifact): Upload
  a file to be accessed from the UI or from a later job.
- [actions/download-artifact](https://github.com/actions/download-artifact):
  Download a file that was previously uploaded, often for releasing. Match
  upload-artifact version.
- [actions/labeler](https://github.com/actions/labeler): Add labels to PRs and
  such.
- [actions/stale](https://github.com/actions/stale): Mark old issues/PRs as
  stale.
- [actions/upload-pages-artifact](https://github.com/actions/upload-pages-artifact),
  [actions/configure-pages](https://github.com/actions/configure-pages), and
  [actions/deploy-pages](https://github.com/actions/configure-pages): Provides
  the ability to deploy directly to GitHub Pages. See the guide later on this
  page.

And many other useful ones:

- [ilammy/msvc-dev-cmd](https://github.com/ilammy/msvc-dev-cmd): Setup MSVC
  compilers.
- [jwlawson/actions-setup-cmake](https://github.com/jwlawson/actions-setup-cmake):
  Setup any version of CMake on almost any image.
- [wntrblm/nox](https://github.com/wntrblm/nox): Setup all versions of Python
  and provide nox.
- [pre-commit/action](https://github.com/pre-commit/action): Run pre-commit with
  built-in caching.
- [conda-incubator/setup-miniconda](https://github.com/conda-incubator/setup-miniconda):
  Setup conda or mamba on GitHub Actions.
- [ruby/setup-ruby](https://github.com/ruby/setup-ruby): Setup Ruby if you need
  it for something.
- [peter-evans/create-pull-request](https://github.com/peter-evans/create-pull-request):
  Make a new PR with the current changes (more options than just using `gh`).
  You can even auto-merge PRs with `run: gh pr merge --merge --auto "1"`
  afterwards.

A couple more from Python developers; note these do not provide `vX` moving tags
like the official actions and most other actions, but instead have `release/vX`
branches that you can use.

- [pypa/gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish):
  Publish Python packages to PyPI. Supports trusted publisher deployment.
- [re-actors/alls-green](https://github.com/re-actors/alls-green): Tooling to
  check to see if all jobs passed (supports allowed failures, too).

There are also a few useful tools installed which can really simplify your
workflow or adding custom actions. This includes system package managers (like
brew, chocolaty, NuGet, Vcpkg, etc), as well as a fantastic cross platform one:

- [pipx](https://github.com/pypa/pipx): This is pre-installed on all runners
  (GitHub uses to set up other things), and is kept up to date. It enables you
  to use any PyPI application in a single line with `pipx run <app>`.

You can also run GitHub Actions locally:

- [act](https://github.com/nektos/act): Run GitHub Actions in a docker image
  locally.

## Advanced usage

These are some things you might need.

### Cancel existing runs

{% rr GH102 %} If you add the following, you can ensure only one run per
PR/branch happens at a time, cancelling the old run when a new one starts:

{% raw %}

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

{% endraw %}

Anything with a matching group name will count in the same group - the ref is
the "from" name for the PR. If you want, you can replace `github.ref` with
`github.event.pull_request.number || github.sha`; this will still cancel on PR
pushes but will build each commit on `main`.

### Pass job

If you want support GitHub's "merge when pass" feature, you should set up a pass
job instead of listing every job you wand to require. Besides making it much
easier to add and remove jobs, it also means that adding a new required job
won't make all of your past, _merged_ PRs change from a green checkmark to an
orange "pending" symbol (since there are new requirements that they didn't
pass).

As an example, if you had `lint` and `checks` jobs, use this:

{% raw %}

```yaml
pass:
  if: always()
  needs: [lint, checks]
  runs-on: ubuntu-latest
  steps:
    - uses: re-actors/alls-green@release/v1
      with:
        jobs: ${{ toJSON(needs) }}
```

{% endraw %}

We want the job to always run, so we set `if: always()`. Otherwise, it might be
skipped if any job it depends on is skipped, and skipped jobs count as "passing"
to GitHub's automerge (yikes!). The important part of the job is the `needs:`
list; this tells it what is required.

We use `re-actors/alls-green` to evaluate whether required jobs have passed. You
need to tell it what jobs are required, which you can do without repeating the
needs list by taking the `needs` list and inputing it as json to `with: jobs:`.

This will also support jobs that are allowed to fail (`allowed-failures:`) and
allowed to be skipped (`allowed-skips:`) too.

Just set this `pass` job in your required checks for your main branch. Then
you'll be able to use GitHub's auto merge functionality.

### Custom actions

You can
[write your own actions](https://docs.github.com/en/actions/creating-actions)
locally or in a shared GitHub repo in either GitHub actions syntax itself
(called "composite"), JavaScript, or Docker. Combined with pipx, composite
actions are very easy to write!

To create a custom action, either places it in `.github/acitons` (Just for
internal use in that repo's workflows), or in `action.yml` if you want to allow
others to use your repository as an action. The start of the file looks like:

```yaml
name: <some name>
description: <Some description>
```

You can also setup inputs, which will be placed by the user in `with:`:

```yaml
inputs:
  some-input:
    description: <Some description>
    required: true
```

Then you specify that the action is composite and give it the steps to run:

```yaml
runs:
  using: composite
  steps:
```

If you specify a `runs:` step, you have to specify `shell: <something>`.
Otherwise, it's basically identical to what you are used to; you can use `if:`,
etc.

One common use case is using Python. Unless it's the point of your action, you
ideally shouldn't change the user's environment; suddenly changing the active
Python version might come as a surprise. You can do that, though, using
`update-environment: false` with `setup-python` and `pipx`:

{% raw %}

```yaml
- uses: actions/setup-python@v4
  id: python
  with:
    python-version: "3.11"
    update-environment: false

- name: Run some local program
  shell: bash
  run:
    pipx run --python '${{ steps.python.outputs.python-path }}' '${{
    github.action_path }}' ${{ inputs.some-input }}
```

{% endraw %}

You use the `python-path` output from `setup-python` to get the Python you
activated. You use `github.action_path` to get the path to the checked-out
action.

{: .highlight }

> Examples of custom composite actions include:
>
> - [pypa/cibuildwheel](https://github.com/pypa/cibuildwheel/blob/main/action.yml)
> - [wntrblm/nox](https://github.com/wntrblm/nox/blob/main/action.yml)
> - [scientific-python/repo-review](https://github.com/scientific-python/repo-review/blob/main/action.yml)
> - [scientific-python/cookie](https://github.com/scientific-python/cookie/blob/main/action.yml)
>   (This repo)

### Reusable workflows

You can also make reusable workflows. One reason to do this is it allows you to
use `needs` or communicate values between workflows. It's an easy way to make
one workflow (which con contain multiple jobs, even a matrix) depend on anther.

To use a reusable workflow, you replace the triggers with:

```yaml
on:
  workflow_call:
```

If you add a `outputs:` table to the workflow call table, you can specify
outputs for other workflows to read. See other options
[in the docs](https://docs.github.com/en/actions/using-workflows/reusing-workflows).

### Conditional workflows

Sometimes you have jobs that depend on certain files in our repository. Maybe
you only want to run tests if code or tests files are changed, docs if
documentation changes, etc. While GitHub does allow you to specify files in
triggers, it doesn't play well with required checks or usage across multiple
workflows. Here is a way to set it up that works well with those:

Write your workflows as reusable workflows. This means they start with a trigger
that allows other workflows to call them:

```yaml
# reusable-tests.yml, for example
on:
  workflow_call:
```

Otherwise, they look like normal workflows. Then you need another reusable
workflow file to decide when to run a specific situation.

{% raw %}

```yaml
# reusable-change-detection.yml
on:
  workflow_call:
    outputs:
      run-tests:
        value: ${{ jobs.change-detection.outputs.run-tests || false }}
      # More here if you have more situations to detect
```

{% endraw %}

You start by specifying outputs when running this. You'll want one output per
situation you want to detect. The value will be output from our
`change-detection` job below, and defaults to "false" if we don't output
anything.

Now, we need our job:

{% raw %}

```yaml
jobs:
  change-detection:
    runs-on: ubuntu-latest
    outputs:
      run-tests: ${{ steps.cookie-changes.outputs.run-tests || false }}
      # more here if you have more situations to detect

    steps:
      - uses: actions/checkout@v3

      - name: Changed test-related files
        if: github.event_name == 'pull_request'
        id: changed-tests-files
        uses: Ana06/get-changed-files@v2.2.0
        with:
          format: "json"
          filter: |
            tests/**
            src/**.py
            .github/workflows/ci.yml
            .github/workflows/reusable-tests.yml

      - name: Set a flag for running the tests
        if: >-
          github.event_name != 'pull_request' ||
          steps.changed-tests-files.outputs.added_modified_renamed != '[]'
        id: tests-changes
        run: echo "run-tests=true" >> "${GITHUB_OUTPUT}"

      # Add 2 more steps per situation you have to detect
```

{% endraw %}

This has a bit of boilerplate (mostly around passing variables around), but what
it's doing is fairly simple. Instead of stepping through it, let's look at what
it's trying to do. First, you need to find a list of all changed files in the
current PR. That's done using `Ana06/get-changed-files` (which does not provide
a `v2` or `v2.2` moving tag). That list is then filtered using `filter:`. It is
returned as `json` (otherwise you will not be able to support filenames with
spaces in them). The return list doesn't actually matter; in the next step, we
simply check to see if it's empty (`[]` in json). If we are not in a PR or if
there are returned files, we set `run-tests=true`; otherwise, we don't (if we
are in a PR and there were no matches).

Everything else in the job is about getting the output from the step
`changed-tests-files` to `tests-changes`, then from there into the resusable
workflow output as `run-tests`.

{: .note }

Someone probably could write an action (maybe even an composite action using
either `gh` or `shell: python`) that could directly report changes true/false
instead of a file list, saving the two step process and greatly simplifying
this.

If you have more situations, you just repeat these two steps with different
`id`s and inputs.

Finally, you write the overarching CI workflow that combines the reusable
workflows, something like `ci.yml`:

{% raw %}

```yaml
on:
  workflow_dispatch:
  pull_request:
  push:
    branches:
      - main

jobs:
  change-detection:
    uses: ./.github/workflows/reusable-change-detection.yml

  tests:
    needs: change-detection
    if: fromJSON(needs.change-detection.outputs.run-tests)
    uses: ./.github/workflows/reusable-tests.yml

  # more here if you need more

  pass:
    if: always()
    needs:
      - change-detection
      - tests
    runs-on: ubuntu-latest

    steps:
      - name: Decide whether the needed jobs succeeded or failed
        uses: re-actors/alls-green@release/v1
        with:
          allowed-skips: >-
            ${{
              fromJSON(needs.change-detection.outputs.run-tests)
              && ''
              || '
              tests,
              '
            }}
          jobs: ${{ toJSON(needs) }}
```

If you have more situations, add another `${{ ... }}` above, after the first
one, and add them to the needs list. This is really just injecting "tests" only
if the "tests" job is being skipped into `allowed-skips`.

{% endraw %}

{: .highlight }

> Some examples of repos using this method are:
>
> - [pypa/build](https://github.com/pypa/build/tree/main/.github/workflows)
> - [scientific-python/cookie](https://github.com/scientific-python/cookie/tree/main/.github/workflows)
>   (this repo)

### GitHub pages

GitHub has finished moving their pages build infrastructure to Actions, and they
[now provide](https://github.blog/changelog/2022-07-27-github-pages-custom-github-actions-workflows-beta/)
the ability to directly push to Pages from Actions. This replaced the old
workarounds of (force) pushing output to a branch or to separate repository.

Before starting, make sure in the Pages settings the source is set to "Actions".

You'll probably want this job to run on both your main branch, as well as
`workflow_dispatch`, just in case you want to manually trigger a rebuild. You
should set the permission so that the built-in `GITHUB_TOKEN` can write to
pages:

```yaml
permissions:
  contents: read
  pages: write
  id-token: write
```

{% rr GH103 %} You probably only want one deployment at a time, so you can use:

```yaml
concurrency:
  group: "pages"
  cancel-in-progress: true
```

Now you'll want three custom actions in your `steps:`. First, you need to
configure Pages.

```yaml
- name: Setup Pages
  id: pages
  uses: actions/configure-pages@v3
```

{% raw %}

Notice this action sets an `id:`; this will allow you to use the outputs from
this action later; specifically, may want to use
`${{ steps.pages.outputs.base_path }}` when building (you can also get `origin`,
`base_url`, or `host` - see the action
[config](https://github.com/actions/configure-pages/blob/main/action.yml)).

{% endraw %}

```yaml
- name: Upload artifact
  uses: actions/upload-pages-artifact@v2
```

This actions defaults to uploading `_site`, but you can give any `with: path:`
if you want, including `"."` which is the whole repository.

Finally, you'll need to deploy the artifact (named `github-pages`) to Pages. You
can make this a custom job with `needs:` pointing at your previous job (in this
example, the previous job is called `build`):

{% raw %}

```yaml
deploy:
  environment:
    name: github-pages
    url: ${{ steps.deployment.outputs.page_url }}
  runs-on: ubuntu-latest
  needs: [build]
  steps:
    - name: Deploy to GitHub Pages
      id: deployment
      uses: actions/deploy-pages@v2
```

{% endraw %}

The deploy-pages job gives a `page_url`, which is the same as `base_url` on the
configure step, and can be set in the `environment`. If you want to do
everything in one job, you only need one of these.

{: .highlight }

> See the
> [official starter workflows](https://github.com/actions/starter-workflows/tree/main/pages)
> for examples. Some other examples include:
>
> - [CLIUtils.github.io/CLI11](https://github.com/CLIUtils/CLI11/blob/main/.github/workflows/docs.yml)
> - [iris-hep.org](https://github.com/iris-hep/iris-hep.github.io/blob/master/.github/workflows/deploy.yml)
