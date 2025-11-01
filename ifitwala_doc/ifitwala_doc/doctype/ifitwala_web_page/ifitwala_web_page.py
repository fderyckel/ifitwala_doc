# Copyright (c) 2025, François de Ryckel and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe import _

ALLOWED_BLOCK_TYPES = {
    "Hero",
    "Feature Highlights",
    "Trust Logos",
    "Longform Content",
    "Testimonial Group",
    "CTA",
}


class IfitwalaWebPage(WebsiteGenerator):
    website_route_field = "slug"
    website = frappe._dict(
        condition_field="is_published",
        page_title_field="title",
        template="generators/ifitwala_web_page.html",
    )

    def before_validate(self):
        self.slug = self._normalize_slug_value(self.slug)
        if self.slug != "/" and self.canonical_url in (None, "", "/"):
            self.canonical_url = f"/{self.slug}"

    def validate(self):
        self._validate_slug_unique()
        self._validate_has_sections()
        self._validate_sections_order_and_types()

    def _validate_slug_unique(self):
        if not self.slug:
            frappe.throw(_("Slug is required."))
        # normalize common slugs (allow "/" as homepage)
        existing = frappe.db.exists("Ifitwala Web Page", {"slug": self.slug, "name": ["!=", self.name]})
        if existing:
            frappe.throw(_("Slug '{0}' is already used by {1}. Slugs must be unique.").format(self.slug, existing))

    def _validate_has_sections(self):
        if not self.sections:
            frappe.throw(_("Add at least one Section before publishing."))
        if self.is_published and not any(r.block_ref for r in self.sections):
            frappe.throw(_("Each published page must include at least one linked Block."))

    def _validate_sections_order_and_types(self):
        seen = set()
        for row in self.sections:
            if row.section_order in seen:
                frappe.throw(_("Duplicate section_order {0}. Use unique order values.").format(row.section_order))
            seen.add(row.section_order)
            if row.block_type and row.block_type not in ALLOWED_BLOCK_TYPES:
                frappe.throw(_("Block Type '{0}' is not allowed.").format(row.block_type))

    def get_context(self, context):
        context = super().get_context(context)
        context.slug = self.slug
        context.layout = (self.layout or "Standard").lower()
        return context

    @staticmethod
    def _normalize_slug_value(value: str | None) -> str:
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
        return trimmed
