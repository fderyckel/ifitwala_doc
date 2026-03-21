# Copyright (c) 2025, François de Ryckel and Contributors
# See license.txt

from unittest.mock import patch

import frappe
from frappe.tests.utils import FrappeTestCase

from ifitwala_doc.api import docs as docs_api


def _unique(prefix: str) -> str:
	return f"{prefix}-{frappe.generate_hash(length=8).lower()}"


def _make_category(label=None, slug=None):
	label = label or _unique("Category")
	slug = slug or label.lower().replace(" ", "-")
	return frappe.get_doc(
		{
			"doctype": "Doc Category",
			"label": label,
			"slug": slug,
		}
	).insert()


def _make_subcategory(category_name: str, label=None):
	label = label or _unique("Subcategory")
	return frappe.get_doc(
		{
			"doctype": "Doc Subcategory",
			"category": category_name,
			"label": label,
			"subcat_order": 1,
		}
	).insert()


class TestDocumentation(FrappeTestCase):
	def test_published_doc_auto_sets_slug_and_publish_date(self):
		category = _make_category()
		subcategory = _make_subcategory(category.name)

		with patch("frappe.enqueue"):
			doc = frappe.get_doc(
				{
					"doctype": "Documentation",
					"title": "Smoke Test Guide",
					"language": "en",
					"status": "Published",
					"category": category.name,
					"subcategory": subcategory.name,
					"summary": "Short summary",
					"body_md": "# Hello world",
					"author": "CI",
				}
			).insert()

		self.assertEqual(doc.slug, "smoke-test-guide")
		self.assertTrue(doc.published_on)
		self.assertEqual(doc.last_edited_by, "Administrator")

	def test_rejects_mismatched_subcategory(self):
		category = _make_category(_unique("Docs Parent"))
		other_category = _make_category(_unique("Wrong Parent"))
		subcategory = _make_subcategory(category.name, _unique("Teacher Guides"))

		with self.assertRaises(frappe.ValidationError):
			with patch("frappe.enqueue"):
				frappe.get_doc(
					{
						"doctype": "Documentation",
						"title": _unique("Invalid Doc"),
						"slug": _unique("invalid-doc"),
						"language": "en",
						"status": "Draft",
						"category": other_category.name,
						"subcategory": subcategory.name,
						"body_md": "Body",
					}
				).insert()

	def test_fetch_endpoints_return_published_docs_with_category_metadata(self):
		category_label = _unique("Operations")
		category_slug = _unique("operations")
		category = _make_category(category_label, category_slug)
		subcategory = _make_subcategory(category.name, _unique("Attendance"))

		with patch("frappe.enqueue"):
			doc = frappe.get_doc(
				{
					"doctype": "Documentation",
					"title": _unique("Attendance Guide"),
					"slug": _unique("attendance-guide"),
					"language": "en",
					"status": "Published",
					"category": category.name,
					"subcategory": subcategory.name,
					"summary": "How to take attendance",
					"body_md": "## Steps\nTake attendance",
					"author": "QA",
				}
			).insert()

		frappe.local.request = frappe._dict(headers={})
		frappe.local.response = frappe._dict()

		payload = docs_api.fetch_all(language="en")
		items = {item["name"]: item for item in payload["docs"]}
		self.assertIn(doc.name, items)
		self.assertEqual(items[doc.name]["category_slug"], category.slug)
		self.assertEqual(items[doc.name]["category_label"], category.label)
		self.assertEqual(items[doc.name]["subcategory"], subcategory.name)

		record = docs_api.fetch_one(language="en", slug=doc.slug)
		self.assertEqual(record["name"], doc.name)
		self.assertEqual(record["category_slug"], category.slug)
		self.assertEqual(record["tags"], [])
		self.assertEqual(record["screenshots"], [])
		self.assertIsNone(record["og_image"])
