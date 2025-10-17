# Copyright (c) 2025, François de Ryckel and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _

class FeatureHighlight(Document):
    def validate(self):
        if not self.items:
            frappe.throw(_("Add at least one Feature Item."))
        labels = set()
        for row in self.items:
            if not row.label:
                frappe.throw(_("Each Feature Item requires a Label."))
            if row.item_order in labels:
                frappe.throw(_("Duplicate item_order {0}. Use unique order values.").format(row.item_order))
            labels.add(row.item_order)
