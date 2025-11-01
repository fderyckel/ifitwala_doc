from __future__ import annotations

from pathlib import Path
from typing import Optional

import frappe

from ifitwala_doc.api.site import _normalize_slug, get_page


def _to_slug(path: Optional[str]) -> str:
    raw = path or ""
    if raw.startswith("/"):
        raw = raw[1:]
    return _normalize_slug(raw)


def _loader_html() -> str:
    app_path = frappe.get_app_path("ifitwala_doc", "www", "index.html")
    return Path(app_path).read_text(encoding="utf-8")


def handle(path: str):
    """Serve the marketing loader when a published Ifitwala Web Page matches the request path."""
    slug = _to_slug(path)
    if slug == "/":
        return

    page = get_page(slug)
    has_content = bool(page.get("sections")) or bool(page.get("title"))
    is_published = bool(page.get("is_published"))
    if not has_content or not is_published:
        return

    if not frappe.local.response:
        frappe.local.response = frappe._dict()

    frappe.local.response.type = "page"
    frappe.local.response.route = path
    frappe.local.response.http_status_code = 200
    frappe.local.response.data = _loader_html()
    frappe.local.response.headers = frappe.local.response.get("headers") or {}
    frappe.local.response.headers["Content-Type"] = "text/html; charset=utf-8"
    return frappe.local.response.data
