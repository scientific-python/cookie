#!/usr/bin/env bash
set -euo pipefail

# Copy assets to both build outputs
for build_dir in docs/_build/html docs/_build/site/public; do
  if [ -d "$build_dir" ]; then
    mkdir -p "$build_dir/assets/js"
    cp -v docs/assets/js/repo-review-app.min.js "$build_dir/assets/js/"
    cp -v docs/assets/js/repo-review-app.min.js.map "$build_dir/assets/js/"
  fi
done

echo "✓ Assets copied successfully"
