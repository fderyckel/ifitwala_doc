# ifitwala_doc/api/site.py

from __future__ import annotations

from collections.abc import Callable
from typing import Any, Optional, TypedDict
from urllib.parse import urlparse

import frappe
from frappe.model.document import Document
from frappe.utils import format_datetime


class SectionDict(TypedDict):
    type: str
    props: dict[str, Any]
    order: int
    block: dict[str, Any]


class PageSummary(TypedDict):
    name: str
    slug: str
    title: str
    layout: str
    is_published: int
    modified: str | None
    created: str | None


class PagePayload(TypedDict, total=False):
    name: str
    slug: str
    title: str
    layout: str
    seo: dict[str, Any]
    sections: list[SectionDict]
    is_published: int
    modified: str | None
    created: str | None


class StorySummary(TypedDict, total=False):
    name: str
    slug: str
    title: str
    hero_subtitle: str | None
    summary: str | None
    story_type: str | None
    topic: str | None
    author_name: str | None
    author_role: str | None
    published_on: str | None
    estimated_read_minutes: int
    cover_image: str | None
    cover_image_alt: str | None
    featured: int
    featured_priority: int | None


class StoryPayload(StorySummary, total=False):
    status: str | None
    body_md: str | None
    seo_title: str | None
    seo_description: str | None
    canonical_url: str | None
    og_image: str | None
    noindex: int
    key_takeaways: list[dict[str, Any]]
    primary_cta: dict[str, str] | None
    secondary_cta: dict[str, str] | None
    related_stories: list[StorySummary]


THEME_DEFAULTS: dict[str, str] = {
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

BOOK_A_DEMO_PATH = "/book-a-demo/"
BOOK_A_CALL_PATH = "/book-a-call/"
DEMO_LABEL_HINTS = {
    "demo",
    "book a demo",
    "see a live demo",
}
CALL_LABEL_HINTS = {
    "book a call",
    "discuss your systems",
    "talk to us",
}


# -----------------------
# Block mappers
# -----------------------

def _normalize_demo_href(label: Any, href: Any) -> str:
    label_value = (label or "").strip().lower()
    href_value = (href or "").strip()

    if not href_value:
        if label_value in CALL_LABEL_HINTS:
            return BOOK_A_CALL_PATH
        if label_value in DEMO_LABEL_HINTS:
            return BOOK_A_DEMO_PATH
        return href_value

    parsed_path = ""
    try:
        parsed_path = (urlparse(href_value).path or "").strip().rstrip("/")
    except Exception:
        parsed_path = href_value.strip().rstrip("/")

    if label_value in CALL_LABEL_HINTS:
        return BOOK_A_CALL_PATH
    if label_value in DEMO_LABEL_HINTS:
        return BOOK_A_DEMO_PATH
    if parsed_path in {"/call", "/book-call", "/book-a-call", "/contact"}:
        return BOOK_A_CALL_PATH
    if parsed_path in {"/demo", "/book-demo", "/book-a-demo"}:
        return BOOK_A_DEMO_PATH

    return href_value

def _null_last_int_sort_key(value: Any) -> tuple[int, int]:
    if value in (None, ""):
        return (1, 0)
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return (0, 0)
    # Frappe v16 normalizes blank Int fields to 0 on readback, so treat 0 as unset.
    if parsed == 0:
        return (1, 0)
    return (0, parsed)

def _hero_props(doc: Document) -> dict[str, Any]:
    return {
        "eyebrow": getattr(doc, "eyebrow", None),
        "title": doc.heading,
        "subtitle": doc.subheading,
        "bgImage": doc.bg_image,
        "align": (doc.align or "left"),
        "theme": (doc.theme or "light"),
        "actions": [
            {
                "label": r.label,
                "href": _normalize_demo_href(r.label, r.href),
                "variant": (r.variant or "primary"),
            }
            for r in (doc.actions or [])
        ],
    }


def _feature_highlights_props(doc: Document) -> dict[str, Any]:
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


def _trust_logos_props(doc: Document) -> dict[str, Any]:
    rows = sorted(doc.logos or [], key=lambda r: (r.item_order or 0))
    return {
        "title": doc.title,
        "logos": [
            {"src": r.image, "alt": r.alt, "href": r.href, "order": r.item_order}
            for r in rows
        ],
    }


def _longform_props(doc: Document) -> dict[str, Any]:
    sections = sorted(
        doc.sections or [],
        key=lambda r: (
            getattr(r, "section_order", None)
            if getattr(r, "section_order", None) is not None
            else getattr(r, "idx", 0)
        ),
    )
    payload: list[dict[str, Any]] = []
    for row in sections:
        order = getattr(row, "section_order", None)
        if order is None:
            order = getattr(row, "idx", None) or 0

        section_payload: dict[str, Any] = {
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


BlockSerializer = Callable[[Document], dict[str, Any]]

BLOCK_REGISTRY: tuple[tuple[str, tuple[str, ...], BlockSerializer], ...] = (
    ("Hero", ("Hero Block",), _hero_props),
    ("Feature Highlights", ("Feature Highlight", "Feature Highlights"), _feature_highlights_props),
    ("Trust Logos", ("Trust Logos", "Trust Logo", "Trust Logo Group"), _trust_logos_props),
    ("Longform Content", ("Longform Block",), _longform_props),
)

BLOCK_TYPES: dict[str, dict[str, Any]] = {}
BLOCK_DOCTYPES: dict[str, dict[str, Any]] = {}

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


def _serialize_block(block_dt: str, name: str) -> tuple[str, dict[str, Any]] | None:
    index_key = (block_dt or "").strip().lower()
    info = BLOCK_DOCTYPES.get(index_key)
    if not info:
        return None
    doc = frappe.get_doc(block_dt, name)
    return info["type"], info["serializer"](doc)


def _seo_payload(page: Document) -> dict[str, Any]:
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

def _format(value: Any) -> str | None:
    if not value:
        return None
    return format_datetime(value)


def _normalize_slug(value: str | None) -> str:
    if not value:
        return "/"
    raw = str(value).strip()
    if not raw or raw == "/":
        return "/"
    trimmed = raw.strip("/")
    if not trimmed:
        return "/"
    lowered = trimmed.lower()
    if lowered in ("index", "home"):
        return "/"
    if lowered.endswith("/index"):
        trimmed = trimmed[: -len("/index")]
    trimmed = trimmed.strip("/")
    if not trimmed:
        return "/"
    return f"/{trimmed}"


def _slug_candidates(slug: str) -> list[str]:
    normalized = _normalize_slug(slug)
    bare = normalized.lstrip("/")
    candidates: list[str] = [normalized]
    if bare:
        candidates.append(bare)
        candidates.append(bare.rstrip("/"))
    else:
        candidates.extend(["", "home", "index"])

    seen: list[str] = []
    for candidate in candidates:
        key = candidate.strip()
        if not key:
            continue
        if key not in seen:
            seen.append(key)

    if "/" not in seen:
        seen.append("/")
    return seen


def _coerce_int(value: Any) -> int | None:
    try:
        if value is None:
            return None
        return int(value)
    except (TypeError, ValueError):
        return None


def _normalize_story_slug(value: str | None) -> str:
    if not value:
        return ""
    return str(value).strip().strip("/").lower()


def _story_date(value: Any) -> str | None:
    if not value:
        return None
    return str(value)


def _story_takeaways(doc: Document) -> list[dict[str, Any]]:
    rows = list(getattr(doc, "key_takeaways", None) or [])
    rows.sort(
        key=lambda row: (
            _null_last_int_sort_key(getattr(row, "takeaway_order", None)),
            _coerce_int(getattr(row, "idx", None)) or 0,
        )
    )

    payload: list[dict[str, Any]] = []
    for row in rows:
        title = (getattr(row, "title", None) or "").strip()
        detail = (getattr(row, "detail", None) or "").strip()
        if not title and not detail:
            continue
        payload.append(
            {
                "title": title,
                "detail": detail,
                "order": _coerce_int(getattr(row, "takeaway_order", None)) or 0,
            }
        )
    return payload


def _story_cta(label: Any, href: Any) -> dict[str, str] | None:
    label_value = (label or "").strip()
    href_value = _normalize_demo_href(label, href)
    if not label_value or not href_value:
        return None
    return {"label": label_value, "href": href_value}


def _story_summary_payload(item: Any) -> StorySummary:
    title = (getattr(item, "title", None) or "").strip()
    return {
        "name": getattr(item, "name", None),
        "slug": _normalize_story_slug(getattr(item, "slug", None)),
        "title": title,
        "hero_subtitle": getattr(item, "hero_subtitle", None),
        "summary": getattr(item, "summary", None),
        "story_type": getattr(item, "story_type", None),
        "topic": getattr(item, "topic", None),
        "author_name": getattr(item, "author_name", None),
        "author_role": getattr(item, "author_role", None),
        "published_on": _story_date(getattr(item, "published_on", None)),
        "estimated_read_minutes": _coerce_int(getattr(item, "estimated_read_minutes", None)) or 1,
        "cover_image": getattr(item, "cover_image", None),
        "cover_image_alt": getattr(item, "cover_image_alt", None) or title or None,
        "featured": _coerce_int(getattr(item, "featured", None)) or 0,
        "featured_priority": _coerce_int(getattr(item, "featured_priority", None)),
    }


def _story_payload(doc: Document) -> StoryPayload:
    payload: StoryPayload = {
        **_story_summary_payload(doc),
        "status": getattr(doc, "status", None),
        "body_md": getattr(doc, "body_md", None),
        "seo_title": getattr(doc, "seo_title", None),
        "seo_description": getattr(doc, "seo_description", None),
        "canonical_url": getattr(doc, "canonical_url", None),
        "og_image": getattr(doc, "og_image", None) or getattr(doc, "cover_image", None),
        "noindex": _coerce_int(getattr(doc, "noindex", None)) or 0,
        "key_takeaways": _story_takeaways(doc),
        "primary_cta": _story_cta(
            getattr(doc, "primary_cta_label", None),
            getattr(doc, "primary_cta_href", None),
        ),
        "secondary_cta": _story_cta(
            getattr(doc, "secondary_cta_label", None),
            getattr(doc, "secondary_cta_href", None),
        ),
        "related_stories": [],
    }
    return payload


def _story_order_by() -> str:
    return "featured desc, featured_priority asc, published_on desc, modified desc"


def _list_related_stories(doc: Document, limit: int = 3) -> list[StorySummary]:
    filters: dict[str, Any] = {
        "status": "Published",
        "name": ["!=", doc.name],
    }
    if getattr(doc, "topic", None):
        filters["topic"] = doc.topic
    elif getattr(doc, "story_type", None):
        filters["story_type"] = doc.story_type

    rows = frappe.get_all(
        "Ifitwala Story",
        filters=filters,
        fields=[
            "name",
            "slug",
            "title",
            "hero_subtitle",
            "summary",
            "story_type",
            "topic",
            "author_name",
            "author_role",
            "published_on",
            "estimated_read_minutes",
            "cover_image",
            "cover_image_alt",
            "featured",
            "featured_priority",
        ],
        limit_page_length=limit,
        order_by=_story_order_by(),
    )
    return [_story_summary_payload(row) for row in rows]


def _serialize_sections(page_doc: Document) -> list[SectionDict]:
    rows = list(page_doc.sections or [])
    if not rows:
        return []

    sections: list[SectionDict] = []
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
def get_nav(location: str = "Header") -> list[dict[str, Any]]:
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
            "href": _normalize_demo_href(r.get("label"), r.get("href")),
            "target_blank": int(r.get("target_blank") or 0),
            "order": int(r.get("item_order") or 0),
        }
        for r in rows
    ]


@frappe.whitelist(allow_guest=True)
def search_blocks(block_type: str, limit: int = 10) -> list[dict[str, Any]]:
    """Simple helper for editors (find blocks by doctype)."""
    if not block_type:
        return []

    key = block_type.strip().lower()
    target_dt: str | None = None
    block_label: str | None = None

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
    page_doc: Document | None = None
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
def list_pages(include_unpublished: int = 0) -> list[PageSummary]:
    """Return all marketing pages so Astro can determine which routes to pre-render."""
    include_drafts = bool(int(include_unpublished or 0))
    filters: dict[str, Any] = {}
    if not include_drafts:
        filters["is_published"] = 1

    rows = frappe.get_all(
        "Ifitwala Web Page",
        filters=filters,
        fields=["name", "slug", "title", "layout", "is_published", "modified", "creation"],
        order_by="modified desc",
    )

    payload: list[PageSummary] = []
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
def get_site_settings() -> dict[str, Any]:
    ws = frappe.get_single("Ifitwala Website Settings")
    social_links = frappe.get_all(
        "Website Social Link",
        filters={"parent": ws.name, "parenttype": "Ifitwala Website Settings"},
        fields=["platform", "url", "icon", "display_order"],
        order_by="platform asc",
    )
    social_links.sort(
        key=lambda row: (
            _null_last_int_sort_key(row.get("display_order")),
            (row.get("platform") or "").lower(),
        )
    )
    return {
        "site_name": ws.site_name,
        "brand_logo": ws.brand_logo,
        "brand_logo_alt": ws.brand_logo_alt,
        "tagline": ws.tagline,
        "primary_cta_label": ws.primary_cta_label,
        "primary_cta_url": _normalize_demo_href(ws.primary_cta_label, ws.primary_cta_url),
        "footer_md": ws.footer_md,
        "social_links": social_links,
        "social_same_as": [link["url"] for link in social_links if link.get("url")],
        "updated_at": _format(ws.modified),
    }


@frappe.whitelist(allow_guest=True)
def get_theme() -> dict[str, str]:
    """Return design tokens defined in Ifitwala Theme Settings (with safe defaults)."""
    payload: dict[str, str] = {}
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


@frappe.whitelist(allow_guest=True)
def list_stories(
    include_unpublished: int = 0,
    topic: str | None = None,
    story_type: str | None = None,
    limit: int | None = None,
) -> list[StorySummary]:
    filters: dict[str, Any] = {}
    if not bool(int(include_unpublished or 0)):
        filters["status"] = "Published"
    if topic:
        filters["topic"] = topic
    if story_type:
        filters["story_type"] = story_type

    limit_value = _coerce_int(limit) or 100
    rows = frappe.get_all(
        "Ifitwala Story",
        filters=filters,
        fields=[
            "name",
            "slug",
            "title",
            "hero_subtitle",
            "summary",
            "story_type",
            "topic",
            "author_name",
            "author_role",
            "published_on",
            "estimated_read_minutes",
            "cover_image",
            "cover_image_alt",
            "featured",
            "featured_priority",
        ],
        limit_page_length=limit_value,
        order_by=_story_order_by(),
    )
    return [_story_summary_payload(row) for row in rows]


@frappe.whitelist(allow_guest=True)
def get_story(slug: str, include_unpublished: int = 0) -> StoryPayload:
    normalized = _normalize_story_slug(slug)
    filters: dict[str, Any] = {"slug": normalized}
    if not bool(int(include_unpublished or 0)):
        filters["status"] = "Published"

    row = frappe.get_all("Ifitwala Story", filters=filters, fields=["name"], limit=1)
    if not row:
        return {
            "slug": normalized,
            "title": "",
            "key_takeaways": [],
            "related_stories": [],
        }

    doc = frappe.get_doc("Ifitwala Story", row[0].name)
    payload = _story_payload(doc)
    payload["related_stories"] = _list_related_stories(doc)
    return payload


@frappe.whitelist(allow_guest=True)
def get_story_topics(include_unpublished: int = 0) -> list[dict[str, Any]]:
    filters: dict[str, Any] = {}
    if not bool(int(include_unpublished or 0)):
        filters["status"] = "Published"

    rows = frappe.get_all(
        "Ifitwala Story",
        filters=filters,
        fields=["topic"],
        limit_page_length=500,
    )

    counts: dict[str, int] = {}
    for row in rows:
        topic = (getattr(row, "topic", None) or "").strip()
        if not topic:
            continue
        counts[topic] = counts.get(topic, 0) + 1

    return [
        {"topic": topic, "count": count}
        for topic, count in sorted(counts.items(), key=lambda item: (-item[1], item[0].lower()))
    ]
