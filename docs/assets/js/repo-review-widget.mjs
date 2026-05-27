/**
 * AnyWidget wrapper for repo-review app
 * Provides the render() interface for MyST's anywidget directive
 */

export async function render({ model, el }) {
  // Create a root container for the React app
  const root = document.createElement("div");
  root.id = "root";
  root.style.width = "100%";
  root.style.minHeight = "600px";

  // Add Material Design fonts if not already present
  ensureFonts();

  // Append root to the target element
  el.appendChild(root);

  // Determine the correct path to the app
  // The widget will be in /build/ and the app is in /assets/js/
  const baseUrl = new URL(import.meta.url);
  const appUrl = new URL("../../assets/js/repo-review-app.min.js", baseUrl)
    .href;

  // Load the app via dynamic import
  try {
    const appModule = await import(appUrl);

    // The app should export a mountApp function
    if (appModule.mountApp) {
      appModule.mountApp({
        header: true,
        deps: [
          "repo-review~=1.0.0",
          "sp-repo-review==2026.04.04",
          "validate-pyproject[all]~=0.25.0",
          "validate-pyproject-schema-store==2026.03.29",
        ],
      });
    } else {
      console.warn(
        "repo-review-app.min.js does not export mountApp, attempting alternative load",
      );
      // Try loading as a script tag instead
      loadAppAsScript(appUrl);
    }
  } catch (error) {
    console.error("Failed to load repo-review app via import:", error);
    // Fallback: load as a regular script
    const appSrc = appUrl.replace(/\.mjs$/, ".js").replace(/\.js$/, ".min.js");
    loadAppAsScript(appSrc);
  }

  function loadAppAsScript(src) {
    const script = document.createElement("script");
    script.type = "module";
    script.textContent = `import('./repo-review-app.min.js').then(m => m.mountApp ? m.mountApp({
      header: true,
      deps: [
        "repo-review~=1.0.0",
        "sp-repo-review==2026.04.04",
        "validate-pyproject[all]~=0.25.0",
        "validate-pyproject-schema-store==2026.03.29",
      ],
    }) : console.error("mountApp not found")).catch(e => {
      root.innerHTML = "<p style='color: red; padding: 20px;'>Failed to load repo-review app. Please check the browser console for details.</p>";
      console.error("Failed to load repo-review app:", e);
    });`;
    document.head.appendChild(script);
  }
}

/**
 * Ensure Material Design fonts are loaded
 */
function ensureFonts() {
  // Check if fonts are already loaded
  if (document.querySelector('link[href*="fonts.googleapis.com"]')) {
    return;
  }

  // Add Roboto font for Material Design
  const robotoLink = document.createElement("link");
  robotoLink.rel = "stylesheet";
  robotoLink.href =
    "https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap";
  document.head.appendChild(robotoLink);

  // Add Material Icons
  const iconsLink = document.createElement("link");
  iconsLink.rel = "stylesheet";
  iconsLink.href = "https://fonts.googleapis.com/icon?family=Material+Icons";
  document.head.appendChild(iconsLink);
}
