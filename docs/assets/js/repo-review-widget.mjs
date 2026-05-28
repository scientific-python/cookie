/**
 * AnyWidget wrapper for repo-review app
 * Provides the render() interface for MyST's anywidget directive
 */

import { mountApp } from "https://cdn.jsdelivr.net/npm/repo-review-webapp@1.1.0/dist/repo-review-app.mjs";

export async function render({ model, el }) {
  const root = document.createElement("div");
  root.id = "root";
  root.style.width = "100%";
  root.style.minHeight = "600px";

  ensureFonts();
  el.appendChild(root);

  mountApp({
    header: true,
    deps: [
      "repo-review~=1.0.0",
      "sp-repo-review==2026.04.04",
      "validate-pyproject[all]~=0.25.0",
      "validate-pyproject-schema-store==2026.03.29",
    ],
  });
}

function ensureFonts() {
  if (document.querySelector('link[href*="fonts.googleapis.com"]')) {
    return;
  }
  const robotoLink = document.createElement("link");
  robotoLink.rel = "stylesheet";
  robotoLink.href =
    "https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap";
  document.head.appendChild(robotoLink);

  const iconsLink = document.createElement("link");
  iconsLink.rel = "stylesheet";
  iconsLink.href = "https://fonts.googleapis.com/icon?family=Material+Icons";
  document.head.appendChild(iconsLink);
}
