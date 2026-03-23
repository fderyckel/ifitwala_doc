# Copyright (c) 2025, François de Ryckel and Contributors
# See license.txt

from unittest.mock import patch

import frappe
from frappe.tests.utils import FrappeTestCase

from ifitwala_doc.api import docs as docs_api


def _unique(prefix: str) -> str:
	return f"{prefix}-{frappe.generate_hash(length=8).lower()}"


def _make_category(label=None, slug=None, cat_order=None):
	label = label or _unique("Category")
	slug = slug or label.lower().replace(" ", "-")
	return frappe.get_doc(
		{
			"doctype": "Doc Category",
			"label": label,
			"slug": slug,
			"cat_order": cat_order,
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

	def test_fetch_one_orders_screenshots_with_missing_image_order_last(self):
		category = _make_category()
		subcategory = _make_subcategory(category.name)

		with patch("frappe.enqueue"):
			doc = frappe.get_doc(
				{
					"doctype": "Documentation",
					"title": _unique("Screenshot Guide"),
					"slug": _unique("screenshot-guide"),
					"language": "en",
					"status": "Published",
					"category": category.name,
					"subcategory": subcategory.name,
					"summary": "Screenshot ordering",
					"body_md": "## Ordered screenshots",
					"author": "QA",
					"screenshots": [
						{
							"anchor_id": "third-shot",
							"title": "Third",
							"image": "/files/third-shot.png",
							"alt_text": "Third screenshot",
						},
						{
							"anchor_id": "second-shot",
							"title": "Second",
							"image": "/files/second-shot.png",
							"image_order": 2,
							"alt_text": "Second screenshot",
						},
						{
							"anchor_id": "first-shot",
							"title": "First",
							"image": "/files/first-shot.png",
							"image_order": 1,
							"alt_text": "First screenshot",
						},
					],
				}
			).insert()

		record = docs_api.fetch_one(language="en", slug=doc.slug)
		self.assertEqual(
			[shot["fig"] for shot in record["screenshots"]],
			["first-shot", "second-shot", "third-shot"],
		)

	def test_category_endpoints_keep_missing_sort_orders_last(self):
		ordered_category = _make_category(
			label=_unique("Zulu Category"),
			slug=_unique("zulu-category"),
			cat_order=1,
		)
		unordered_category = _make_category(
			label=_unique("Alpha Category"),
			slug=_unique("alpha-category"),
		)
		subcategory = _make_subcategory(ordered_category.name, _unique("Ordering"))

		with patch("frappe.enqueue"):
			late_doc = frappe.get_doc(
				{
					"doctype": "Documentation",
					"title": "Alpha Unordered",
					"slug": _unique("alpha-unordered"),
					"language": "en",
					"status": "Published",
					"category": ordered_category.name,
					"subcategory": subcategory.name,
					"summary": "No explicit order",
					"body_md": "Body",
					"author": "QA",
				}
			).insert()
			first_doc = frappe.get_doc(
				{
					"doctype": "Documentation",
					"title": "Zulu Ordered",
					"slug": _unique("zulu-ordered"),
					"language": "en",
					"status": "Published",
					"category": ordered_category.name,
					"subcategory": subcategory.name,
					"summary": "Explicit order",
					"body_md": "Body",
					"author": "QA",
					"doc_order": 1,
				}
			).insert()

		categories = docs_api.get_categories()
		category_names = [
			row["name"]
			for row in categories
			if row["name"] in {ordered_category.name, unordered_category.name}
		]
		self.assertEqual(category_names, [ordered_category.name, unordered_category.name])

		docs = docs_api.get_docs_in_category(language="en", category_slug=ordered_category.slug)
		self.assertEqual([row["name"] for row in docs], [first_doc.name, late_doc.name])
