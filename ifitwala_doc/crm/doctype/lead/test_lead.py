# Copyright (c) 2026, François de Ryckel and Contributors
# See license.txt

from unittest.mock import patch

import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.utils import getdate

from ifitwala_doc.crm.api import capture_lead
from ifitwala_doc.crm.doctype.lead.lead import FOLLOW_UP_TODO_PREFIX


def _unique_email():
	return f"lead-{frappe.generate_hash(length=8).lower()}@example.com"


def _ensure_system_user(email, first_name):
	if frappe.db.exists("User", email):
		return email

	user = frappe.get_doc(
		{
			"doctype": "User",
			"email": email,
			"first_name": first_name,
			"enabled": 1,
			"user_type": "System User",
			"send_welcome_email": 0,
			"roles": [{"role": "System Manager"}],
		}
	)
	user.insert(ignore_permissions=True)
	return user.name


class TestLead(FrappeTestCase):
	def setUp(self):
		self.reset_crm_settings()

	def reset_crm_settings(self):
		settings = frappe.get_single("Ifitwala CRM Settings")
		settings.default_lead_owner = None
		settings.source_assignment_rules = []
		settings.save(ignore_permissions=True)

	def test_creates_follow_up_task_for_owned_leads(self):
		lead = frappe.get_doc(
			{
				"doctype": "Lead",
				"first_name": "Amina",
				"email": _unique_email(),
				"lead_owner": "Administrator",
			}
		).insert()

		self.assertEqual(lead.follow_up_status, "Scheduled")
		self.assertTrue(lead.next_follow_up_on)

		todos = frappe.get_all(
			"ToDo",
			filters={
				"reference_type": "Lead",
				"reference_name": lead.name,
				"description": ["like", f"{FOLLOW_UP_TODO_PREFIX}%"],
			},
			fields=["name", "allocated_to", "date", "status"],
		)

		self.assertEqual(len(todos), 1)
		self.assertEqual(todos[0].allocated_to, "Administrator")
		self.assertEqual(todos[0].status, "Open")
		self.assertEqual(todos[0].date, getdate(lead.next_follow_up_on))

	def test_sets_last_contacted_on_when_progressing_the_lead(self):
		lead = frappe.get_doc(
			{
				"doctype": "Lead",
				"first_name": "Jon",
				"email": _unique_email(),
			}
		).insert()

		self.assertFalse(lead.last_contacted_on)

		lead.status = "Contacted"
		lead.save()

		self.assertTrue(lead.last_contacted_on)
		self.assertEqual(lead.follow_up_status, "Scheduled")

	def test_closes_follow_up_tasks_when_lead_is_converted(self):
		lead = frappe.get_doc(
			{
				"doctype": "Lead",
				"first_name": "Maya",
				"email": _unique_email(),
				"lead_owner": "Administrator",
			}
		).insert()

		todo_name = frappe.get_value(
			"ToDo",
			{
				"reference_type": "Lead",
				"reference_name": lead.name,
				"description": ["like", f"{FOLLOW_UP_TODO_PREFIX}%"],
			},
		)
		self.assertTrue(todo_name)

		lead.status = "Converted"
		lead.save()

		self.assertEqual(lead.follow_up_status, "Closed")
		self.assertEqual(frappe.db.get_value("ToDo", todo_name, "status"), "Closed")

	def test_guest_website_leads_use_default_owner_from_settings(self):
		default_owner = _ensure_system_user(_unique_email(), "Default Owner")
		settings = frappe.get_single("Ifitwala CRM Settings")
		settings.default_lead_owner = default_owner
		settings.source_assignment_rules = []
		settings.save(ignore_permissions=True)

		with patch("frappe.session.user", "Guest"):
			lead_name = capture_lead(first_name="Sara", email=_unique_email(), source="Website")

		lead = frappe.get_doc("Lead", lead_name)
		self.assertEqual(lead.lead_owner, default_owner)

		todo_name = frappe.get_value(
			"ToDo",
			{
				"reference_type": "Lead",
				"reference_name": lead.name,
				"description": ["like", f"{FOLLOW_UP_TODO_PREFIX}%"],
			},
		)
		self.assertTrue(todo_name)

	def test_guest_leads_use_source_specific_owner_before_default_owner(self):
		default_owner = _ensure_system_user(_unique_email(), "Default Owner")
		referral_owner = _ensure_system_user(_unique_email(), "Referral Owner")

		settings = frappe.get_single("Ifitwala CRM Settings")
		settings.default_lead_owner = default_owner
		settings.source_assignment_rules = []
		settings.append(
			"source_assignment_rules",
			{
				"source": "Referral",
				"lead_owner": referral_owner,
			},
		)
		settings.save(ignore_permissions=True)

		with patch("frappe.session.user", "Guest"):
			lead_name = capture_lead(first_name="Mila", email=_unique_email(), source="Referral")

		lead = frappe.get_doc("Lead", lead_name)
		self.assertEqual(lead.lead_owner, referral_owner)
