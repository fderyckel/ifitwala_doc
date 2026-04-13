# Copyright (c) 2026, François de Ryckel and Contributors
# See license.txt

import frappe


TEMPLATES = [
	{
		"name": "Ifitwala Lead - First Response",
		"subject": "Thanks for reaching out to Ifitwala, {{ doc.first_name }}",
		"response": """Hi {{ doc.first_name or "there" }},

Thank you for reaching out to Ifitwala. We have received your enquiry and will review the details so the follow-up is relevant to {{ doc.school_name or "your institution" }}.

If it helps, reply with:
- the type of institution you run
- the number of students or campuses
- the workflows you want to improve first
- your ideal decision timeline

Best regards,
The Ifitwala team""",
	},
	{
		"name": "Ifitwala Lead - Qualification Follow-Up",
		"subject": "A quick follow-up on your Ifitwala enquiry",
		"response": """Hi {{ doc.first_name or "there" }},

I wanted to follow up on your enquiry about Ifitwala.

To make the next conversation useful, could you share:
- the main pain points you want to solve
- the teams that need to be involved
- whether you are evaluating this for the current term or a future rollout

Once I have that context, I can suggest the most relevant workflows to review.

Best regards,
The Ifitwala team""",
	},
	{
		"name": "Ifitwala Lead - Demo Invitation",
		"subject": "Would a focused Ifitwala walkthrough help?",
		"response": """Hi {{ doc.first_name or "there" }},

If helpful, we can schedule a focused walkthrough of Ifitwala for {{ doc.school_name or "your team" }}.

We would tailor it around the workflows that matter most to you, such as:
- admissions and enquiries
- academic operations
- finance and billing
- leadership reporting

If you would like to book a session, reply with a few time windows that work for you and the stakeholders who should attend.

Best regards,
The Ifitwala team""",
	},
]


def execute():
	if not frappe.db.exists("DocType", "Email Template"):
		return

	meta = frappe.get_meta("Email Template")
	fieldnames = {field.fieldname for field in meta.fields}

	for template in TEMPLATES:
		doc, exists = get_or_initialize_template(template["name"], fieldnames)
		apply_template_values(doc, template, fieldnames)

		if exists:
			doc.save(ignore_permissions=True)
		else:
			doc.insert(ignore_permissions=True)


def get_or_initialize_template(template_name, fieldnames):
	existing_template_name = find_existing_template_name(template_name, fieldnames)
	if existing_template_name:
		return frappe.get_doc("Email Template", existing_template_name), True

	doc = frappe.new_doc("Email Template")

	if "title" in fieldnames:
		doc.title = template_name

	if "template_name" in fieldnames:
		doc.template_name = template_name

	if "title" not in fieldnames and "template_name" not in fieldnames:
		doc.name = template_name

	return doc, False


def find_existing_template_name(template_name, fieldnames):
	existing_by_name = frappe.db.exists("Email Template", template_name)
	if existing_by_name:
		return existing_by_name

	if "template_name" in fieldnames:
		existing_by_template_name = frappe.db.exists(
			"Email Template", {"template_name": template_name}
		)
		if existing_by_template_name:
			return existing_by_template_name

	if "title" in fieldnames:
		existing_by_title = frappe.db.exists("Email Template", {"title": template_name})
		if existing_by_title:
			return existing_by_title

	return None


def apply_template_values(doc, template, fieldnames):
	if "reference_doctype" in fieldnames:
		doc.reference_doctype = "Lead"

	if "doc_type" in fieldnames:
		doc.doc_type = "Lead"

	if "enabled" in fieldnames:
		doc.enabled = 1

	if "use_html" in fieldnames:
		doc.use_html = 0

	if "subject" in fieldnames:
		doc.subject = template["subject"]

	if "response" in fieldnames:
		doc.response = template["response"]
