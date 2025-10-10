# no_cache makes edits visible immediately
no_cache = 1

import frappe
from frappe.utils.data import md_to_html

def get_context(context):
    lang = frappe.form_dict.language
    slug = frappe.form_dict.slug

    # Load regardless of status (Draft preview allowed)
    fields = [
        "name","slug","language","title","summary","version",
        "published_on","category","doc_order","body_md","modified"
    ]
    doc = frappe.db.get_value("Documentation", {"language": lang, "slug": slug}, fields, as_dict=True)
    if not doc:
        frappe.throw("Document not found", frappe.DoesNotExistError)

    context.title = f"{doc.title} — Preview"
    context.doc = doc
    context.body_html = md_to_html(doc.body_md or "")
    # use the same base template; content block comes from preview.html
    return context
