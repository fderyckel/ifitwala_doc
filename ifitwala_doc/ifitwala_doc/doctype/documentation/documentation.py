# Copyright (c) 2025, François de Ryckel and contributors
# For license information, please see license.txt

# ifitwala_doc/ifitwala_doc/doctype/documentation/documentation.py

import os
import re
import hashlib
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import nowdate, get_site_path, cint
from ifitwala_doc.ifitwala_doc.image_utils import slugify, resize_and_save

# ────────────────────────────────────────────────────────────────────────────
# Local helpers (renamed to avoid colliding with image_utils.slugify)
# ────────────────────────────────────────────────────────────────────────────
SLUG_RE = re.compile(r"[^a-z0-9-]+")

def doc_slugify(s: str) -> str:
    """Slug for Documentation URLs (kebab-case, keep hyphens)."""
    base = re.sub(r"\s+", "-", (s or "").strip().lower())
    return SLUG_RE.sub("", base).strip("-")

def _safe_slug(s: str) -> str:
    return doc_slugify(s)

def _checksum_for(file_url: str) -> str | None:
    """MD5 of the public file content; None if not found."""
    if not file_url:
        return None
    path = get_site_path("public", file_url.lstrip("/"))
    if not os.path.exists(path):
        return None
    with open(path, "rb") as fh:
        return hashlib.md5(fh.read()).hexdigest()

def _doctype_folder_for_doc_screens(slug: str) -> str:
    """
    Single-level folder name to match image_utils.resize_and_save behavior.
    Variants will live in: /files/gallery_resized/<folder>/<size>_<base>.webp
    Example: slug='student-attendance' -> 'docs_student-attendance_shots'
    """
    return f"docs_{slug}_shots"

VALID_SIZES = {"auto", "large", "medium", "small", "thumb"}
SIZE_WIDTHS = {"large": 1280, "medium": 960, "small": 640, "thumb": 320}


def _ensure_flags_container(row):
    if getattr(row, "flags", None) is None:
        row.flags = frappe._dict()
    return row.flags


def _has_generated_variants_field(row) -> bool:
    meta = getattr(row, "meta", None)
    get_field = getattr(meta, "get_field", None)
    return bool(callable(get_field) and get_field("generated_variants"))


def _get_generated_variants(row) -> int:
    if not row:
        return 0
    if _has_generated_variants_field(row):
        try:
            return cint(row.get("generated_variants") or 0)
        except Exception:
            return 0
    flags = _ensure_flags_container(row)
    return cint(flags.get("generated_variants") or 0)


def _set_generated_variants(row, value: int):
    if not row:
        return
    value = cint(value)
    if _has_generated_variants_field(row):
        row.set("generated_variants", value)
    else:
        flags = _ensure_flags_container(row)
        flags.generated_variants = value


def _log_missing_generated_variants_once(docname: str):
    if getattr(frappe.flags, "_missing_generated_variants_logged", False):
        return
    frappe.flags._missing_generated_variants_logged = True
    frappe.log_error(
        f"'generated_variants' field missing on Doc Screenshot rows for Documentation {docname}",
        "Doc Screenshot Schema Mismatch"
    )


# ────────────────────────────────────────────────────────────────────────────
# Document
# ────────────────────────────────────────────────────────────────────────────
class Documentation(Document):
    def before_insert(self):
        if not self.slug and self.title:
            self.slug = doc_slugify(self.title)
        self.slug = doc_slugify(self.slug)

    def validate(self):
        # normalize slug + publish date
        self.slug = doc_slugify(self.slug)
        if self.status == "Published" and not self.published_on:
            self.published_on = nowdate()

        # unique per (language, slug)
        if frappe.db.exists(
            "Documentation",
            {"name": ["!=", self.name], "language": self.language, "slug": self.slug},
        ):
            frappe.throw(_("Slug already in use for language '{0}': {1}")
                         .format(self.language, self.slug))

        # subcategory must belong to category (guard)
        if getattr(self, "subcategory", None) and self.category:
            parent = frappe.db.get_value("Doc Subcategory", self.subcategory, "category")
            if parent and parent != self.category:
                frappe.throw(_("Selected Subcategory does not belong to the chosen Category"))

        # child table validations (screenshots)
        self._validate_screenshots_and_compute_checksums()

    def before_save(self):
        self.last_edited_by = frappe.session.user

        # Decide whether to trigger a rebuild
        old = self.get_doc_before_save()
        if not old:
            self.flags.trigger_docs_build = (self.status == "Published")
        else:
            became_published = (old.status != "Published" and self.status == "Published")
            updated_published = (
                old.status == "Published" and self.status == "Published" and (
                    (old.title != self.title) or
                    (old.summary != self.summary) or
                    (old.body_md != self.body_md) or
                    (old.language != self.language) or
                    (old.slug != self.slug) or
                    (old.category != self.category) or
                    (getattr(old, "subcategory", None) != getattr(self, "subcategory", None)) or
                    (old.doc_order != self.doc_order)
                )
            )
            self.flags.trigger_docs_build = became_published or updated_published

    def on_update(self):
        # keep your existing build ping
        if getattr(self.flags, "trigger_docs_build", False):
            from ifitwala_doc.ifitwala_doc.published_utils import ping_build
            frappe.enqueue(ping_build, queue="short")

        # queue variant generation for any screenshot rows that need it
        self._enqueue_variant_generation_if_needed()

    # ----------------------------------------------------------------------
    # Screenshots validation & jobs
    # ----------------------------------------------------------------------
    def _validate_screenshots_and_compute_checksums(self):
        """Enforce required fields, uniqueness, size enum; compute checksums."""
        anchors = set()
        for row in (self.screenshots or []):
            # required
            if not getattr(row, "anchor_id", None):
                frappe.throw(_("Row #{0}: Anchor ID is required").format(row.idx))
            if not getattr(row, "image", None):
                frappe.throw(_("Row #{0}: Screenshot is required").format(row.idx))
            if not getattr(row, "alt_text", None):
                frappe.throw(_("Row #{0}: Alt Text is required").format(row.idx))

            # unique anchor per doc (case-insensitive)
            key = row.anchor_id.strip().lower()
            if key in anchors:
                frappe.throw(_("Duplicate Anchor ID: {0} (row #{1})").format(row.anchor_id, row.idx))
            anchors.add(key)

            # size option
            size = (row.display_size or "auto").strip().lower()
            if size not in VALID_SIZES:
                frappe.throw(_("Row #{0}: Invalid Display Size").format(row.idx))

            # compute checksum; if changed, reset variants
            cs = _checksum_for(row.image)
            if cs and cs != (row.checksum or ""):
                row.checksum = cs
                _set_generated_variants(row, 0)  # force regeneration when the image changes

    def _enqueue_variant_generation_if_needed(self):
        for row in (self.screenshots or []):
            generated_variants = _get_generated_variants(row)
            if row.image and not generated_variants:
                if not _has_generated_variants_field(row):
                    _log_missing_generated_variants_once(self.name)
                frappe.enqueue(
                    "ifitwala_doc.ifitwala_doc.doctype.documentation.documentation._generate_row_variants",
                    queue="short",
                    docname=self.name,
                    row_idx=row.idx
                )


# ────────────────────────────────────────────────────────────────────────────
# Worker: generate resized WebP variants for a single screenshot row
# ────────────────────────────────────────────────────────────────────────────
@frappe.whitelist()
def _generate_row_variants(docname: str, row_idx: int):
    """
    For the given Documentation doc + child row index:
      - read original image
      - write large/medium/small/thumb .webp into gallery_resized/<folder>/
      - register File rows (handled by image_utils.resize_and_save)
      - mark row.generated_variants = 1
    """
    doc = frappe.get_doc("Documentation", docname)
    slug = doc.slug or _safe_slug(doc.title)
    doctype_folder = _doctype_folder_for_doc_screens(slug)  # single-level folder name

    # locate the row
    row = next((r for r in (doc.screenshots or []) if int(r.idx) == int(row_idx)), None)
    if not row or not row.image:
        return

    # resolve original File + path
    filedoc = frappe.get_doc("File", {"file_url": row.image})
    original_path = get_site_path("public", filedoc.file_url.lstrip("/"))
    if not os.path.exists(original_path):
        frappe.log_error(f"Original not found: {original_path}", "Doc Screenshot Variants")
        return

    # base filename uses YOUR image_utils.slugify (underscores)
    base_name = slugify(row.anchor_id or f"fig_{row.idx}")

    # generate four sizes (webp) via your util
    for size_label, width in SIZE_WIDTHS.items():
        try:
            resize_and_save(
                doc=filedoc,                    # keep attached_to_* linkage
                original_path=original_path,
                base_filename=base_name,
                doctype_folder=doctype_folder,  # e.g., docs_<slug>_shots
                size_label=size_label,          # large|medium|small|thumb
                width=width,
                quality=80,
            )
        except Exception as e:
            frappe.log_error(f"{e}", "Doc Screenshot Resize Error")

    # mark done
    _set_generated_variants(row, 1)
    if _has_generated_variants_field(row):
        # keep checksum as-is (already computed in validate)
        doc.save(ignore_permissions=True)
    else:
        _log_missing_generated_variants_once(docname)
