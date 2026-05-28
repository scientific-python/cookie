/**
 * MyST plugin: {rr} inline role
 *
 * Renders a repo-review check badge:
 *   {rr}`PP007`  →  <span class="rr-btn" id="PP007">PP007</span>
 *
 * The .rr-btn CSS is in assets/css/site.css.
 */

const escapeHtml = (value) =>
  String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");

const rrRole = {
  name: "rr",
  body: {
    type: String,
    required: true,
  },
  run(data) {
    const code = String(data.body).trim();
    const safeId = code.replace(/[^A-Za-z0-9_-]/g, "_");

    return [
      {
        type: "html",
        value: `<span class="rr-btn" id="${safeId}">${escapeHtml(code)}</span>`,
      },
    ];
  },
};

export default { roles: [rrRole] };
