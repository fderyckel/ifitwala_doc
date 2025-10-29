# ifitwala_doc/api/site.py

from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, Tuple, TypedDict
import frappe
from frappe.model.document import Document
from frappe.utils import format_datetime


class SectionDict(TypedDict):
    type: str
    props: Dict[str, Any]
    order: int
    block: Dict[str, Any]


class PageSummary(TypedDict):
    name: str
    slug: str
    title: str
    layout: str
    is_published: int
    modified: Optional[str]
    created: Optional[str]


class PagePayload(TypedDict, total=False):
    name: str
    slug: str
    title: str
    layout: str
    seo: Dict[str, Any]
    sections: List[SectionDict]
    is_published: int
    modified: Optional[str]
    created: Optional[str]


THEME_DEFAULTS: Dict[str, str] = {
    "ink_color": "#0F172A",
    "slate_color": "#475569",
    "canopy_color": "#12563A",
    "leaf_color": "#2F855A",
    "moss_color": "#A6D6B1",
    "sky_color": "#E6F3F9",
    "sand_color": "#F4EFE7",
    "border_color": "#E2E8F0",
    "radius_lg": "1rem",
    "radius_xl": "1.25rem",
    "shadow_soft": "0 6px 20px rgba(15, 23, 42, 0.06)",
    "shadow_strong": "0 12px 32px rgba(15, 23, 42, 0.1)",
    "focus_ring": "0 0 0 3px rgba(47, 133, 90, 0.35)",
}


# -----------------------
# Block mappers
# -----------------------

def _hero_props(doc: Document) -> Dict[str, Any]:
    return {
        "title": doc.heading,
        "subtitle": doc.subheading,
        "bgImage": doc.bg_image,
        "align": (doc.align or "left"),
        "theme": (doc.theme or "light"),
        "actions": [
            {"label": r.label, "href": r.href, "variant": (r.variant or "primary")}
            for r in (doc.actions or [])
        ],
    }


def _feature_highlights_props(doc: Document) -> Dict[str, Any]:
    items = sorted(doc.items or [], key=lambda x: (x.item_order or 0))
    return {
        "eyebrow": doc.eyebrow,
        "intro": doc.intro,
        "items": [
            {
                "order": r.item_order,
                "icon": r.icon_name,
                "label": r.label,
                "description": r.description,
                "href": r.href,
            }
            for r in items
        ],
    }


def _trust_logos_props(doc: Document) -> Dict[str, Any]:
    rows = sorted(doc.logos or [], key=lambda r: (r.item_order or 0))
    return {
        "title": doc.title,
        "logos": [
            {"src": r.image, "alt": r.alt, "href": r.href, "order": r.item_order}
            for r in rows
        ],
    }


def _longform_props(doc: Document) -> Dict[str, Any]:
    sections = sorted(
        doc.sections or [],
        key=lambda r: (
            getattr(r, "section_order", None)
            if getattr(r, "section_order", None) is not None
            else getattr(r, "idx", 0)
        ),
    )
    payload: List[Dict[str, Any]] = []
    for row in sections:
        order = getattr(row, "section_order", None)
        if order is None:
            order = getattr(row, "idx", None) or 0

        section_payload: Dict[str, Any] = {
            "order": order,
            "layout": (getattr(row, "layout", None) or "text"),
            "style": (getattr(row, "style", None) or getattr(doc, "background", None) or "default"),
            "anchor": getattr(row, "anchor", None),
            "eyebrow": getattr(row, "eyebrow", None),
            "heading": getattr(row, "heading", None),
            "subheading": getattr(row, "subheading", None),
            "body": getattr(row, "body", None),
            "image": getattr(row, "image", None),
            "imageAlt": getattr(row, "image_alt", None),
            "imageCaption": getattr(row, "image_caption", None),
        }

        cta_label = getattr(row, "cta_label", None)
        cta_href = getattr(row, "cta_href", None)
        if cta_label and cta_href:
            section_payload["cta"] = {
                "label": cta_label,
                "href": cta_href,
                "variant": getattr(row, "cta_variant", None) or "link",
            }

        payload.append(section_payload)

    return {
        "title": getattr(doc, "title", None),
        "lede": getattr(doc, "lede", None),
        "background": getattr(doc, "background", None) or "default",
        "seo": {
            "title": getattr(doc, "seo_title", None),
            "description": getattr(doc, "seo_description", None),
            "keywords": getattr(doc, "seo_keywords", None),
            "canonical": getattr(doc, "seo_canonical_override", None),
            "ogTitle": getattr(doc, "og_title", None),
            "ogDescription": getattr(doc, "og_description", None),
            "ogImage": getattr(doc, "og_image", None),
            "ogImageAlt": getattr(doc, "og_image_alt", None),
            "ogType": getattr(doc, "og_type", None),
        },
        "sections": payload,
    }


BlockSerializer = Callable[[Document], Dict[str, Any]]

BLOCK_REGISTRY: Tuple[Tuple[str, Tuple[str, ...], BlockSerializer], ...] = (
    ("Hero", ("Hero Block",), _hero_props),
    ("Feature Highlights", ("Feature Highlight", "Feature Highlights"), _feature_highlights_props),
    ("Trust Logos", ("Trust Logos", "Trust Logo", "Trust Logo Group"), _trust_logos_props),
    ("Longform Content", ("Longform Block",), _longform_props),
)

BLOCK_TYPES: Dict[str, Dict[str, Any]] = {}
BLOCK_DOCTYPES: Dict[str, Dict[str, Any]] = {}

for block_type, doctypes, serializer in BLOCK_REGISTRY:
    key = block_type.lower()
    BLOCK_TYPES[key] = {
        "type": block_type,
        "serializer": serializer,
        "doctypes": doctypes,
    }
    for dt in doctypes:
        dkey = dt.lower()
        BLOCK_DOCTYPES[dkey] = {
            "type": block_type,
            "serializer": serializer,
            "doctype": dt,
        }


def _serialize_block(block_dt: str, name: str) -> Optional[Tuple[str, Dict[str, Any]]]:
    index_key = (block_dt or "").strip().lower()
    info = BLOCK_DOCTYPES.get(index_key)
    if not info:
        return None
    doc = frappe.get_doc(block_dt, name)
    return info["type"], info["serializer"](doc)


def _seo_payload(page: Document) -> Dict[str, Any]:
    return {
        "title": page.seo_title or page.title,
        "description": page.seo_description or page.meta_description,
        "canonical_url": page.canonical_url,
        "meta_description": page.meta_description,
        "seo_title": page.seo_title,
        "seo_description": page.seo_description,
        "seo_keywords": page.seo_keywords,
        "seo_noindex": int(getattr(page, "seo_noindex", 0) or 0),
        "seo_nofollow": int(getattr(page, "seo_nofollow", 0) or 0),
        "og_image": page.og_image,
        "og_title": page.og_title,
        "og_description": page.og_description,
        "og_image_alt": page.og_image_alt,
        "og_type": page.og_type or "website",
    }


# -----------------------
# Helpers
# -----------------------

def _format(value: Any) -> Optional[str]:
    if not value:
        return None
    return format_datetime(value)


def _normalize_slug(value: Optional[str]) -> str:
    if not value:
        return "/"
    raw = str(value).strip()
    if not raw or raw == "/":
        return "/"
    trimmed = raw.strip("/")
    if not trimmed:
        return "/"
    return f"/{trimmed}"


def _slug_candidates(slug: str) -> List[str]:
    normalized = _normalize_slug(slug)
    bare = normalized.lstrip("/")
    candidates: List[str] = [normalized]
    if bare:
        candidates.append(bare)
        candidates.append(bare.rstrip("/"))
    else:
        candidates.extend(["", "home", "index"])

    seen: List[str] = []
    for candidate in candidates:
        key = candidate.strip()
        if not key:
            continue
        if key not in seen:
            seen.append(key)

    if "/" not in seen:
        seen.insert(0, "/")
    return seen


def _coerce_int(value: Any) -> Optional[int]:
    try:
        if value is None:
            return None
        return int(value)
    except (TypeError, ValueError):
        return None


def _serialize_sections(page_doc: Document) -> List[SectionDict]:
    rows = list(page_doc.sections or [])
    if not rows:
        return []

    sections: List[SectionDict] = []
    for idx, row in enumerate(rows, start=1):
        block_info = (
            _serialize_block(row.block_doctype, row.block_ref)
            if (row.block_doctype and row.block_ref)
            else None
        )
        if not block_info:
            continue

        type_name, props = block_info
        order = _coerce_int(getattr(row, "section_order", None))
        if order is None:
            order = _coerce_int(getattr(row, "idx", None))
        if order is None:
            order = idx

        sections.append(
            {
                "type": type_name,
                "props": props,
                "order": order,
                "block": {
                    "doctype": row.block_doctype,
                    "name": row.block_ref,
                    "label": getattr(row, "block_type", None) or type_name,
                },
            }
        )

    sections.sort(key=lambda item: item.get("order", 0))
    return sections


# -----------------------
# Public API (whitelisted → /api/method/...)
# -----------------------

@frappe.whitelist(allow_guest=True)
def get_nav(location: str = "Header") -> List[Dict[str, Any]]:
    """Return a flat nav for a given location (Header|Footer|Secondary)."""
    if not location:
        location = "Header"

    parents = frappe.get_all(
        "Navigation Menu",
        filters={"location": location, "is_enabled": 1},
        fields=["name"],
        limit=1,
        order_by="modified desc",
    )
    if not parents:
        return []

    rows = frappe.get_all(
        "Navigation Menu Item",
        filters={"parent": parents[0].name, "parenttype": "Navigation Menu"},
        fields=["label", "href", "item_order", "target_blank"],
        order_by="item_order asc",
    )
    return [
        {
            "label": r["label"],
            "href": r["href"],
            "target_blank": int(r.get("target_blank") or 0),
            "order": int(r.get("item_order") or 0),
        }
        for r in rows
    ]


@frappe.whitelist(allow_guest=True)
def search_blocks(block_type: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Simple helper for editors (find blocks by doctype)."""
    if not block_type:
        return []

    key = block_type.strip().lower()
    target_dt: Optional[str] = None
    block_label: Optional[str] = None

    type_entry = BLOCK_TYPES.get(key)
    if type_entry:
        target_dt = type_entry["doctypes"][0]
        block_label = type_entry["type"]
    else:
        doc_entry = BLOCK_DOCTYPES.get(key)
        if doc_entry:
            target_dt = doc_entry["doctype"]
            block_label = doc_entry["type"]
        else:
            target_dt = block_type
            block_label = block_type

    try:
        rows = frappe.get_all(
            target_dt,
            fields=["name", "modified"],
            limit=limit,
            order_by="modified desc",
        )
    except Exception:
        return []

    return [
        {
            "doctype": target_dt,
            "name": r.name,
            "type": block_label,
            "modified": r.get("modified"),
        }
        for r in rows
    ]


@frappe.whitelist(allow_guest=True)
def get_page(slug: str = "/", include_unpublished: int = 0) -> PagePayload:
    """Return the page defined in Ifitwala Web Page with its ordered sections."""
    candidates = _slug_candidates(slug or "/")
    page_doc: Optional[Document] = None
    include_drafts = bool(int(include_unpublished or 0))

    for candidate in candidates:
        filters = {"slug": candidate}
        if not include_drafts:
            filters["is_published"] = 1
        row = frappe.get_all(
            "Ifitwala Web Page",
            filters=filters,
            fields=["name"],
            limit=1,
        )
        if row:
            page_doc = frappe.get_doc("Ifitwala Web Page", row[0].name)
            break

    normalized = _normalize_slug(slug)
    if not page_doc:
        return {
            "slug": normalized,
            "title": "",
            "seo": {},
            "sections": [],
        }

    sections = _serialize_sections(page_doc)
    page_slug = _normalize_slug(page_doc.slug)

    return {
        "name": page_doc.name,
        "slug": page_slug,
        "title": page_doc.title,
        "layout": page_doc.layout or "Landing",
        "is_published": int(page_doc.is_published or 0),
        "seo": _seo_payload(page_doc),
        "sections": sections,
        "modified": _format(page_doc.modified),
        "created": _format(page_doc.creation),
    }


@frappe.whitelist(allow_guest=True)
def list_pages(include_unpublished: int = 0) -> List[PageSummary]:
    """Return all marketing pages so Astro can determine which routes to pre-render."""
    include_drafts = bool(int(include_unpublished or 0))
    filters: Dict[str, Any] = {}
    if not include_drafts:
        filters["is_published"] = 1

    rows = frappe.get_all(
        "Ifitwala Web Page",
        filters=filters,
        fields=["name", "slug", "title", "layout", "is_published", "modified", "creation"],
        order_by="modified desc",
    )

    payload: List[PageSummary] = []
    seen_slugs: set[str] = set()
    for row in rows:
        slug_value = _normalize_slug(row.slug)
        if not slug_value or slug_value in seen_slugs:
            continue
        seen_slugs.add(slug_value)
        payload.append(
            {
                "name": row.name,
                "slug": slug_value,
                "title": row.title,
                "layout": row.layout or "Landing",
                "is_published": int(row.is_published or 0),
                "modified": _format(row.modified),
                "created": _format(row.creation),
            }
        )

    payload.sort(key=lambda item: (0 if item["slug"] == "/" else 1, item["slug"]))
    return payload


# Optional: expose Single settings to the front-end if you ever need it
@frappe.whitelist(allow_guest=True)
def get_site_settings() -> Dict[str, Any]:
    ws = frappe.get_single("Ifitwala Website Settings")
    social_links = frappe.get_all(
        "Website Social Link",
        filters={"parent": ws.name, "parenttype": "Ifitwala Website Settings"},
        fields=["platform", "url", "icon", "display_order"],
        order_by="IFNULL(display_order, 9999), platform asc",
    )
    return {
        "site_name": ws.site_name,
        "brand_logo": ws.brand_logo,
        "brand_logo_alt": ws.brand_logo_alt,
        "tagline": ws.tagline,
        "primary_cta_label": ws.primary_cta_label,
        "primary_cta_url": ws.primary_cta_url,
        "footer_md": ws.footer_md,
        "social_links": social_links,
        "social_same_as": [link["url"] for link in social_links if link.get("url")],
        "updated_at": _format(ws.modified),
    }


@frappe.whitelist(allow_guest=True)
def get_theme() -> Dict[str, str]:
    """Return design tokens defined in Ifitwala Theme Settings (with safe defaults)."""
    payload: Dict[str, str] = {}
    doc = None
    try:
        doc = frappe.get_single("Ifitwala Theme Settings")
    except Exception:
        doc = None

    for key, default in THEME_DEFAULTS.items():
        value = None
        if doc:
            try:
                value = doc.get(key)
            except Exception:
                value = None
        payload[key] = (value or default).strip() if isinstance(value, str) else default

    return payload
