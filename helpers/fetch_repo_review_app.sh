#!/usr/bin/env bash
set -euo pipefail

version="${1:-v1.0.0rc3}"
archive_url="https://github.com/scientific-python/repo-review/releases/download/${version}/repo-review-app.zip"
dest_dir="docs/assets/js"
tmp_zip="$(mktemp)"

trap 'rm -f "$tmp_zip"' EXIT

mkdir -p "$dest_dir"
curl -fsSL "$archive_url" -o "$tmp_zip"
unzip -o -j "$tmp_zip" repo-review-app.min.js repo-review-app.min.js.map -d "$dest_dir" >/dev/null
