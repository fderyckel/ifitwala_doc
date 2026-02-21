# no_cache makes edits visible immediately
no_cache = 1

import re
from urllib.parse import quote
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
_STEPS_RE = re.compile(
    r"(?:&(?:amp;)?lt;|<)Steps\b([^>]*?)(?:&(?:amp;)?gt;|>)"
    r"([\s\S]*?)"
    r"(?:&(?:amp;)?lt;|<)\/Steps(?:&(?:amp;)?gt;|>)",
    re.IGNORECASE,
)
_STEP_RE = re.compile(
    r"(?:&(?:amp;)?lt;|<)Step\b([^>]*?)(?:&(?:amp;)?gt;|>)"
    r"([\s\S]*?)"
    r"(?:&(?:amp;)?lt;|<)\/Step(?:&(?:amp;)?gt;|>)",
    re.IGNORECASE,
)
_DODONT_RE = re.compile(
    r"(?:&(?:amp;)?lt;|<)DoDont\b([^>]*?)(?:&(?:amp;)?gt;|>)"
    r"([\s\S]*?)"
    r"(?:&(?:amp;)?lt;|<)\/DoDont(?:&(?:amp;)?gt;|>)",
    re.IGNORECASE,
)
_DO_RE = re.compile(
    r"(?:&(?:amp;)?lt;|<)Do(?:&(?:amp;)?gt;|>)"
    r"([\s\S]*?)"
    r"(?:&(?:amp;)?lt;|<)\/Do(?:&(?:amp;)?gt;|>)",
    re.IGNORECASE,
)
_DONT_RE = re.compile(
    r"(?:&(?:amp;)?lt;|<)Dont(?:&(?:amp;)?gt;|>)"
    r"([\s\S]*?)"
    r"(?:&(?:amp;)?lt;|<)\/Dont(?:&(?:amp;)?gt;|>)",
    re.IGNORECASE,
)
_RELATED_SELF_RE = re.compile(
    r"(?:&(?:amp;)?lt;|<)RelatedDocs\b([^>]*?)(?:\/(?:&(?:amp;)?gt;|>))",
    re.IGNORECASE,
)
_RELATED_BLOCK_RE = re.compile(
    r"(?:&(?:amp;)?lt;|<)RelatedDocs\b([^>]*?)(?:&(?:amp;)?gt;|>)"
    r"([\s\S]*?)"
    r"(?:&(?:amp;)?lt;|<)\/RelatedDocs(?:&(?:amp;)?gt;|>)",
    re.IGNORECASE,
)


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


def _normalize_slug(value: str | None) -> str:
    return (value or "").strip().strip("/").lower()


def _parse_slug_list(raw: str | None) -> list[str]:
    dedupe: list[str] = []
    seen: set[str] = set()
    for chunk in re.split(r"[\s,]+", raw or ""):
        slug = _normalize_slug(chunk)
        if not slug or slug in seen:
            continue
        seen.add(slug)
        dedupe.append(slug)
    return dedupe


def _language_slug(value: str | None) -> str:
    raw = (value or "").strip().lower()
    if not raw:
        return "en"
    slug = re.sub(r"[^a-z0-9]+", "-", raw).strip("-")
    return slug or "en"


def _render_related_docs_html(attrs: dict[str, str], *, language: str | None) -> str:
    slugs = _parse_slug_list(attrs.get("slugs") or attrs.get("slug"))
    if not slugs:
        return ""

    filters: dict = {"status": "Published", "slug": ["in", slugs]}
    if language:
        filters["language"] = language

    rows = frappe.get_all(
        "Documentation",
        filters=filters,
        fields=["slug", "title", "summary", "category", "language"],
        ignore_permissions=True,
    )

    by_slug = {_normalize_slug(row.get("slug")): row for row in rows}
    cards: list[str] = []
    for slug in slugs:
        item = by_slug.get(slug)
        if not item:
            continue
        language_slug = quote(_language_slug(item.get("language") or language), safe="")
        href_slug = quote((item.get("slug") or "").strip(), safe="")
        href = f"/docs/{language_slug}/{href_slug}/"
        title = frappe.utils.escape_html(item.get("title") or item.get("slug") or "")
        summary_raw = (item.get("summary") or "").strip()
        summary = (
            f'<p style="margin:.45rem 0 0;color:#475569;font-size:.92rem;">'
            f"{frappe.utils.escape_html(summary_raw)}</p>"
            if summary_raw
            else ""
        )
        category_raw = (item.get("category") or "").strip()
        category = (
            f'<span style="display:inline-flex;margin-top:.55rem;border-radius:999px;'
            f'padding:.12rem .55rem;background:#E4F4E9;color:#12563A;'
            f'font-size:.66rem;font-weight:600;letter-spacing:.08em;text-transform:uppercase;">'
            f"{frappe.utils.escape_html(category_raw)}</span>"
            if category_raw
            else ""
        )
        cards.append(
            f'<a href="{href}" style="display:block;border:1px solid #E2E8F0;border-radius:14px;'
            f'padding:.9rem 1rem;background:#fff;text-decoration:none;">'
            f'<div style="display:flex;justify-content:space-between;gap:.6rem;align-items:flex-start;">'
            f'<strong style="color:#0F172A;font-size:1rem;line-height:1.35;">{title}</strong>'
            f'<span style="color:#2F855A;font-size:1.05rem;line-height:1;">&rarr;</span></div>'
            f"{category}{summary}</a>"
        )

    title = frappe.utils.escape_html((attrs.get("title") or "Related docs").strip() or "Related docs")
    cards_html = "".join(cards) or (
        '<p style="border:1px solid #E2E8F0;border-radius:10px;padding:.8rem;color:#475569;'
        'font-size:.9rem;background:#fff;">No related docs found for these slugs yet.</p>'
    )

    return (
        '<section style="margin:1.2rem 0;padding:1rem;border-radius:16px;'
        'border:1px solid #E2E8F0;background:rgba(230,243,249,.45);">'
        f'<div style="margin-bottom:.75rem;font-size:.68rem;font-weight:700;'
        f'letter-spacing:.16em;text-transform:uppercase;color:#475569;">{title}</div>'
        f'<div style="display:grid;gap:.65rem;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));">{cards_html}</div>'
        "</section>"
    )


def _render_doc_markdown(md: str | None, *, language: str | None = None) -> str:
    source = md or ""
    callouts = []
    steps_blocks = []
    do_dont_blocks = []
    related_blocks = []

    def _replace_callout(match: re.Match) -> str:
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

    rendered = _CALLOUT_RE.sub(_replace_callout, source)

    def _replace_steps(match: re.Match) -> str:
        idx = len(steps_blocks)
        placeholder = f'__STEPS_PLACEHOLDER_{idx}__'
        attrs = _parse_attrs(match.group(1) or "")
        body = match.group(2) or ""
        items = []
        for step_match in _STEP_RE.finditer(body):
            step_attrs = _parse_attrs(step_match.group(1) or "")
            step_body = (step_match.group(2) or "").strip()
            if not step_body and not step_attrs.get("title"):
                continue
            items.append(
                {
                    "title": (step_attrs.get("title") or "").strip(),
                    "body": step_body,
                }
            )
        steps_blocks.append(
            {
                "placeholder": placeholder,
                "title": (attrs.get("title") or "").strip(),
                "items": items,
            }
        )
        return f"\n\n<div data-steps-placeholder=\"{placeholder}\"></div>\n\n"

    rendered = _STEPS_RE.sub(_replace_steps, rendered)

    def _replace_dodont(match: re.Match) -> str:
        idx = len(do_dont_blocks)
        placeholder = f'__DODONT_PLACEHOLDER_{idx}__'
        attrs = _parse_attrs(match.group(1) or "")
        body = match.group(2) or ""
        dos = [(m.group(1) or "").strip() for m in _DO_RE.finditer(body) if (m.group(1) or "").strip()]
        donts = [(m.group(1) or "").strip() for m in _DONT_RE.finditer(body) if (m.group(1) or "").strip()]
        do_dont_blocks.append(
            {
                "placeholder": placeholder,
                "do_title": (attrs.get("doTitle") or attrs.get("do_title") or "Do").strip() or "Do",
                "dont_title": (
                    attrs.get("dontTitle") or attrs.get("dont_title") or "Don't"
                ).strip()
                or "Don't",
                "dos": dos,
                "donts": donts,
            }
        )
        return f"\n\n<div data-dodont-placeholder=\"{placeholder}\"></div>\n\n"

    rendered = _DODONT_RE.sub(_replace_dodont, rendered)

    def _replace_related_from_attrs(raw_attrs: str) -> str:
        idx = len(related_blocks)
        placeholder = f'__RELATED_PLACEHOLDER_{idx}__'
        related_blocks.append(
            {
                "placeholder": placeholder,
                "attrs": _parse_attrs(raw_attrs or ""),
            }
        )
        return f"\n\n<div data-related-placeholder=\"{placeholder}\"></div>\n\n"

    rendered = _RELATED_SELF_RE.sub(lambda m: _replace_related_from_attrs(m.group(1) or ""), rendered)
    rendered = _RELATED_BLOCK_RE.sub(lambda m: _replace_related_from_attrs(m.group(1) or ""), rendered)

    html = str(md_to_html(rendered))

    for block in steps_blocks:
        cards = []
        for index, item in enumerate(block["items"], start=1):
            title = frappe.utils.escape_html((item.get("title") or f"Step {index}").strip() or f"Step {index}")
            body_html = _render_doc_markdown(item.get("body") or "", language=language).strip()
            cards.append(
                '<article style="border:1px solid #E2E8F0;border-radius:14px;padding:.9rem;'
                'background:#fff;box-shadow:0 4px 18px rgba(15,23,42,.06);">'
                '<div style="display:flex;align-items:center;gap:.55rem;margin-bottom:.55rem;">'
                f'<span style="display:inline-flex;align-items:center;justify-content:center;'
                f'width:1.7rem;height:1.7rem;border-radius:999px;background:rgba(47,133,90,.15);'
                f'color:#12563A;font-weight:700;font-size:.85rem;">{index}</span>'
                f'<strong style="color:#0F172A;">{title}</strong></div>'
                f'<div>{body_html}</div></article>'
            )
        title_html = (
            f'<div style="margin-bottom:.55rem;font-size:.68rem;font-weight:700;letter-spacing:.16em;'
            f'text-transform:uppercase;color:#475569;">{frappe.utils.escape_html(block["title"])}</div>'
            if block["title"]
            else ""
        )
        block_html = (
            '<section style="margin:1.2rem 0;">'
            f"{title_html}"
            '<div style="display:grid;gap:.7rem;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));">'
            f"{''.join(cards)}</div></section>"
        ) if cards else ""
        placeholder = f'<div data-steps-placeholder="{block["placeholder"]}"></div>'
        html = html.replace(f"<p>{placeholder}</p>", block_html).replace(placeholder, block_html)

    for block in do_dont_blocks:
        def _render_items(items, tone: str) -> str:
            if not items:
                return '<p style="margin:0;color:#475569;font-size:.9rem;">No entries yet.</p>'
            rendered_items = []
            for item in items:
                body_html = _render_doc_markdown(item, language=language).strip()
                border = "#2F855A33" if tone == "do" else "rgba(214,138,40,.38)"
                bg = "rgba(41,159,101,.09)" if tone == "do" else "rgba(208,135,0,.09)"
                rendered_items.append(
                    f'<li style="list-style:none;margin:0;border:1px solid {border};'
                    f'background:{bg};border-radius:11px;padding:.65rem;">{body_html}</li>'
                )
            return f'<ul style="display:grid;gap:.55rem;margin:0;padding:0;">{"".join(rendered_items)}</ul>'

        do_html = _render_items(block["dos"], "do")
        dont_html = _render_items(block["donts"], "dont")
        block_html = (
            '<section style="margin:1.2rem 0;display:grid;gap:.7rem;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));">'
            '<article style="border:1px solid rgba(47,133,90,.3);border-radius:14px;'
            'padding:.9rem;background:rgba(41,159,101,.06);">'
            f'<h3 style="margin:0 0 .55rem;font-size:.74rem;font-weight:700;letter-spacing:.14em;'
            f'text-transform:uppercase;color:#12563A;">{frappe.utils.escape_html(block["do_title"])}</h3>'
            f"{do_html}</article>"
            '<article style="border:1px solid rgba(214,138,40,.35);border-radius:14px;'
            'padding:.9rem;background:rgba(208,135,0,.06);">'
            f'<h3 style="margin:0 0 .55rem;font-size:.74rem;font-weight:700;letter-spacing:.14em;'
            f'text-transform:uppercase;color:#A66017;">{frappe.utils.escape_html(block["dont_title"])}</h3>'
            f"{dont_html}</article></section>"
        )
        placeholder = f'<div data-dodont-placeholder="{block["placeholder"]}"></div>'
        html = html.replace(f"<p>{placeholder}</p>", block_html).replace(placeholder, block_html)

    for block in related_blocks:
        block_html = _render_related_docs_html(block["attrs"], language=language)
        placeholder = f'<div data-related-placeholder="{block["placeholder"]}"></div>'
        html = html.replace(f"<p>{placeholder}</p>", block_html).replace(placeholder, block_html)

    for callout in callouts:
        type_raw = (callout["attrs"].get("type") or "info").strip().lower()
        callout_type = type_raw if type_raw in _ALLOWED_TYPES else "info"
        title = (callout["attrs"].get("title") or "").strip()
        body_html = _render_doc_markdown(callout["body"], language=language).strip()
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
    context.body_html = Markup(_render_doc_markdown(doc.body_md or "", language=doc.language))
    # use the same base template; content block comes from preview.html
    return context
