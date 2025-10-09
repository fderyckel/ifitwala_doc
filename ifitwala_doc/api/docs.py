import re
import frappe
from frappe.utils import format_datetime
from hashlib import md5

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$", re.M)

def _extract_headings(md: str):
    return [m.group(2).strip() for m in HEADING_RE.finditer(md or "")]

def _set_cache_headers(payload: bytes, modified: str | None):
    etag = md5(payload).hexdigest()
    resp = frappe.local.response
    resp["type"] = "json"
    resp["ETag"] = etag
    if modified:
        resp["Last-Modified"] = format_datetime(modified)
    inm = frappe.get_request_header("If-None-Match")
    if inm and inm.strip('"') == etag:
        resp["status_code"] = 304
        resp["type"] = "text"
        resp["message"] = ""
        return True
    return False

@frappe.whitelist(allow_guest=True)
def fetch_all(language: str | None = None):
    flt = {"status": "Published"}
    if language:
        flt["language"] = language
    docs = frappe.get_all(
        "Documentation",
        filters=flt,
        fields=["name","slug","language","title","summary","version",
                "published_on","category","subcategory","doc_order",
                "body_md","modified"],
        order_by="category, subcategory, doc_order, title",
        ignore_permissions=True,
    )
    for d in docs:
        d["tags"] = frappe.get_tags("Documentation", d["name"])
    payload = frappe.as_json({"docs": docs})
    if _set_cache_headers(payload.encode(), max((d.modified for d in docs), default=None)):
        return
    return {"docs": docs}

@frappe.whitelist(allow_guest=True)
def fetch_one(language: str, slug: str):
    d = frappe.get_value(
        "Documentation",
        {"language": language, "slug": slug, "status": "Published"},
        ["name","slug","language","title","summary","version",
         "published_on","category","subcategory","doc_order",
         "body_md","modified"],
        as_dict=True,
        ignore_permissions=True,
    )
    if not d:
        frappe.throw("Not Found", frappe.DoesNotExistError)
    d["tags"] = frappe.get_tags("Documentation", d["name"])
    return d

@frappe.whitelist(allow_guest=True)
def search_index(language: str | None = None):
    flt = {"status": "Published"}
    if language:
        flt["language"] = language
    items = frappe.get_all(
        "Documentation",
        filters=flt,
        fields=["name","slug","language","title","summary","category","subcategory","body_md","modified"],
        ignore_permissions=True,
    )
    for i in items:
        i["tags"] = frappe.get_tags("Documentation", i["name"])
        i["headings"] = _extract_headings(i.get("body_md") or "")
        i.pop("body_md", None)  # keep index payload small
        i.pop("name", None)
    payload = frappe.as_json({"items": items})
    if _set_cache_headers(payload.encode(), max((i.modified for i in items), default=None)):
        return
    return {"items": items}
