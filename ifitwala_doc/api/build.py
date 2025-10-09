# ifitwala_doc/ifitwala_doc/api/build.py

import os, subprocess, shlex
import frappe
from frappe.utils import get_site_path

def _require_token():
    expected = frappe.conf.get("docs_build_token")
    got = frappe.get_request_header("X-Ifitwala-Docs-Token")
    if not expected or got != expected:
        frappe.throw("Unauthorized", frappe.PermissionError)

def _run(cmd, cwd):
    proc = subprocess.run(cmd, cwd=cwd, shell=True,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    frappe.logger("ifitwala_doc").info(proc.stdout)
    if proc.returncode != 0:
        frappe.throw(f"Command failed: {cmd}\n{proc.stdout}")

@frappe.whitelist(allow_guest=True)
def trigger():
    _require_token()
    frappe.enqueue("ifitwala_doc.api.build.run_astro_build", queue="short")
    return {"queued": True}

def run_astro_build():
    app_root = frappe.get_app_path("ifitwala_doc")              # apps/ifitwala_doc/ifitwala_doc
    proj_root = os.path.dirname(app_root)                        # apps/ifitwala_doc
    out_dir   = get_site_path("assets", "ifitwala_doc", "docs")  # sites/assets/ifitwala_doc/docs
    os.makedirs(out_dir, exist_ok=True)

    _run("npm ci --prefer-offline --no-audit", cwd=proj_root)
    _run("npx astro build", cwd=proj_root)

    built_docs = os.path.join(proj_root, "dist", "docs")
    if not os.path.isdir(built_docs):
        frappe.throw("Astro build did not produce dist/docs")
    _run(f"rsync -a --delete {shlex.quote(built_docs)}/ {shlex.quote(out_dir)}/", cwd=proj_root)

@frappe.whitelist(allow_guest=True)
def debug_headers():
    return {
        "headers": frappe.local.request.headers,
        "token": frappe.get_conf().get("docs_build_token"),
        "site": frappe.local.site
    }
