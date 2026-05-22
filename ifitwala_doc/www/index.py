from __future__ import annotations

from markupsafe import Markup

import frappe

from ifitwala_doc.api.catch_all import _find_static_target

no_cache = 1


def _request_path() -> str:
    request = getattr(frappe.local, "request", None)
    path = getattr(request, "path", None) or getattr(frappe.local, "path", None)
    return path or "/"


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

    target = _find_static_target(_request_path())
    if target:
        context.static_html = Markup(target.read_text(encoding="utf-8"))
    else:
        context.static_html = Markup(_fallback_html())
