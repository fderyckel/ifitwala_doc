# Copyright (c) 2025, François de Ryckel and contributors
# For license information, please see license.txt

# ifitwala_doc/ifitwala_doc/doctype/documentation/documentation.py

import re, frappe
from frappe.model.document import Document
from frappe.utils import nowdate

SLUG_RE = re.compile(r"[^a-z0-9-]+")

def slugify(s: str) -> str:
    base = re.sub(r"\s+", "-", (s or "").strip().lower())
    return SLUG_RE.sub("", base).strip("-")

class Documentation(Document):
    def before_insert(self):
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        self.slug = slugify(self.slug)

    def validate(self):
        self.slug = slugify(self.slug)
        if self.status == "Published" and not self.published_on:
            self.published_on = nowdate()

        # unique per (language, slug)
        if frappe.db.exists(
            "Documentation",
            {"name": ["!=", self.name], "language": self.language, "slug": self.slug}
        ):
            frappe.throw(f"Slug already in use for language '{self.language}': {self.slug}")

        # subcategory must belong to category (guard)
        if self.sub_category and self.category:
            parent = frappe.db.get_value("Doc Subcategory", self.sub_category, "category")
            if parent and parent != self.category:
                frappe.throw("Selected Subcategory does not belong to the chosen Category")

    def before_save(self):
        self.last_edited_by = frappe.session.user
        # Decide whether to trigger a rebuild
        old = self.get_doc_before_save()
        if not old:
            # new doc
            self.flags.trigger_docs_build = (self.status == "Published")
        else:
            became_published = (old.status != "Published" and self.status == "Published")
            updated_published = (old.status == "Published" and self.status == "Published" and (
                (old.title != self.title) or
                (old.summary != self.summary) or
                (old.body_md != self.body_md) or
                (old.language != self.language) or
                (old.slug != self.slug) or
                (old.category != self.category) or
                (old.sub_category != self.sub_category) or
                (old.doc_order != self.doc_order)
            ))
            self.flags.trigger_docs_build = became_published or updated_published

    def on_update(self):
        if getattr(self.flags, "trigger_docs_build", False):
            from ifitwala_doc.ifitwala_doc.published_utils import ping_build
            # enqueue so the form stays snappy
            frappe.enqueue(ping_build, queue="short")
