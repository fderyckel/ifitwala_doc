# ifitwala_doc/ifitwala_doc/api/build.py

import os, subprocess, shlex, shutil
import frappe

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

    # ───────────────────────── Paths ─────────────────────────
    app_root  = frappe.get_app_path("ifitwala_doc")          # apps/ifitwala_doc/ifitwala_doc
    proj_root = os.path.dirname(app_root)                    # apps/ifitwala_doc
    bench_root = os.path.dirname(os.path.dirname(proj_root)) # <bench>

    # Use the *shared* assets dir: <bench>/sites/assets/ifitwala_doc
    # (Frappe serves static from sites/assets) :contentReference[oaicite:0]{index=0}
    site_candidates = [
        getattr(frappe.local, "sites_path", None),
        os.environ.get("FRAPPE_SITES_PATH"),
        os.path.join(bench_root, "sites"),
    ]
    resolved_sites = []
    for candidate in site_candidates:
        if not candidate:
            continue
        if os.path.isabs(candidate):
            resolved_sites.append(os.path.normpath(candidate))
        else:
            for anchor in (bench_root, os.getcwd()):
                resolved_sites.append(os.path.normpath(os.path.join(anchor, candidate)))
    sites_dir = next(
        (
            path
            for path in resolved_sites
            if os.path.isdir(path) and os.path.basename(path.rstrip(os.sep)) == "sites"
        ),
        None,
    )
    if not sites_dir:
        sites_dir = os.path.join(bench_root, "sites")
    sites_dir = os.path.normpath(sites_dir)
    out_root  = os.path.join(sites_dir, "assets", "ifitwala_doc")
    dest_docs = os.path.join(out_root, "docs")
    dest_ast  = os.path.join(out_root, "_astro")
    os.makedirs(dest_docs, exist_ok=True)
    os.makedirs(dest_ast,  exist_ok=True)

    # ───────────────────── Environment ───────────────────────
    env = os.environ.copy()
    # Make yarn/node visible in worker env
    env["PATH"] = os.pathsep.join(["/usr/local/bin", "/usr/bin", "/bin", env.get("PATH", "")])
    env.setdefault("NODE_ENV", "production")  # build env can be production

    yarn_bin = shutil.which("yarn", path=env["PATH"])
    if not yarn_bin:
        frappe.throw("yarn not found on PATH for the worker. PATH=" + env.get("PATH", ""))

    # ─────────────────────── Build step ──────────────────────
    # 1) Install with devDependencies so 'astro' exists
    _run(f"{shlex.quote(yarn_bin)} install --frozen-lockfile --check-files --production=false",
         cwd=proj_root, env=env)

    # (optional diagnostics)
    _run(f"{shlex.quote(yarn_bin)} --version", cwd=proj_root, env=env)
    _run("node --version", cwd=proj_root, env=env)

    # 2) Build via package.json script (runs 'astro build')
    _run(f"{shlex.quote(yarn_bin)} astro:build", cwd=proj_root, env=env)

    # 3) Deploy built assets
    built_docs = os.path.join(proj_root, "dist", "docs")
    built_ast  = os.path.join(proj_root, "dist", "_astro")
    if not os.path.isdir(built_docs):
        frappe.throw("Astro build did not produce dist/docs")

    # Absolute paths; neutral cwd avoids accidental relatives
    _run(f"rsync -a --delete {shlex.quote(built_docs)}/ {shlex.quote(dest_docs)}/", cwd="/", env=env)
    if os.path.isdir(built_ast):
        _run(f"rsync -a --delete {shlex.quote(built_ast)}/ {shlex.quote(dest_ast)}/", cwd="/", env=env)

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
