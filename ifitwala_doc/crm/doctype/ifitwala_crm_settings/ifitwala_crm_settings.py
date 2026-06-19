# Copyright (c) 2026, François de Ryckel and Contributors
# See license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class IfitwalaCRMSettings(Document):
	def validate(self):
		self.normalize_source_assignment_rules()
		self.validate_unique_sources()

	def normalize_source_assignment_rules(self):
		for row in self.source_assignment_rules or []:
			row.source = (row.source or "").strip()

	def validate_unique_sources(self):
		seen_sources = set()

		for row in self.source_assignment_rules or []:
			normalized_source = normalize_source(row.source)
			if not normalized_source:
				continue

			if normalized_source in seen_sources:
				frappe.throw(_("Lead source '{0}' is configured more than once.").format(row.source))

			seen_sources.add(normalized_source)


def get_configured_lead_owner(source=None):
	if not frappe.db.exists("DocType", "Ifitwala CRM Settings"):
		return None

	settings = frappe.get_single("Ifitwala CRM Settings")
	normalized_source = normalize_source(source)

	if normalized_source:
		for row in settings.source_assignment_rules or []:
			if normalize_source(row.source) != normalized_source:
				continue

			if is_active_user(row.lead_owner):
				return row.lead_owner

	if is_active_user(settings.default_lead_owner):
		return settings.default_lead_owner

	return None


def normalize_source(source):
	return (source or "").strip().casefold()


def is_active_user(user):
	if not user:
		return False

	return bool(frappe.db.get_value("User", user, "enabled"))

