# Copyright (c) 2025, François de Ryckel and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase

from ifitwala_doc.api import site as site_api


def _unique(prefix: str) -> str:
	return f"{prefix}-{frappe.generate_hash(length=8).lower()}"


def _make_hero_block():
	return frappe.get_doc(
		{
			"doctype": "Hero Block",
			"heading": _unique("Hero"),
			"subheading": "Smoke test hero",
			"align": "left",
			"theme": "light",
		}
	).insert()


class TestIfitwalaWebPage(FrappeTestCase):
	def test_published_page_serializes_sections_and_normalizes_home_slug(self):
		hero = _make_hero_block()
		page = frappe.get_doc(
			{
				"doctype": "Ifitwala Web Page",
				"title": _unique("Home Page"),
				"slug": "home",
				"layout": "Landing",
				"is_published": 1,
				"sections": [
					{
						"doctype": "Ifitwala Web Page Section",
						"block_type": "Hero",
						"block_doctype": "Hero Block",
						"block_ref": hero.name,
						"section_order": 1,
					}
				],
			}
		).insert()

		payload = site_api.get_page("home")
		self.assertEqual(payload["name"], page.name)
		self.assertEqual(payload["slug"], "/")
		self.assertEqual(payload["sections"][0]["type"], "Hero")
		self.assertEqual(payload["sections"][0]["block"]["doctype"], "Hero Block")
		self.assertEqual(payload["sections"][0]["block"]["name"], hero.name)

		pages = {entry["name"]: entry for entry in site_api.list_pages()}
		self.assertIn(page.name, pages)
		self.assertEqual(pages[page.name]["slug"], "/")

	def test_rejects_duplicate_section_order(self):
		hero = _make_hero_block()

		with self.assertRaises(frappe.ValidationError):
			frappe.get_doc(
				{
					"doctype": "Ifitwala Web Page",
					"title": _unique("Bad Page"),
					"slug": _unique("bad-page"),
					"layout": "Landing",
					"is_published": 1,
					"sections": [
						{
							"doctype": "Ifitwala Web Page Section",
							"block_type": "Hero",
							"block_doctype": "Hero Block",
							"block_ref": hero.name,
							"section_order": 1,
						},
						{
							"doctype": "Ifitwala Web Page Section",
							"block_type": "Hero",
							"block_doctype": "Hero Block",
							"block_ref": hero.name,
							"section_order": 1,
						},
					],
				}
			).insert()

	def test_get_nav_returns_enabled_menu_items_in_order(self):
		frappe.get_doc(
			{
				"doctype": "Navigation Menu",
				"title": _unique("Header Menu"),
				"location": "Header",
				"is_enabled": 1,
				"items": [
					{
						"doctype": "Navigation Menu Item",
						"label": "Docs",
						"href": "/docs",
						"item_order": 10,
						"target_blank": 0,
					},
					{
						"doctype": "Navigation Menu Item",
						"label": "Book a Demo",
						"href": "/demo",
						"item_order": 20,
						"target_blank": 1,
					},
				],
			}
		).insert()

		items = site_api.get_nav("Header")
		self.assertEqual([item["label"] for item in items], ["Docs", "Book a Demo"])
		self.assertEqual(items[0]["href"], "/docs")
		self.assertEqual(items[1]["href"], "/book-a-demo/")
		self.assertEqual(items[1]["target_blank"], 1)
