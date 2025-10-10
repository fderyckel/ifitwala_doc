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

def _load_tags_for(names: list[str]) -> dict[str, list[str]]:
    if not names:
        return {}
    placeholders = ", ".join(["%s"] * len(names))
    rows = frappe.db.sql(
        f"""
        SELECT link_name, tag
        FROM `tabTag Link`
        WHERE link_doctype = 'Documentation'
          AND link_name IN ({placeholders})
        """,
        names,
        as_dict=True,
    )
    tags_by_name: dict[str, list[str]] = {}
    for row in rows:
        tags_by_name.setdefault(row["link_name"], []).append(row["tag"])
    return tags_by_name

def _subcategory_column() -> str | None:
    columns = []
    try:
        columns = frappe.db.get_table_columns("Documentation") or []
    except Exception:
        pass
    if "subcategory" in columns:
        return "subcategory"
    if "sub_category" in columns:
        return "sub_category"
    return None

def _normalize_subcategory(record: dict, column: str | None):
    if not column:
        record.setdefault("subcategory", None)
        return record
    if column != "subcategory":
        record["subcategory"] = record.pop(column, None)
    return record

@frappe.whitelist(allow_guest=True)
def fetch_all(language: str | None = None):
    flt = {"status": "Published"}
    if language:
        flt["language"] = language
    subcat_col = _subcategory_column()
    fields = [
        "name","slug","language","title","summary","version",
        "published_on","category","doc_order","body_md","modified"
    ]
    if subcat_col:
        fields.insert(7, subcat_col)
    docs = frappe.get_all(
        "Documentation",
        filters=flt,
        fields=fields,
        order_by=f"category, {subcat_col}, doc_order, title" if subcat_col else "category, doc_order, title",
        ignore_permissions=True,
    )
    tags = _load_tags_for([d["name"] for d in docs])
    for d in docs:
        _normalize_subcategory(d, subcat_col)
        d["tags"] = tags.get(d.get("name"), [])
    payload = frappe.as_json({"docs": docs})
    if _set_cache_headers(payload.encode(), max((d.modified for d in docs), default=None)):
        return
    return {"docs": docs}

@frappe.whitelist(allow_guest=True)
def fetch_one(language: str, slug: str):
    subcat_col = _subcategory_column()
    fields = [
        "name","slug","language","title","summary","version",
        "published_on","category","doc_order","body_md","modified"
    ]
    if subcat_col:
        fields.insert(7, subcat_col)
    d = frappe.get_value(
        "Documentation",
        {"language": language, "slug": slug, "status": "Published"},
        fields,
        as_dict=True,
        ignore_permissions=True,
    )
    if not d:
        frappe.throw("Not Found", frappe.DoesNotExistError)
    _normalize_subcategory(d, subcat_col)
    tags = _load_tags_for([d.get("name")])
    d["tags"] = tags.get(d.get("name"), [])
    return d

@frappe.whitelist(allow_guest=True)
def search_index(language: str | None = None):
    flt = {"status": "Published"}
    if language:
        flt["language"] = language
    subcat_col = _subcategory_column()
    fields = [
        "name","slug","language","title","summary","category","body_md","modified"
    ]
    if subcat_col:
        fields.insert(6, subcat_col)
    items = frappe.get_all(
        "Documentation",
        filters=flt,
        fields=fields,
        ignore_permissions=True,
    )
    tags = _load_tags_for([i["name"] for i in items])
    for i in items:
        _normalize_subcategory(i, subcat_col)
        i["tags"] = tags.get(i.get("name"), [])
        i["headings"] = _extract_headings(i.get("body_md") or "")
        i.pop("body_md", None)  # keep index payload small
        i.pop("name", None)
    payload = frappe.as_json({"items": items})
    if _set_cache_headers(payload.encode(), max((i.modified for i in items), default=None)):
        return
    return {"items": items}
