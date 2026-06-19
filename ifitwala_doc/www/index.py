from __future__ import annotations

from markupsafe import Markup

import frappe

from ifitwala_doc.api.catch_all import _find_static_target

no_cache = 1

SUPPORTED_LOCALES = {"fr", "en"}
FALLBACK_LOCALE = "en"
FRENCH_DEFAULT_COUNTRIES = {
    "BE",
    "FR",
    "GF",
    "GP",
    "LU",
    "MC",
    "MQ",
    "NC",
    "PF",
    "PM",
    "RE",
    "WF",
    "YT",
}
LOCALIZED_PUBLIC_PREFIXES = {
    "",
    "about",
    "book-a-call",
    "book-a-demo",
    "data-governance",
    "docs",
    "education",
    "ifitwala-ed",
    "implementation",
    "insights",
    "platform",
    "security",
    "services",
}
UNLOCALIZED_PREFIXES = {
    "api",
    "app",
    "assets",
    "desk",
    "files",
    "private",
}


def _request_path() -> str:
    request = getattr(frappe.local, "request", None)
    path = getattr(request, "path", None) or getattr(frappe.local, "path", None)
    return path or "/"


def _normalized_parts(path: str) -> list[str]:
    return [part for part in (path or "/").split("/") if part]


def _is_public_locale_candidate(path: str) -> bool:
    parts = _normalized_parts(path)
    if parts and parts[0] in SUPPORTED_LOCALES:
        return False
    first = parts[0] if parts else ""
    if first in UNLOCALIZED_PREFIXES:
        return False
    return first in LOCALIZED_PUBLIC_PREFIXES


def _request_method() -> str:
    request = getattr(frappe.local, "request", None)
    return (getattr(request, "method", None) or "GET").upper()


def _cookie_locale() -> str | None:
    request = getattr(frappe.local, "request", None)
    cookies = getattr(request, "cookies", None) or {}
    locale = (cookies.get("ifw_locale") or "").strip().lower()
    return locale if locale in SUPPORTED_LOCALES else None


def _country_header() -> str:
    request = getattr(frappe.local, "request", None)
    headers = getattr(request, "headers", None) or {}
    for key in ("CF-IPCountry", "X-Country-Code", "X-Appengine-Country", "CloudFront-Viewer-Country"):
        value = (headers.get(key) or "").strip().upper()
        if value and value != "XX":
            return value
    return ""


def _accept_language_locale() -> str | None:
    request = getattr(frappe.local, "request", None)
    headers = getattr(request, "headers", None) or {}
    raw = headers.get("Accept-Language") or ""
    weighted: list[tuple[float, str]] = []
    for idx, item in enumerate(raw.split(",")):
        token = item.strip()
        if not token:
            continue
        lang, _, params = token.partition(";")
        q = 1.0
        if "q=" in params:
            try:
                q = float(params.split("q=", 1)[1].split(";", 1)[0])
            except ValueError:
                q = 0.0
        primary = lang.split("-", 1)[0].lower()
        if primary in SUPPORTED_LOCALES:
            weighted.append((q - (idx * 0.001), primary))
    if not weighted:
        return None
    weighted.sort(reverse=True)
    return weighted[0][1]


def _preferred_locale() -> str:
    cookie_locale = _cookie_locale()
    if cookie_locale:
        return cookie_locale

    country = _country_header()
    if country in FRENCH_DEFAULT_COUNTRIES:
        return "fr"

    language_locale = _accept_language_locale()
    if language_locale:
        return language_locale

    return FALLBACK_LOCALE


def _localized_target(path: str, locale: str) -> str:
    normalized = "/" + "/".join(_normalized_parts(path))
    if normalized != "/":
        normalized = normalized.rstrip("/") + "/"
    target = f"/{locale}{normalized}"
    request = getattr(frappe.local, "request", None)
    query = getattr(request, "query_string", b"") or b""
    if isinstance(query, bytes):
        query = query.decode("utf-8", errors="ignore")
    if query:
        target = f"{target}?{query}"
    return target


def _redirect_to_locale(path: str) -> bool:
    if _request_method() != "GET" or not _is_public_locale_candidate(path):
        return False

    locale = _preferred_locale()
    target = _localized_target(path, locale)
    if not _find_static_target(target.split("?", 1)[0]):
        return False

    frappe.local.response["type"] = "redirect"
    frappe.local.response["location"] = target
    frappe.local.response["status_code"] = 302
    cookie_manager = getattr(frappe.local, "cookie_manager", None)
    if cookie_manager:
        cookie_manager.set_cookie(
            "ifw_locale",
            locale,
            max_age=60 * 60 * 24 * 365,
            path="/",
            samesite="Lax",
        )
    return True


def _fallback_html() -> str:
    return """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Ifitwala - Page not built</title>
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="robots" content="noindex" />
  </head>
  <body>
    <main style="font-family: system-ui, sans-serif; max-width: 42rem; margin: 4rem auto; padding: 0 1.5rem; line-height: 1.5;">
      <h1>Static page not built yet</h1>
      <p>The requested Ifitwala page was not found in the deployed static assets. Run <code>./deploy_docs.sh</code> from the app root and refresh.</p>
    </main>
  </body>
</html>"""


def get_context(context):
    context.no_cache = 1
    context.base_template = ""

    request_path = _request_path()
    if _redirect_to_locale(request_path):
        context.static_html = Markup("")
        return

    target = _find_static_target(request_path)
    if target:
        context.static_html = Markup(target.read_text(encoding="utf-8"))
    else:
        context.static_html = Markup(_fallback_html())
