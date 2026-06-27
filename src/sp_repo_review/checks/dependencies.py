# DU: Dependency Updating

from __future__ import annotations

from typing import Any

from . import mk_url

class Dependencies:
    family = "dependencies"


class DEP200(Dependencies):
    """Maintained by Dependabot or Renovate."""

    url = mk_url("gha-basic")

    @staticmethod
    def check(dependabot: dict[str, Any], renovate: dict[str, Any]) -> bool:
        """
        All projects should have a tool to manage dependencies, either Dependabot or Renovate.

        Something like one of these:

        `.github/dependabot.yml`
        ```yaml
        version: 2
        updates:
        # Maintain dependencies for GitHub Actions
          - package-ecosystem: "github-actions"
            directory: "/"
            schedule:
              interval: "weekly"
        ```

        `renovate.json`
        ```json
        {{
          "extends": ["config:recommended"]
        }}
        ```
        Renovate configurations in `package.json` are not supported.
        Configurations in `.jsonc` or `.json5` files are not fully supported.
        """
        return bool(dependabot or renovate)


def repo_review_checks() -> dict[str, Dependencies]:
    return {p.__name__: p() for p in Dependencies.__subclasses__()}
