/**
 * Subpath deployment helper — e.g. http://host/english/ alongside an existing site.
 */
(function pep6BaseModule() {
  function normalizeBase(raw) {
    const s = String(raw || "").trim();
    if (!s || s === "/") return "";
    const withSlash = s.startsWith("/") ? s : `/${s}`;
    return withSlash.replace(/\/+$/, "");
  }

  const meta = document.querySelector('meta[name="pep6-base"]');
  window.PEP6_BASE = normalizeBase(meta?.getAttribute("content") || "");

  window.pep6Url = function pep6Url(path) {
    const p = String(path || "");
    if (!p) return window.PEP6_BASE || "/";
    if (p.startsWith("http://") || p.startsWith("https://")) return p;
    const suffix = p.startsWith("/") ? p : `/${p}`;
    return `${window.PEP6_BASE || ""}${suffix}`;
  };
})();
