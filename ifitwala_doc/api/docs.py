# apps/ifitwala_doc/ifitwala_doc/api/docs.py

import re
import frappe
from frappe.utils import format_datetime
from hashlib import md5
from frappe import _
import os
from frappe.utils import get_site_path
from ifitwala_doc.ifitwala_doc.image_utils import slugify

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$", re.M)
SLUG_SAFE_RE = re.compile(r"[^a-z0-9-]+")

def _extract_headings(md: str):
    return [m.group(2).strip() for m in HEADING_RE.finditer(md or "")]

def _set_cache_headers(payload: bytes, modified: str | None):
    resp = frappe.local.response
    resp["type"] = "json"

    ua = (frappe.get_request_header("User-Agent") or "").lower()
    if "astro-build" in ua:
        if modified:
            resp["Last-Modified"] = format_datetime(modified)
        return False

    etag = md5(payload).hexdigest()
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
    """Return {docname: [tag, ...]} for Documentation docs in `names`,
    adapting to whichever Tag Link schema this site uses."""
    if not names:
        return {}

    has = frappe.db.has_column
    # Prefer the classic schema first (most common)
    if has("Tag Link", "parenttype") and has("Tag Link", "parent"):
        rows = frappe.get_all(
            "Tag Link",
            filters={"parenttype": "Documentation", "parent": ["in", names]},
            fields=["parent as name", "tag"],
            ignore_permissions=True,
        )
    elif has("Tag Link", "document_type") and has("Tag Link", "document_name"):
        rows = frappe.get_all(
            "Tag Link",
            filters={"document_type": "Documentation", "document_name": ["in", names]},
            fields=["document_name as name", "tag"],
            ignore_permissions=True,
        )
    elif has("Tag Link", "link_doctype") and has("Tag Link", "link_name"):
        rows = frappe.get_all(
            "Tag Link",
            filters={"link_doctype": "Documentation", "link_name": ["in", names]},
            fields=["link_name as name", "tag"],
            ignore_permissions=True,
        )
    else:
        # Unknown schema; return empty safely
        return {}

    tags_by_name: dict[str, list[str]] = {}
    for r in rows:
        nm = r.get("name")
        if nm:
            tags_by_name.setdefault(nm, []).append(r["tag"])
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

def _shot_folder(slug: str) -> str:
    """
    Folder name that matches image_util.resize_and_save (single level under gallery_resized).
    Example: slug='student-attendance' -> 'docs_student-attendance_shots'
    """
    return f"docs_{slug}_shots"

def _slug_safe(s: str) -> str:
    """Kebab-case for URLs; keep hyphens."""
    return SLUG_SAFE_RE.sub("", (s or "").strip().lower().replace(" ", "-")).strip("-")

def _file_exists(url: str) -> bool:
    """Check for /public files existence from a /files/... URL."""
    if not url:
        return False
    path = get_site_path("public", url.lstrip("/"))
    return os.path.exists(path)

def _variant_bases(anchor: str) -> list[str]:
    """
    Return a list of candidate basename tokens for a screenshot anchor.
    We primarily use image_utils.slugify (underscores), but we also consider
    a kebab-case flavour so we gracefully handle legacy files that were saved
    with hyphens.
    """
    seeds = [anchor or ""]
    seed = seeds[0]
    if seed:
        for extra in (seed.replace("-", "_"), seed.replace("_", "-")):
            if extra not in seeds:
                seeds.append(extra)

    candidates: list[str] = []

    def _add(value: str | None):
        value = (value or "").strip().strip("_-")
        if not value:
            return
        if value not in candidates:
            candidates.append(value)

    for s in seeds:
        _add(slugify(s))

    for c in list(candidates):
        kebab = c.replace("_", "-")
        _add(kebab)

    return candidates or [slugify(anchor or "")]

def _shot_manifest_for(docname: str, slug: str) -> list[dict]:
    """
    Build a manifest containing metadata + URLs for each Doc Screenshot row.
    Uses the SAME slug algorithm as the resizer so filenames match, but also
    probes a kebab-case variant to avoid 404s when legacy files used hyphens.
    """
    rows = frappe.get_all(
        "Doc Screenshot",
        filters={"parenttype": "Documentation", "parent": docname},
        fields=[
            "idx", "anchor_id", "title", "image", "display_size",
            "caption_md", "alt_text", "is_og_image"
        ],
        order_by="IFNULL(image_order, 9999), idx",
        ignore_permissions=True,
    )

    folder = f"docs_{slug}_shots"             # e.g. docs_student_shots
    base_url = f"/files/gallery_resized/{folder}"
    manifest: list[dict] = []

    for idx, r in enumerate(rows, start=1):
        anchor = (r.get("anchor_id") or f"fig_{r.get('idx') or idx}").strip()
        bases  = _variant_bases(anchor)
        sizes  = ("large", "medium", "small", "thumb")

        srcset = {}
        for s in sizes:
            url = None
            for base in bases:
                candidate = f"{base_url}/{s}_{base}.webp"
                if _file_exists(candidate):
                    url = candidate
                    break
            if url:
                srcset[s] = url

        original = r.get("image") or ""
        urls = {}
        if srcset:
            urls["webp"] = srcset
        if original:
            urls["original"] = original
            urls.setdefault("fallback", original)

        # Choose a default for {data-size="auto"}: prefer medium, then small, then thumb, else original
        auto_url = (
            srcset.get("medium")
            or srcset.get("small")
            or srcset.get("thumb")
            or original
        )

        manifest.append({
            "fig": anchor,
            "title": r.get("title") or "",
            "alt": r.get("alt_text") or "",
            "caption_md": r.get("caption_md") or "",
            "display_size": (r.get("display_size") or "auto").lower(),
            "srcset": srcset,
            "auto": auto_url,
            "urls": urls,
            "is_og_image": 1 if (r.get("is_og_image") or 0) else 0,
        })

    return manifest


def _select_og_image(shots: list[dict]) -> str | None:
    if not shots:
        return None
    def _candidate(shot):
        return (
            shot.get("auto")
            or (shot.get("urls") or {}).get("original")
            or (shot.get("urls") or {}).get("fallback")
        )

    preferred = next((s for s in shots if s.get("is_og_image")), None)
    if preferred:
        return _candidate(preferred)
    return _candidate(shots[0])


@frappe.whitelist(allow_guest=True)
def fetch_all(language: str | None = None):
    flt = {"status": "Published"}
    if language:
        flt["language"] = language
    subcat_col = _subcategory_column()
    fields = [
        "name","slug","language","title","summary","version",
        "author","published_on","category","doc_order","body_md","modified",
        "seo_title","seo_description","canonical_url","noindex"
    ]
    if subcat_col:
        fields.insert(7, subcat_col)
    docs = frappe.get_all(
        "Documentation",
        filters=flt,
        fields=fields,
        order_by=(f"category, {subcat_col}, doc_order, title" if subcat_col
                  else "category, doc_order, title"),
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
        "author","published_on","category","doc_order","body_md","modified",
        "seo_title","seo_description","canonical_url","noindex"
    ]
    if subcat_col:
        fields.insert(7, f"{subcat_col} as subcategory")

    d = frappe.db.get_value(
        "Documentation",
        {"language": language, "slug": slug, "status": "Published"},
        fields,
        as_dict=True
    )
    if not d:
        frappe.throw("Not Found", frappe.DoesNotExistError)

    _normalize_subcategory(d, subcat_col)
    tags = _load_tags_for([d.get("name")])
    d["tags"] = tags.get(d.get("name"), [])

    # ⬇️ include per-page screenshot manifest
    d["screenshots"] = _shot_manifest_for(d["name"], d["slug"])
    d["og_image"] = _select_og_image(d["screenshots"])


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

@frappe.whitelist(allow_guest=True)
def get_categories(language="en"):
    """Doc Category cards (ordered)."""
    return frappe.get_all(
        "Doc Category",
        fields=["name", "slug", "label", "icon", "description", "cat_order"],
        order_by="IFNULL(cat_order, 9999), label asc",
        limit_page_length=500,
    )

@frappe.whitelist(allow_guest=True)
def get_category(slug: str):
    """Single category by slug."""
    return frappe.db.get_value(
        "Doc Category",
        {"slug": slug},
        ["name", "slug", "label", "icon", "description", "cat_order"],
        as_dict=True,
    )

@frappe.whitelist(allow_guest=True)
def get_docs_in_category(language: str, category_slug: str):
    """
    Docs for (language, category.slug).
    'Documentation.category' is a Link to 'Doc Category' (by name),
    so we resolve slug -> name first.
    """
    cat = frappe.db.get_value("Doc Category", {"slug": category_slug}, "name")
    if not cat:
        return []

    filters = {
        "status": "Published",
        "language": language,
        "category": cat,
    }
    return frappe.get_all(
        "Documentation",
        filters=filters,
        fields=["name", "title", "slug", "summary", "doc_order"],
        order_by="IFNULL(doc_order, 9999), title asc",
        limit_page_length=1000,
    )
