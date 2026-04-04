from __future__ import annotations

import os
from pathlib import Path

import frappe


def _normalize_path(path: str | None) -> str:
    slug = (path or "").strip()
    if not slug:
        return "/"
    parts = [part for part in slug.split("/") if part]
    return f"/{'/'.join(parts)}" if parts else "/"


def _resolve_assets_root() -> Path:
    app_root = Path(frappe.get_app_path("ifitwala_doc")).resolve()
    project_root = app_root.parent
    bench_root = project_root.parent.parent

    site_candidates = [
        getattr(frappe.local, "sites_path", None),
        os.environ.get("FRAPPE_SITES_PATH"),
        str(bench_root / "sites"),
    ]

    resolved_candidates: list[Path] = []
    for candidate in site_candidates:
        if not candidate:
            continue
        candidate_path = Path(str(candidate)).expanduser()
        if candidate_path.is_absolute():
            resolved_candidates.append(candidate_path)
            continue
        for anchor in (bench_root, Path.cwd()):
            resolved_candidates.append((anchor / candidate_path).resolve())

    for candidate in resolved_candidates:
        if candidate.is_dir() and candidate.name == "sites":
            return candidate / "assets" / "ifitwala_doc"

    return (bench_root / "sites" / "assets" / "ifitwala_doc").resolve()


def _static_candidates(path: str | None) -> tuple[str, ...]:
    normalized = _normalize_path(path)
    if normalized == "/":
        return ("index.html", "index/index.html")

    trimmed = normalized.lstrip("/")
    return (
        f"{trimmed}/index.html",
        f"{trimmed}.html",
        f"{trimmed}/index/index.html",
    )


def _find_static_target(path: str | None, assets_root: Path | None = None) -> Path | None:
    root = (assets_root or _resolve_assets_root()).resolve()
    if not root.exists():
        return None

    for relative_target in _static_candidates(path):
        candidate = (root / relative_target).resolve()
        try:
            candidate.relative_to(root)
        except ValueError:
            continue
        if candidate.is_file():
            return candidate
    return None


def _published_web_page_exists(slug: str) -> bool:
    page = frappe.get_all(
        "Ifitwala Web Page",
        filters={"slug": slug, "is_published": 1},
        fields=["name"],
        limit=1,
    )
    return bool(page)


def _serve_loader():
    loader_path = Path(frappe.get_app_path("ifitwala_doc", "www", "index.html"))
    html = loader_path.read_text(encoding="utf-8")
    frappe.local.response.type = "page"
    frappe.local.response.data = html
    frappe.local.response.headers = frappe.local.response.get("headers") or {}
    frappe.local.response.headers["Content-Type"] = "text/html; charset=utf-8"
    return html


def handle(path: str):
    """Serve the static site loader for Astro routes and published web pages."""
    try:
        slug = _normalize_path(path)
        has_static_route = _find_static_target(slug) is not None
        if not has_static_route and not _published_web_page_exists(slug):
            return

        return _serve_loader()
    except Exception:
        frappe.log_error("Error handling marketing catch-all", "ifitwala_doc")
        return
