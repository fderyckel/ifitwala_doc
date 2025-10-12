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
    """Build docs with Astro (yarn) and deploy to sites/assets/ifitwala_doc."""
    import os, shlex, shutil
    import frappe

    # ── Paths
    app_root  = frappe.get_app_path("ifitwala_doc")                  # apps/ifitwala_doc/ifitwala_doc
    proj_root = os.path.dirname(app_root)                             # apps/ifitwala_doc
    out_root  = frappe.utils.get_site_path("assets", "ifitwala_doc")  # /.../sites/assets/ifitwala_doc

    # Ensure deploy targets exist (rsync --delete expects dirs to exist)
    dest_docs = os.path.join(out_root, "docs")
    dest_ast  = os.path.join(out_root, "_astro")
    os.makedirs(dest_docs, exist_ok=True)
    os.makedirs(dest_ast,  exist_ok=True)

    # ── Environment (ensure yarn/node are discoverable in worker)
    env = os.environ.copy()
    extra_paths = ["/usr/local/bin", "/usr/bin", "/bin"]
    env["PATH"] = os.pathsep.join(extra_paths + [env.get("PATH", "")])
    env.setdefault("NODE_ENV", "production")  # build env is fine as production

    # Resolve yarn absolute path
    yarn_bin = shutil.which("yarn", path=env["PATH"])
    if not yarn_bin:
        frappe.throw("yarn not found on PATH for the worker. PATH=" + env.get("PATH", ""))

    # ── 1) Install (force devDependencies so 'astro' is present)
    _run(f"{shlex.quote(yarn_bin)} install --frozen-lockfile --check-files --production=false",
         cwd=proj_root, env=env)

    # (optional diagnostics)
    _run(f"{shlex.quote(yarn_bin)} --version", cwd=proj_root, env=env)
    _run("node --version", cwd=proj_root, env=env)

    # ── 2) Build via package.json script
    _run(f"{shlex.quote(yarn_bin)} astro:build", cwd=proj_root, env=env)

    # ── 3) Deploy built assets (use absolute paths)
    built_docs = os.path.join(proj_root, "dist", "docs")
    built_ast  = os.path.join(proj_root, "dist", "_astro")
    if not os.path.isdir(built_docs):
        frappe.throw("Astro build did not produce dist/docs")

    _run(f"rsync -a --delete {shlex.quote(built_docs)}/ {shlex.quote(dest_docs)}/",
         cwd="/", env=env)

    if os.path.isdir(built_ast):
        _run(f"rsync -a --delete {shlex.quote(built_ast)}/ {shlex.quote(dest_ast)}/",
             cwd="/", env=env)


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
