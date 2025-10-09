# ifitwala_doc/ifitwala_doc/published_utils.py
import requests, frappe

def ping_build():
    url = f"{frappe.utils.get_url()}/api/method/ifitwala_doc.api.build.trigger"
    token = frappe.conf.docs_build_token
    requests.get(url, headers={"X-Ifitwala-Docs-Token": token}, timeout=5)
