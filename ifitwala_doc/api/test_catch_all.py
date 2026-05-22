# Copyright (c) 2025, François de Ryckel and Contributors
# See license.txt

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import patch

import frappe

from ifitwala_doc.api import catch_all


class TestCatchAll(TestCase):
    def test_find_static_target_matches_docs_language_index(self):
        with TemporaryDirectory() as tmpdir:
            assets_root = Path(tmpdir)
            target = assets_root / "docs" / "en" / "index.html"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("<html>Docs</html>", encoding="utf-8")

            found = catch_all._find_static_target("/docs/en", assets_root=assets_root)

        self.assertEqual(found, target)

    def test_find_static_target_normalizes_duplicate_and_trailing_slashes(self):
        with TemporaryDirectory() as tmpdir:
            assets_root = Path(tmpdir)
            target = assets_root / "docs" / "en" / "getting-started" / "index.html"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("<html>Guide</html>", encoding="utf-8")

            found = catch_all._find_static_target("//docs//en//getting-started//", assets_root=assets_root)

        self.assertEqual(found, target)

    def test_resolve_loader_route_returns_index_for_built_static_route(self):
        with TemporaryDirectory() as tmpdir:
            assets_root = Path(tmpdir)
            target = assets_root / "book-a-demo" / "index.html"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("<html>Demo</html>", encoding="utf-8")

            with patch("ifitwala_doc.api.catch_all._resolve_assets_root", return_value=assets_root):
                resolved = catch_all.resolve_loader_route("/book-a-demo")

        self.assertEqual(resolved, "index")

    def test_resolve_loader_route_returns_index_for_built_homepage(self):
        with TemporaryDirectory() as tmpdir:
            assets_root = Path(tmpdir)
            target = assets_root / "index.html"
            target.write_text("<html>Home</html>", encoding="utf-8")

            with patch("ifitwala_doc.api.catch_all._resolve_assets_root", return_value=assets_root):
                resolved = catch_all.resolve_loader_route("/")

        self.assertEqual(resolved, "index")

    def test_resolve_loader_route_disables_frappe_page_cache_for_static_bridge(self):
        previous_no_cache = getattr(frappe.local, "no_cache", None)
        frappe.local.no_cache = False

        try:
            with TemporaryDirectory() as tmpdir:
                assets_root = Path(tmpdir)
                target = assets_root / "index.html"
                target.write_text("<html>Home</html>", encoding="utf-8")

                with patch("ifitwala_doc.api.catch_all._resolve_assets_root", return_value=assets_root):
                    catch_all.resolve_loader_route("/")

            self.assertTrue(frappe.local.no_cache)
        finally:
            frappe.local.no_cache = previous_no_cache

    def test_resolve_loader_route_ignores_missing_static_route(self):
        with TemporaryDirectory() as tmpdir:
            assets_root = Path(tmpdir)

            with patch("ifitwala_doc.api.catch_all._resolve_assets_root", return_value=assets_root):
                with patch("ifitwala_doc.api.catch_all.resolve_path", return_value="docs/preview") as resolve_path:
                    resolved = catch_all.resolve_loader_route("/docs/preview/en/school")

        self.assertEqual(resolved, "docs/preview")
        resolve_path.assert_called_once_with("docs/preview/en/school")
