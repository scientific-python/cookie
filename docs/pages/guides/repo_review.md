# Repo-Review

You can check the style of a GitHub repository below. Enter any repository, such
as `scikit-hep/hist`, and the branch you want to check, such as `main` (it must
exist). This will produce a list of results - green checkmarks mean this rule is
followed, red errors mean the rule is not. A yellow warning sign means that the
check was skipped because a previous required check failed. Some checks will
fail, that's okay - the goal is bring all possible issues to your attention, not
to force compliance with arbitrary checks.

You can also run [this tool](https://github.com/scientific-python/repo-review)
locally (Python 3.10+ required):

```bash
pipx run 'sp-repo-review[cli]' <path to repo>
```

---

<!-- rumdl-disable-next-line MD034 -->
:::{anywidget} https://cdn.jsdelivr.net/npm/repo-review-webapp@1.2.1/dist/repo-review-anywidget.mjs
{
  "url_sync": true,
  "deps": [
    "repo-review~=1.2.1",
    "sp-repo-review==2026.06.18",
    "validate-pyproject[all]~=0.25.0",
    "validate-pyproject-schema-store==2026.06.14",
  ]
}
:::
