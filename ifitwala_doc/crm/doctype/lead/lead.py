
import frappe
from frappe.model.document import Document

class Lead(Document):
	def validate(self):
		self.set_full_name()

	def set_full_name(self):
		if self.last_name:
			self.title = f"{self.first_name} {self.last_name}"
		else:
			self.title = self.first_name

