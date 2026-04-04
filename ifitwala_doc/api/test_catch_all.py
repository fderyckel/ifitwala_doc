# Copyright (c) 2025, François de Ryckel and Contributors
# See license.txt

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import patch

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

    def test_resolve_loader_route_ignores_missing_static_route(self):
        with TemporaryDirectory() as tmpdir:
            assets_root = Path(tmpdir)

            with patch("ifitwala_doc.api.catch_all._resolve_assets_root", return_value=assets_root):
                resolved = catch_all.resolve_loader_route("/docs/fr")

        self.assertIsNone(resolved)
