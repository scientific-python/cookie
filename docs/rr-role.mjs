/**
 * MyST plugin: {rr} inline role
 *
 * Renders a repo-review check badge:
 *   {rr}`PP007`  →  <span class="rr-btn" id="PP007">PP007</span>
 *
 * The .rr-btn CSS is in assets/css/site.css.
 */

const rrRole = {
  name: "rr",
  body: {
    type: String,
    required: true,
  },
  run(data) {
    const code = String(data.body).trim();

    // Emit a span carrying an exact-case `html_id` (e.g. id="PP007") so
    // repo-review results can deep-link into the guides. We set `html_id`
    // directly rather than `identifier`/`label`: MyST lowercases (and
    // de-duplicates) identifiers, but the same check legitimately appears on
    // multiple pages, and the deep-link fragments are case-sensitive.
    return [
      {
        type: "span",
        html_id: code,
        class: "rr-btn",
        children: [{ type: "text", value: code }],
      },
    ];
  },
};

export default { roles: [rrRole] };
