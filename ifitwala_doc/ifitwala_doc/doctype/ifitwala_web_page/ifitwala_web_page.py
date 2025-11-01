# Copyright (c) 2025, François de Ryckel and contributors
# For license information, please see license.txt

# ifitwala_doc/ifitwala_doc/doctype/ifitwala_web_page/ifitwala_web_page.py

import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe import _

# DEBUG: log route resolution
frappe.log_error(f"WebPage slug={_(lambda self: self.slug) if False else '…'}", "IfitwalaWebPage Debug")

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
        cleaned = (self.slug or "").strip()
        if cleaned and cleaned != "/":
            # remove leading slash but keep intentional segments
            cleaned = cleaned.lstrip("/")
            self.slug = cleaned or "/"
        else:
            self.slug = "/" if cleaned == "/" else cleaned

        if self.slug not in (None, "", "/") and not self.canonical_url:
            self.canonical_url = f"/{self.slug}"

        # Ensure `route` mirrors the slug (with a leading slash)
        normalized_route = (self.slug or "").strip()
        if normalized_route and not normalized_route.startswith("/"):
            normalized_route = f"/{normalized_route}"
        if not normalized_route:
            normalized_route = "/"
        self.route = normalized_route

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
