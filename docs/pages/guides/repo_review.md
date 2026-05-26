---
title: Repo-Review
html_head_extra: |
  <script src="https://cdn.jsdelivr.net/pyodide/v0.29.3/full/pyodide.js" crossorigin></script>
  <link rel="modulepreload" href="/assets/js/repo-review-app.min.js" />
---

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

```{raw} html
<div id="root">Loading (requires javascript and WebAssembly)...</div>
<style>
  .main-content ul > li::before {
    position: inherit;
    margin-left: none;
    color: none;
    content: none;
  }
  .main-content ul {
    padding-left: none;
  }
</style>
<script type="module">
  import { mountApp } from "/assets/js/repo-review-app.min.js";

  mountApp({
    header: false,
    deps: [
      "repo-review~=1.0.0",
      "sp-repo-review==2026.04.04",
      "validate-pyproject-schema-store==2026.04.03",
      "validate-pyproject[all]~=0.25.0",
    ],
  });
</script>
```

[Open in new page](https://scientific-python.github.io/repo-review/).
