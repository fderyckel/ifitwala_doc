from __future__ import annotations

from pathlib import Path

import frappe


def handle(path: str):
    """Serve the static marketing loader for published Ifitwala Web Pages."""
    try:
        slug = (path or "").strip()
        if not slug:
            slug = "/"
        if not slug.startswith("/"):
            slug = f"/{slug}"

        page = frappe.get_all(
            "Ifitwala Web Page",
            filters={"slug": slug, "is_published": 1},
            fields=["name"],
            limit=1,
        )
        if not page:
            return

        loader_path = Path(frappe.get_app_path("ifitwala_doc", "www", "index.html"))
        html = loader_path.read_text(encoding="utf-8")
        frappe.local.response.type = "page"
        frappe.local.response.data = html
        frappe.local.response.headers = frappe.local.response.get("headers") or {}
        frappe.local.response.headers["Content-Type"] = "text/html; charset=utf-8"
        return html
    except Exception:
        frappe.log_error("Error handling marketing catch-all", "ifitwala_doc")
        return
