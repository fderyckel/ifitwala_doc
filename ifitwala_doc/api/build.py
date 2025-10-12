# ifitwala_doc/ifitwala_doc/api/build.py

import os, subprocess, shlex, shutil
import frappe
from frappe.utils import get_site_path

def _require_token():
    expected = frappe.conf.get("docs_build_token")
    got = frappe.get_request_header("X-Ifitwala-Docs-Token")
    if not expected or got != expected:
        frappe.throw("Unauthorized", frappe.PermissionError)



def _run(cmd, cwd, env=None):
    proc = subprocess.run(
        cmd, cwd=cwd, shell=True, env=env,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )
    frappe.logger("ifitwala_doc").info(proc.stdout)
    if proc.returncode != 0:
        frappe.throw(f"Command failed: {cmd}\n{proc.stdout}")

@frappe.whitelist(allow_guest=True)
def trigger():
    _require_token()
    frappe.enqueue("ifitwala_doc.api.build.run_astro_build", queue="short")
    return {"queued": True}

def run_astro_build():
    app_root = frappe.get_app_path("ifitwala_doc")
    proj_root = os.path.dirname(app_root)
    out_root  = get_site_path("assets", "ifitwala_doc")
    os.makedirs(out_root, exist_ok=True)

    env = os.environ.copy()

    # Ensure PATH includes common bin dirs so workers find node/yarn
    extra_paths = ["/usr/local/bin", "/usr/bin", "/bin"]
    env["PATH"] = os.pathsep.join(extra_paths + [env.get("PATH", "")])

    yarn_bin = shutil.which("yarn", path=env["PATH"])
    if not yarn_bin:
        frappe.throw("yarn not found on PATH for the worker. PATH=" + env.get("PATH",""))

    # 1) install — FORCE devDependencies available for Astro
    #    (don’t rely on NODE_ENV=production which would skip dev deps)
    install_cmd = f"{shlex.quote(yarn_bin)} install --frozen-lockfile --check-files --production=false"
    _run(install_cmd, cwd=proj_root, env=env)

    # (optional) small diagnostics
    _run(f"{shlex.quote(yarn_bin)} --version", cwd=proj_root, env=env)
    _run("node --version", cwd=proj_root, env=env)

    # 2) build using the script defined in package.json
    build_cmd = f"{shlex.quote(yarn_bin)} astro:build"
    _run(build_cmd, cwd=proj_root, env=env)

    # 3) deploy as before...
    built_docs = os.path.join(proj_root, "dist", "docs")
    built_ast  = os.path.join(proj_root, "dist", "_astro")
    if not os.path.isdir(built_docs):
        frappe.throw("Astro build did not produce dist/docs")

    _run(f"rsync -a --delete {shlex.quote(built_docs)}/ {shlex.quote(os.path.join(out_root, 'docs'))}/", cwd=proj_root, env=env)

    if os.path.isdir(built_ast):
        _run(f"rsync -a --delete {shlex.quote(built_ast)}/ {shlex.quote(os.path.join(out_root, '_astro'))}/", cwd=proj_root, env=env)



@frappe.whitelist(allow_guest=True)
def debug_headers():
    return {
        "headers": frappe.local.request.headers,
        "token": frappe.get_conf().get("docs_build_token"),
        "site": frappe.local.site
    }


@frappe.whitelist()
def kick_build():
    """Server-side trigger so Desk JS doesn't handle tokens.
    Restrict to trusted roles.
    """
    frappe.only_for(("System Manager", "Website Manager"))
    from ifitwala_doc.ifitwala_doc.published_utils import ping_build
    ping_build()
    return {"queued": True}
