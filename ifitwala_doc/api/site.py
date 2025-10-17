# ifitwala_doc/api/site.py

from __future__ import annotations

from typing import Any, Dict, List, Optional, TypedDict
import frappe
from frappe import _
from frappe.model.document import Document


class SectionDict(TypedDict):
    type: str
    props: Dict[str, Any]


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


def _serialize_block(block_dt: str, name: str) -> Optional[SectionDict]:
    doc = frappe.get_doc(block_dt, name)
    if block_dt == "Hero Block":
        return {"type": "Hero", "props": _hero_props(doc)}
    if block_dt == "Feature Highlights":
        return {"type": "Feature Highlights", "props": _feature_highlights_props(doc)}
    if block_dt == "Trust Logos":
        return {"type": "Trust Logos", "props": _trust_logos_props(doc)}
    return None


def _seo_payload(page: Document) -> Dict[str, Any]:
    return {
        "title": page.title,
        "description": page.meta_description,
        "og_image": page.og_image,
        "canonical_url": page.canonical_url,
    }


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
        {"label": r["label"], "href": r["href"], "target_blank": int(r.get("target_blank") or 0)}
        for r in rows
    ]


@frappe.whitelist(allow_guest=True)
def search_blocks(block_type: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Simple helper for editors (find blocks by doctype)."""
    if not block_type:
        return []

    dt_map = {
        "Hero": "Hero Block",
        "Feature Highlights": "Feature Highlights",
        "Trust Logos": "Trust Logos",
    }
    dt = dt_map.get(block_type, block_type)

    rows = frappe.get_all(dt, fields=["name"], limit=limit, order_by="modified desc")
    return [{"doctype": dt, "name": r.name} for r in rows]


@frappe.whitelist(allow_guest=True)
def get_page(slug: str = "/") -> Dict[str, Any]:
    """Return the page defined in Ifitwala Web Page (published) with its ordered sections."""
    if not slug:
        slug = "/"

    page_row = frappe.get_all(
        "Ifitwala Web Page",
        filters={"slug": slug, "is_published": 1},
        fields=["name", "title", "meta_description", "og_image", "canonical_url"],
        limit=1,
    )
    if not page_row:
        return {"title": "", "seo": {}, "sections": []}

    page_doc = frappe.get_doc("Ifitwala Web Page", page_row[0].name)

    sections: List[SectionDict] = []
    for row in sorted(page_doc.sections or [], key=lambda r: (r.section_order or 0)):
        if not (row.block_doctype and row.block_ref):
            continue
        packed = _serialize_block(row.block_doctype, row.block_ref)
        if packed:
            sections.append(packed)

    return {
        "title": page_doc.title,
        "seo": _seo_payload(page_doc),
        "sections": sections,
    }


# Optional: expose Single settings to the front-end if you ever need it
@frappe.whitelist(allow_guest=True)
def get_site_settings() -> Dict[str, Any]:
    ws = frappe.get_single("Ifitwala Website Settings")
    return {
        "site_name": ws.site_name,
        "brand_logo": ws.brand_logo,
        "brand_logo_alt": ws.brand_logo_alt,
        "tagline": ws.tagline,
        "primary_cta_label": ws.primary_cta_label,
        "primary_cta_url": ws.primary_cta_url,
        "footer_md": ws.footer_md,
    }
