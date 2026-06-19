# Copyright (c) 2026, François de Ryckel and contributors
# For license information, please see license.txt

import math
import re

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import cint, nowdate

SLUG_RE = re.compile(r"[^a-z0-9-]+")
WORD_RE = re.compile(r"\b[\w'-]+\b")



def story_slugify(value: str | None) -> str:
    base = re.sub(r"\s+", "-", (value or "").strip().lower())
    return SLUG_RE.sub("", base).strip("-")



def _read_minutes(*parts: str | None) -> int:
    words = 0
    for part in parts:
        if not part:
            continue
        words += len(WORD_RE.findall(str(part)))
    if words <= 0:
        return 1
    return max(1, math.ceil(words / 220))



def _serialize_takeaways(rows) -> list[dict[str, str | int]]:
    payload = []
    ordered = sorted(
        list(rows or []),
        key=lambda row: (
            1 if cint(getattr(row, "takeaway_order", None) or 0) == 0 else 0,
            cint(getattr(row, "takeaway_order", None) or 0),
            cint(getattr(row, "idx", None) or 0),
        ),
    )
    for row in ordered:
        title = (getattr(row, "title", None) or "").strip()
        detail = (getattr(row, "detail", None) or "").strip()
        if not title and not detail:
            continue
        payload.append(
            {
                "title": title,
                "detail": detail,
                "order": cint(getattr(row, "takeaway_order", None) or 0),
            }
        )
    return payload



def _snapshot(doc: Document) -> dict:
    return {
        "title": doc.title,
        "slug": doc.slug,
        "hero_subtitle": doc.hero_subtitle,
        "summary": doc.summary,
        "status": doc.status,
        "published_on": str(doc.published_on or ""),
        "story_type": doc.story_type,
        "topic": doc.topic,
        "featured": cint(doc.featured or 0),
        "featured_priority": cint(doc.featured_priority or 0),
        "author_name": doc.author_name,
        "author_role": doc.author_role,
        "estimated_read_minutes": cint(doc.estimated_read_minutes or 0),
        "cover_image": doc.cover_image,
        "cover_image_alt": doc.cover_image_alt,
        "body_md": doc.body_md,
        "primary_cta_label": doc.primary_cta_label,
        "primary_cta_href": doc.primary_cta_href,
        "secondary_cta_label": doc.secondary_cta_label,
        "secondary_cta_href": doc.secondary_cta_href,
        "seo_title": doc.seo_title,
        "seo_description": doc.seo_description,
        "canonical_url": doc.canonical_url,
        "og_image": doc.og_image,
        "noindex": cint(doc.noindex or 0),
        "key_takeaways": _serialize_takeaways(getattr(doc, "key_takeaways", None)),
    }


class IfitwalaStory(Document):
    def before_insert(self):
        if not self.slug and self.title:
            self.slug = story_slugify(self.title)
        self.slug = story_slugify(self.slug)

    def validate(self):
        self.slug = story_slugify(self.slug or self.title)
        if not self.slug:
            frappe.throw(_("Slug is required."))

        existing = frappe.db.exists(
            "Ifitwala Story",
            {"slug": self.slug, "name": ["!=", self.name]},
        )
        if existing:
            frappe.throw(_("Slug '{0}' is already in use.").format(self.slug))

        if self.status == "Published" and not self.published_on:
            self.published_on = nowdate()

        if self.cover_image and not self.cover_image_alt:
            self.cover_image_alt = self.title

        self.estimated_read_minutes = _read_minutes(
            self.hero_subtitle,
            self.summary,
            self.body_md,
        )

        self._validate_cta_pair("Primary CTA", "primary_cta_label", "primary_cta_href")
        self._validate_cta_pair("Secondary CTA", "secondary_cta_label", "secondary_cta_href")

    def before_save(self):
        old = self.get_doc_before_save()
        if not old:
            self.flags.trigger_story_build = self.status == "Published"
            return

        was_published = old.status == "Published"
        is_published = self.status == "Published"
        public_changed = _snapshot(old) != _snapshot(self)
        self.flags.trigger_story_build = (was_published != is_published) or (is_published and public_changed)

    def on_update(self):
        if getattr(self.flags, "trigger_story_build", False):
            from ifitwala_doc.ifitwala_doc.published_utils import ping_build

            frappe.enqueue(ping_build, queue="short")

    def _validate_cta_pair(self, label: str, label_field: str, href_field: str):
        cta_label = (getattr(self, label_field, None) or "").strip()
        cta_href = (getattr(self, href_field, None) or "").strip()
        if cta_label and not cta_href:
            frappe.throw(_("{0} URL is required when a label is set.").format(label))
        if cta_href and not cta_label:
            frappe.throw(_("{0} label is required when a URL is set.").format(label))
