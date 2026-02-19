# no_cache makes edits visible immediately
no_cache = 1

import re
import frappe
from frappe.utils.data import md_to_html
from markupsafe import Markup


_CALLOUT_RE = re.compile(
    r"(?:&(?:amp;)?lt;|<)Callout\b([^>]*?)(?:&(?:amp;)?gt;|>)"
    r"([\s\S]*?)"
    r"(?:&(?:amp;)?lt;|<)\/Callout(?:&(?:amp;)?gt;|>)",
    re.IGNORECASE,
)
_ATTR_RE = re.compile(r"([^\s=]+)\s*=\s*(\"(?:[^\"]*)\"|'(?:[^']*)')")
_ALLOWED_TYPES = {"info", "warning", "tip", "note"}
_CALLOUT_COLORS = {
    "info": {"bg": "rgba(43, 123, 187, 0.08)", "border": "rgba(43, 123, 187, 0.72)"},
    "warning": {"bg": "rgba(208, 135, 0, 0.08)", "border": "rgba(208, 135, 0, 0.72)"},
    "tip": {"bg": "rgba(41, 159, 101, 0.08)", "border": "rgba(41, 159, 101, 0.72)"},
    "note": {"bg": "rgba(148, 163, 184, 0.12)", "border": "rgba(148, 163, 184, 0.8)"},
}


def _decode_entities(value: str | None) -> str:
    current = value or ""
    for _ in range(4):
        decoded = (
            current.replace("&amp;", "&")
            .replace("&lt;", "<")
            .replace("&gt;", ">")
            .replace("&quot;", '"')
            .replace("&#39;", "'")
        )
        if decoded == current:
            return decoded
        current = decoded
    return current


def _parse_attrs(raw_attrs: str) -> dict[str, str]:
    attrs: dict[str, str] = {}
    source = _decode_entities(raw_attrs)
    for match in _ATTR_RE.finditer(source):
        key = match.group(1)
        quoted = match.group(2)
        attrs[key] = _decode_entities(quoted[1:-1])
    return attrs


def _render_doc_markdown(md: str | None) -> str:
    source = md or ""
    callouts = []

    def _replace(match: re.Match) -> str:
        idx = len(callouts)
        placeholder = f'__CALLOUT_PLACEHOLDER_{idx}__'
        callouts.append(
            {
                "placeholder": placeholder,
                "attrs": _parse_attrs(match.group(1) or ""),
                "body": (match.group(2) or "").strip(),
            }
        )
        return f"\n\n<div data-callout-placeholder=\"{placeholder}\"></div>\n\n"

    rendered = _CALLOUT_RE.sub(_replace, source)
    html = str(md_to_html(rendered))

    for callout in callouts:
        type_raw = (callout["attrs"].get("type") or "info").strip().lower()
        callout_type = type_raw if type_raw in _ALLOWED_TYPES else "info"
        title = (callout["attrs"].get("title") or "").strip()
        body_html = _render_doc_markdown(callout["body"]).strip()
        palette = _CALLOUT_COLORS.get(callout_type, _CALLOUT_COLORS["info"])
        title_html = (
            f'<div class="docs-callout-title" style="font-weight:600;margin-bottom:0.25rem;">'
            f"{frappe.utils.escape_html(title)}</div>"
            if title
            else ""
        )
        callout_html = (
            f'<div class="docs-callout docs-callout-{callout_type}" data-callout-type="{callout_type}" '
            f'style="border-left:4px solid {palette["border"]};background:{palette["bg"]};'
            f'border-radius:0.5rem;padding:0.75rem 0.9rem;margin:1rem 0;">'
            f'{title_html}<div class="docs-callout-body">{body_html}</div></div>'
        )
        placeholder = f'<div data-callout-placeholder="{callout["placeholder"]}"></div>'
        html = html.replace(f"<p>{placeholder}</p>", callout_html).replace(placeholder, callout_html)

    return html

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
    context.body_html = Markup(_render_doc_markdown(doc.body_md or ""))
    # use the same base template; content block comes from preview.html
    return context
