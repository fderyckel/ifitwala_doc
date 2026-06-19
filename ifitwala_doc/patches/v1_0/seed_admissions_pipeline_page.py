# Copyright (c) 2026, François de Ryckel and Contributors
# See license.txt

import frappe

PAGE_SLUG = "/ifitwala-ed/admissions-pipeline"
PAGE_SLUG_CANDIDATES = (PAGE_SLUG, PAGE_SLUG.strip("/"), f"{PAGE_SLUG}/")

HERO_HEADING = "Stop losing school enquiries in spreadsheets, inboxes, and disconnected forms."
FEATURE_EYEBROW = "Admissions Pipeline Capabilities"
LONGFORM_TITLE = "From first enquiry to enrolled student"


def execute():
    if page_exists():
        return

    hero_name = ensure_hero_block()
    feature_name = ensure_feature_highlight()
    longform_name = ensure_longform_block()

    page = frappe.get_doc(
        {
            "doctype": "Ifitwala Web Page",
            "title": "Ifitwala Ed Admissions Pipeline",
            "slug": PAGE_SLUG,
            "layout": "Landing",
            "is_published": 1,
            "meta_description": (
                "A focused Ifitwala Ed landing page for managing school enquiries, "
                "applications, documents, offers, deposits, and enrolment handover."
            ),
            "seo_title": "Admissions Pipeline Software for Schools | Ifitwala Ed",
            "seo_description": (
                "Manage school enquiries, applications, documents, reviews, offers, "
                "deposits, and enrolment handover in one structured pipeline connected "
                "to student records."
            ),
            "og_title": "Admissions Pipeline Software for Schools | Ifitwala Ed",
            "og_description": (
                "Give admissions teams one structured pipeline from first enquiry to "
                "enrolled student, connected to the wider school operating system."
            ),
            "og_type": "product",
            "sections": [
                {
                    "doctype": "Ifitwala Web Page Section",
                    "block_type": "Hero",
                    "block_doctype": "Hero Block",
                    "block_ref": hero_name,
                    "section_order": 1,
                },
                {
                    "doctype": "Ifitwala Web Page Section",
                    "block_type": "Feature Highlights",
                    "block_doctype": "Feature Highlight",
                    "block_ref": feature_name,
                    "section_order": 2,
                },
                {
                    "doctype": "Ifitwala Web Page Section",
                    "block_type": "Longform Content",
                    "block_doctype": "Longform Block",
                    "block_ref": longform_name,
                    "section_order": 3,
                },
            ],
        }
    )
    page.insert(ignore_permissions=True)


def page_exists():
    for slug in PAGE_SLUG_CANDIDATES:
        if frappe.db.exists("Ifitwala Web Page", {"slug": slug}):
            return True
    return False


def ensure_hero_block():
    existing = frappe.db.exists("Hero Block", {"heading": HERO_HEADING})
    if existing:
        return existing

    hero = frappe.get_doc(
        {
            "doctype": "Hero Block",
            "eyebrow": "Admissions Pipeline",
            "heading": HERO_HEADING,
            "subheading": (
                "Ifitwala Ed gives admissions teams one structured pipeline for "
                "enquiries, applications, documents, reviews, offers, deposits, and "
                "enrolment handover, connected to the wider student record."
            ),
            "align": "left",
            "theme": "light",
            "actions": [
                {
                    "doctype": "Hero Action",
                    "label": "Book a demo",
                    "href": "/book-a-demo/",
                    "variant": "primary",
                },
                {
                    "doctype": "Hero Action",
                    "label": "Explore the workflow",
                    "href": "#workflow",
                    "variant": "secondary",
                },
            ],
        }
    )
    hero.insert(ignore_permissions=True)
    return hero.name


def ensure_feature_highlight():
    existing = frappe.db.exists("Feature Highlight", {"eyebrow": FEATURE_EYEBROW})
    if existing:
        return existing

    feature = frappe.get_doc(
        {
            "doctype": "Feature Highlight",
            "eyebrow": FEATURE_EYEBROW,
            "intro": (
                "A focused workflow for the first operational win, with records that "
                "carry forward into the wider Ifitwala Ed platform."
            ),
            "items": [
                {
                    "doctype": "Feature Item",
                    "item_order": 1,
                    "icon_name": "inbox",
                    "label": "Enquiry capture",
                    "description": (
                        "Track every enquiry with source, status, owner, next action, "
                        "family context, and follow-up history."
                    ),
                },
                {
                    "doctype": "Feature Item",
                    "item_order": 2,
                    "icon_name": "clipboard-check",
                    "label": "Application checklist",
                    "description": (
                        "Collect forms, required documents, review notes, missing "
                        "items, and completion status in one place."
                    ),
                },
                {
                    "doctype": "Feature Item",
                    "item_order": 3,
                    "icon_name": "route",
                    "label": "Reviewer workflow",
                    "description": (
                        "Route applications, documents, interviews, and decisions to "
                        "the right people without losing context."
                    ),
                },
                {
                    "doctype": "Feature Item",
                    "item_order": 4,
                    "icon_name": "credit-card",
                    "label": "Offer and deposit tracking",
                    "description": (
                        "Track offers, acceptance, deposits, and enrolment readiness "
                        "before handover to student records."
                    ),
                },
                {
                    "doctype": "Feature Item",
                    "item_order": 5,
                    "icon_name": "users",
                    "label": "Parent visibility",
                    "description": (
                        "Give families clearer next steps, required documents, and "
                        "application progress."
                    ),
                },
                {
                    "doctype": "Feature Item",
                    "item_order": 6,
                    "icon_name": "bar-chart-3",
                    "label": "Leadership pipeline view",
                    "description": (
                        "Show school leaders enquiry volume, application movement, "
                        "bottlenecks, and incomplete work."
                    ),
                },
            ],
        }
    )
    feature.insert(ignore_permissions=True)
    return feature.name


def ensure_longform_block():
    existing = frappe.db.exists("Longform Block", {"title": LONGFORM_TITLE})
    if existing:
        return existing

    longform = frappe.get_doc(
        {
            "doctype": "Longform Block",
            "title": LONGFORM_TITLE,
            "lede": (
                "Admissions is not just a form. It is a live operational workflow "
                "involving families, documents, reviews, visits, offers, deposits, "
                "and leadership visibility."
            ),
            "background": "muted",
            "seo_title": "Admissions Pipeline Software for Schools | Ifitwala Ed",
            "seo_description": (
                "Manage enquiries, applications, documents, reviews, offers, deposits, "
                "and enrolment handover in one admissions workflow."
            ),
            "og_title": "From first enquiry to enrolled student",
            "og_description": (
                "A focused admissions workflow that connects enquiries and applications "
                "to student records, portals, reporting, and governed access."
            ),
            "og_type": "product",
            "sections": [
                longform_section(
                    1,
                    "why-admissions",
                    "The problem",
                    "Admissions work leaks when ownership is unclear.",
                    (
                        "<p>A school can receive a promising enquiry, reply once, then "
                        "lose momentum because the next step is buried in an inbox, "
                        "spreadsheet, or private note. The result is not just "
                        "administrative mess. It is lost trust, slow follow-up, and "
                        "weak visibility for leadership.</p>"
                    ),
                ),
                longform_section(
                    2,
                    "workflow",
                    "The workflow",
                    "Admissions is the first structured path into the platform.",
                    (
                        "<p>Admissions is often the first place school data becomes "
                        "fragmented. Ifitwala Ed starts there, then carries the work "
                        "forward into enrolment, student records, portals, reporting, "
                        "and governed access.</p><p>Each enquiry has a status, owner, "
                        "next action, source, family context, and timeline. Applications "
                        "can move through document collection, review, interview, offer, "
                        "deposit, and enrolment handover without rebuilding the same "
                        "information several times.</p>"
                    ),
                ),
                longform_section(
                    3,
                    "handover",
                    "The handover",
                    "Accepted applicants become cleaner student records.",
                    (
                        "<p>The goal is not only to win the enrolment. The goal is to "
                        "avoid starting from zero after acceptance. Ifitwala Ed connects "
                        "admissions data to student, guardian, programme, document, and "
                        "operational records so the school starts with a cleaner base.</p>"
                    ),
                ),
                longform_section(
                    4,
                    "visibility",
                    "The outcome",
                    "Fewer lost leads. Cleaner records. Better leadership visibility.",
                    (
                        "<p>Admissions teams can see what is overdue, what is incomplete, "
                        "who owns the next action, and where families are getting stuck. "
                        "Leaders get a clearer view of pipeline health without asking "
                        "someone to rebuild a spreadsheet before every meeting.</p>"
                    ),
                ),
                longform_section(
                    5,
                    "demo",
                    "Next step",
                    "See it with your real admissions workflow.",
                    (
                        "<p>Use a focused demo to review how enquiries, applications, "
                        "document collection, decisions, offers, deposits, and enrolment "
                        "handover could work for your school.</p>"
                    ),
                    style="highlight",
                    cta_label="Book a demo",
                    cta_href="/book-a-demo/",
                    cta_variant="primary",
                ),
            ],
        }
    )
    longform.insert(ignore_permissions=True)
    return longform.name


def longform_section(
    order,
    anchor,
    eyebrow,
    heading,
    body,
    style="default",
    cta_label=None,
    cta_href=None,
    cta_variant=None,
):
    section = {
        "doctype": "Longform Block Section",
        "section_order": order,
        "layout": "text",
        "style": style,
        "anchor": anchor,
        "eyebrow": eyebrow,
        "heading": heading,
        "body": body,
    }

    if cta_label and cta_href:
        section.update(
            {
                "cta_label": cta_label,
                "cta_href": cta_href,
                "cta_variant": cta_variant or "link",
            }
        )

    return section
