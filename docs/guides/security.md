---
short_title: Security
---

# Security

Supply-chain and CI security are increasingly important for scientific Python
projects; new attacks are targeting smaller packages than ever before thanks
to the ease with which exploits can be found and utilized with AI. This page
collects recommendations for keeping your repository and its automation secure.
This is a work in progress; expect it to grow over time.

## GitHub Actions

{rr}`SEC001` GitHub Actions workflows are a common source of security issues,
such as script injection from untrusted input, overly broad token permissions,
and credentials accidentally persisted by `actions/checkout`.
[zizmor](https://docs.zizmor.sh) is a static analysis tool that audits your
workflows for these problems. The easiest way to run it is as a pre-commit hook:

```yaml
- repo: https://github.com/zizmorcore/zizmor-pre-commit
  rev: "v1.26.1"
  hooks:
    - id: zizmor
```

You can silence individual findings with `# zizmor: ignore[rule]` comments, or
collect them in a [`zizmor.yml`](https://docs.zizmor.sh/configuration/) config
file. If you'd rather keep it out of pre-commit, zizmor also ships the
[`zizmorcore/zizmor-action`](https://github.com/zizmorcore/zizmor-action)
GitHub Action, which can upload results to GitHub's code scanning dashboard.
