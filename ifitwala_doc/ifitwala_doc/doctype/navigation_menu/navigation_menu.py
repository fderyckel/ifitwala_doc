# Copyright (c) 2025, François de Ryckel and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _

class NavigationMenu(Document):
    def validate(self):
        self._validate_unique_item_order()

    def _validate_unique_item_order(self):
        seen = set()
        for row in (self.items or []):
            key = row.item_order
            if key in seen:
                frappe.throw(
                    _("Duplicate item_order {0} in Items. Each item must be unique within a menu.")
                    .format(key)
                )
            seen.add(key)
