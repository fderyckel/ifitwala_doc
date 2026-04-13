import frappe
from frappe.model.document import Document
from frappe.utils import add_to_date, get_datetime, getdate, now_datetime

from ifitwala_doc.crm.doctype.ifitwala_crm_settings.ifitwala_crm_settings import get_configured_lead_owner


FOLLOW_UP_TODO_PREFIX = "Lead follow-up:"
CONTACTED_STATUSES = {"Contacted", "Qualified", "Converted"}
TERMINAL_STATUSES = {"Converted", "Lost"}


class Lead(Document):
	def validate(self):
		self.set_full_name()
		self.set_default_lead_owner()
		self.set_default_next_follow_up()
		self.set_last_contacted_on()
		self.set_follow_up_status()

	def after_insert(self):
		self.sync_follow_up_task()

	def on_update(self):
		self.sync_follow_up_task()

	def set_full_name(self):
		if self.last_name:
			self.title = f"{self.first_name} {self.last_name}"
		else:
			self.title = self.first_name

	def set_default_lead_owner(self):
		if self.lead_owner:
			return

		configured_owner = get_configured_lead_owner(self.source)
		if configured_owner:
			self.lead_owner = configured_owner
			return

		if frappe.session.user == "Guest":
			return

		self.lead_owner = frappe.session.user

	def set_default_next_follow_up(self):
		if self.next_follow_up_on or self.status in TERMINAL_STATUSES:
			return

		self.next_follow_up_on = add_to_date(now_datetime(), days=1, as_datetime=True)

	def set_last_contacted_on(self):
		if self.last_contacted_on or self.status not in CONTACTED_STATUSES:
			return

		self.last_contacted_on = now_datetime()

	def set_follow_up_status(self):
		if self.status in TERMINAL_STATUSES:
			self.follow_up_status = "Closed"
			return

		if not self.next_follow_up_on:
			self.follow_up_status = "Not Scheduled"
			return

		next_follow_up_date = getdate(self.next_follow_up_on)
		today = getdate(now_datetime())

		if next_follow_up_date < today:
			self.follow_up_status = "Overdue"
		elif next_follow_up_date == today:
			self.follow_up_status = "Due Today"
		else:
			self.follow_up_status = "Scheduled"

	def sync_follow_up_task(self):
		open_tasks = self.get_open_follow_up_tasks()

		if self.status in TERMINAL_STATUSES or not self.lead_owner or not self.next_follow_up_on:
			self.close_follow_up_tasks(open_tasks)
			return

		primary_task = open_tasks[0] if open_tasks else None
		if len(open_tasks) > 1:
			self.close_follow_up_tasks(open_tasks[1:])

		if primary_task:
			self.update_follow_up_task(primary_task)
			return

		self.create_follow_up_task()

	def get_open_follow_up_tasks(self):
		task_names = frappe.get_all(
			"ToDo",
			filters={
				"reference_type": self.doctype,
				"reference_name": self.name,
				"status": ["not in", ["Closed", "Cancelled"]],
				"description": ["like", f"{FOLLOW_UP_TODO_PREFIX}%"],
			},
			order_by="date asc, creation asc",
			pluck="name",
		)
		return [frappe.get_doc("ToDo", task_name) for task_name in task_names]

	def close_follow_up_tasks(self, tasks):
		for task in tasks:
			if task.status == "Closed":
				continue

			task.status = "Closed"
			task.save(ignore_permissions=True)

	def create_follow_up_task(self):
		task = frappe.get_doc(
			{
				"doctype": "ToDo",
				"allocated_to": self.lead_owner,
				"date": getdate(self.next_follow_up_on),
				"description": self.get_follow_up_task_description(),
				"priority": self.get_follow_up_task_priority(),
				"reference_type": self.doctype,
				"reference_name": self.name,
				"status": "Open",
			}
		)
		task.insert(ignore_permissions=True)

	def update_follow_up_task(self, task):
		updated = False
		expected_date = getdate(self.next_follow_up_on)
		expected_description = self.get_follow_up_task_description()
		expected_priority = self.get_follow_up_task_priority()

		if task.allocated_to != self.lead_owner:
			task.allocated_to = self.lead_owner
			updated = True

		if task.date != expected_date:
			task.date = expected_date
			updated = True

		if task.description != expected_description:
			task.description = expected_description
			updated = True

		if task.priority != expected_priority:
			task.priority = expected_priority
			updated = True

		if task.status != "Open":
			task.status = "Open"
			updated = True

		if updated:
			task.save(ignore_permissions=True)

	def get_follow_up_task_description(self):
		next_follow_up = get_datetime(self.next_follow_up_on).strftime("%Y-%m-%d %H:%M")
		lead_name = self.title or self.first_name
		return f"{FOLLOW_UP_TODO_PREFIX} {lead_name} ({self.name}) on {next_follow_up}"

	def get_follow_up_task_priority(self):
		if self.follow_up_status in {"Overdue", "Due Today"}:
			return "High"

		return "Medium"
