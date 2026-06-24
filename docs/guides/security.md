---
short_title: Security
---

# Security

Supply-chain and CI security are increasingly important for scientific Python
projects; new attacks are targeting smaller packages than ever before thanks to
the ease with which exploits can be found and utilized with AI. The first six
months of 2026 had 4.5x the malitoius package volume of _all_ of 2025[^1].

[^1]: <https://phoenix.security/accelerating-supply-chain-attacks-npm-pypi-vsx-ai-enabled-2026/>

Most of these attacks strung together smaller vulerabilties into something
exploitable, often in CI like GitHub Actions. Once in, the attacks upload
malitious packages that spread the attack via PyPI or NPM.

This page has recommendations for keeping your repository and its automation
secure. This will never be complete, but even a few small steps can make your
code much more secure.

## GitHub Actions

{rr}`SEC001` GitHub Actions workflows are a common source of security issues,
due to how commonly it is used, and it's original design being focused on ease
of use and convenience.

Common security problems:

* Action moving references, like `@v1`, or tags, like `@v1.0.1`, can be pushed
  if an attacker comprimizes the action repository you are using. If you use
  full 40 character SHA's, these cannot be modified. (Official actions are
  likely okay, but important for third party actions). There's even a GitHub
  setting to require this.
* Action SHA references can be added by a fork. If you make a fork of
  `actions/checkout`, you can reference _your_ SHA via
  `actions/checkout@<SHA>`. Only accept SHAs you have verified or a tool (like
  dependabot) produce. If you use Zizmor, it can also verify that an SHA matches
  a tag, tags cannot be pulled from a fork.
* Caching is dangerous. Attackers can poison an unrelated cache. Avoid caching
  in your release jobs.
* `pull_request_target` is really dangerous. Attackers can use it to poison
  caches, for example.
* Tighten default permissions. A job should not have permissions to do anything
  it doesn't need. Set the default in settings to read-only, then explicitly
  grant required permissions.
* Don't build code in your release job. The release job should do _as little as
  possible_.
* Use trusted publishing. There's no long-lived token to steal.

### Zizmor

[zizmor](https://docs.zizmor.sh) is a static analysis tool that audits your
workflows for common problems, including many of the ones above. You can run
it as a pre-commit hook or as a GitHub Action:

::::{tab-set}
:::{tab-item} pre-commit

```yaml
- repo: https://github.com/zizmorcore/zizmor-pre-commit
  rev: "v1.26.1"
  hooks:
    - id: zizmor
```

:::
:::{tab-item} GitHub Actions

The [`zizmorcore/zizmor-action`](https://github.com/zizmorcore/zizmor-action)
GitHub Action can upload its findings to GitHub's code scanning dashboard:

```yaml
name: zizmor

on:
  push:
    branches: [main]
  pull_request:

permissions: {}

jobs:
  zizmor:
    runs-on: ubuntu-latest
    permissions:
      security-events: write
    steps:
      - uses: actions/checkout@v7
        with:
          persist-credentials: false

      - uses: zizmorcore/zizmor-action@v0.5.7
```

:::
::::

You can silence individual findings with `# zizmor: ignore[rule]` comments, or
collect them in a [`zizmor.yml`](https://docs.zizmor.sh/configuration/) config
file.
