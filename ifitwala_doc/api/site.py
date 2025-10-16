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
    """Map Hero Block → props for <Hero> Vue."""
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
    """Map Feature Highlights → props for your Features grid Vue."""
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


def _serialize_block(block_dt: str, name: str) -> Optional[SectionDict]:
    doc = frappe.get_doc(block_dt, name)

    if block_dt == "Hero Block":
        return {"type": "Hero", "props": _hero_props(doc)}

    if block_dt == "Feature Highlights":
        return {"type": "Feature Highlights", "props": _feature_highlights_props(doc)}

    # unsupported blocks are skipped for now
    return None


def _seo_payload(page: Document) -> Dict[str, Any]:
    """Basic SEO bundle (meta + OG). Extend with JSON-LD later."""
    return {
        "title": page.title,
        "description": page.meta_description,
        "og_image": page.og_image,
        "canonical_url": page.canonical_url,
    }


# -----------------------
# Public API
# -----------------------

@frappe.whitelist(allow_guest=True)
def get_page(slug: str) -> Dict[str, Any]:
    """Return a marketing page and its ordered sections as { type, props }.
    GET /api/method/ifitwala_doc.api.site.get_page?slug=/
    """
    if not isinstance(slug, str) or not slug:
        frappe.throw(_("slug is required"))

    page_row = frappe.get_all(
        "Ifitwala Web Page",
        filters={"slug": slug, "is_published": 1},
        fields=["name", "title", "meta_description", "og_image", "canonical_url"],
        limit=1,
    )
    if not page_row:
        frappe.throw(_("No published page found for slug: {0}").format(slug))

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

    # Map friendly names to doctypes you actually created
    dt_map = {
        "Hero": "Hero Block",
        "Feature Highlights": "Feature Highlights",
        # Add more later: "Trust Logos": "Trust Logos", ...
    }
    dt = dt_map.get(block_type, block_type)

    rows = frappe.get_all(
        dt,
        fields=["name"],
        limit=limit,
        order_by="modified desc",
    )
    return [{"doctype": dt, "name": r.name} for r in rows]
