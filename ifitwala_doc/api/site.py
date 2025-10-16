# ifitwala_doc/api/site.py

from __future__ import annotations

import frappe
from frappe import _
from typing import Any, Dict, List, Optional, TypedDict


class SectionDict(TypedDict):
    type: str
    props: Dict[str, Any]


def _hero_props(doc: "Hero Block") -> Dict[str, Any]:
    """Map Hero Block → props expected by your <Hero> Vue."""
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


def _feature_highlights_props(doc: "Feature Highlights") -> Dict[str, Any]:
    """Map Feature Highlights → props for your FeatureHighlights Vue (or a simple cards grid)."""
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
            for r in sorted(doc.items or [], key=lambda x: (x.item_order or 0))
        ],
    }


def _serialize_block(block_dt: str, name: str) -> Optional[SectionDict]:
    """Return normalized {type, props} for supported block doctypes."""
    doc = frappe.get_doc(block_dt, name)

    if block_dt == "Hero Block":
        return {"type": "Hero", "props": _hero_props(doc)}

    if block_dt == "Feature Highlights":
        return {"type": "Feature Highlights", "props": _feature_highlights_props(doc)}

    # not yet supported → skip silently (or raise if you prefer)
    return None


def _seo_payload(page: "Ifitwala Web Page") -> Dict[str, Any]:
    """Basic SEO bundle (meta + OG). Extend later with JSON-LD."""
    return {
        "title": page.title,
        "description": page.meta_description,
        "og_image": page.og_image,
        "canonical_url": page.canonical_url,
    }


@frappe.whitelist(allow_guest=True)
def get_page(slug: str) -> Dict[str, Any]:
    """Return a marketing page and its ordered sections as { type, props }.

    Usage: GET /api/method/ifitwala_doc.api.site.get_page?slug=/
    """
    if not isinstance(slug, str) or not slug:
        frappe.throw(_("slug is required"))

    page = frappe.get_all(
        "Ifitwala Web Page",
        filters={"slug": slug, "is_published": 1},
        fields=["name", "title", "meta_description", "og_image", "canonical_url"],
        limit=1,
    )
    if not page:
        frappe.throw(_("No published page found for slug: {0}").format(slug))

    page = page[0]
    page_doc = frappe.get_doc("Ifitwala Web Page", page.name)

    # gather/serialize sections (ordered)
    sections: List[SectionDict] = []
    for row in sorted(page_doc.sections or [], key=lambda r: r.section_order or 0):
        if not (row.block_doctype and row.block_ref):
            continue
        serialized = _serialize_block(row.block_doctype, row.block_ref)
        if serialized:
            sections.append(serialized)

    return {
        "title": page_doc.title,
        "seo": _seo_payload(page_doc),
        "sections": sections,
    }
