# Copyright (c) 2025, François de Ryckel and Contributors
# See license.txt

from types import SimpleNamespace
from unittest.mock import patch

from frappe.tests.utils import FrappeTestCase

from ifitwala_doc.api import site as site_api


class TestIfitwalaWebsiteSettings(FrappeTestCase):
	def test_get_site_settings_keeps_missing_display_order_last(self):
		settings = SimpleNamespace(
			name="Ifitwala Website Settings",
			site_name="Ifitwala",
			brand_logo=None,
			brand_logo_alt=None,
			tagline="Tagline",
			primary_cta_label="Book a demo",
			primary_cta_url="https://example.com/demo",
			footer_md="Footer",
			modified=None,
		)

		social_links = [
			{"platform": "X (Twitter)", "url": "https://example.com/x", "icon": None, "display_order": 0},
			{"platform": "LinkedIn", "url": "https://example.com/linkedin", "icon": None, "display_order": 2},
			{"platform": "GitHub", "url": "https://example.com/github", "icon": None, "display_order": 1},
		]

		with patch("ifitwala_doc.api.site.frappe.get_single", return_value=settings), patch(
			"ifitwala_doc.api.site.frappe.get_all", return_value=social_links
		):
			payload = site_api.get_site_settings()

		self.assertEqual(
			[link["platform"] for link in payload["social_links"]],
			["GitHub", "LinkedIn", "X (Twitter)"],
		)
		self.assertEqual(payload["primary_cta_url"], "/book-a-demo/")
