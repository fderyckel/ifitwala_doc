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
    """Build the Astro site (marketing + docs) and deploy to sites/assets/ifitwala_doc."""
    import os, shlex, shutil
    import frappe

    def _normalize_path_entries(value):
        """Return a list of absolute path entries from strings / iterables."""
        if not value:
            return []
        if isinstance(value, (list, tuple, set)):
            raw_entries = value
        else:
            raw_entries = str(value).split(os.pathsep)
        entries = []
        for entry in raw_entries:
            if not entry:
                continue
            entry = os.path.expanduser(str(entry)).strip()
            if entry:
                entries.append(os.path.normpath(entry))
        return entries

    def _parse_semver_from_path(bin_path):
        """Parse ~/.nvm/.../vX.Y.Z/bin into (major, minor, patch) or None."""
        try:
            version_dir = os.path.basename(os.path.dirname(bin_path))  # v22.12.0
            raw = version_dir.lstrip("vV")
            parts = raw.split(".")
            major = int(parts[0])
            minor = int(parts[1]) if len(parts) > 1 else 0
            patch = int(parts[2]) if len(parts) > 2 else 0
            return major, minor, patch
        except Exception:
            return None

    def _preferred_node_majors():
        configured = (
            env.get("IFITWALA_DOC_NODE_PREFERRED_MAJORS")
            or frappe.conf.get("docs_build_node_preferred_majors")
            or "24,22,20"
        )
        values = []
        for token in str(configured).split(","):
            token = token.strip()
            if not token:
                continue
            try:
                values.append(int(token))
            except ValueError:
                continue
        return values or [24, 22, 20]

    def _sort_nvm_bins(paths):
        """Prefer known stable LTS majors before other versions."""
        preferred = _preferred_node_majors()
        priority_map = {major: idx for idx, major in enumerate(preferred)}

        def key(path):
            parsed = _parse_semver_from_path(path)
            if not parsed:
                return (len(preferred) + 1, 0, 0, 0)
            major, minor, patch = parsed
            priority = priority_map.get(major, len(preferred))
            return (priority, -major, -minor, -patch)

        return sorted(paths, key=key)

    def _resolve_yarn(execution_env, project_root):
        """Return (yarn_invocation_path, requires_node_wrapper)."""
        explicit_bins = [
            execution_env.get("IFITWALA_DOC_YARN_BIN"),
            frappe.conf.get("docs_build_yarn_bin"),
        ]
        for candidate in explicit_bins:
            if not candidate:
                continue
            candidate_path = os.path.expanduser(str(candidate))
            if os.path.isfile(candidate_path):
                return candidate_path, False

        local_wrappers = [
            os.path.join(project_root, "node_modules", ".bin", "yarn"),
            os.path.join(project_root, ".yarn", "bin", "yarn"),
        ]
        for candidate in local_wrappers:
            if os.path.isfile(candidate):
                return candidate, False

        releases_dir = os.path.join(project_root, ".yarn", "releases")
        if os.path.isdir(releases_dir):
            release_files = sorted(
                (
                    name
                    for name in os.listdir(releases_dir)
                    if name.startswith("yarn-") and name.endswith((".cjs", ".js"))
                ),
                reverse=True,
            )
            for name in release_files:
                release_path = os.path.join(releases_dir, name)
                if os.path.isfile(release_path):
                    return release_path, True  # run via `node`

        return shutil.which("yarn", path=execution_env.get("PATH") or ""), False

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
    os.makedirs(out_root, exist_ok=True)

    # ───────────────────── Environment ───────────────────────
    env = os.environ.copy()
    env.setdefault("NODE_ENV", "production")  # build env can be production

    # Load .env file manually since we aren't in a shell that sources it
    dotenv_path = os.path.join(proj_root, ".env")
    if os.path.isfile(dotenv_path):
        with open(dotenv_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                # Remove quotes if present
                v = v.strip("'\"")
                env.setdefault(k.strip(), v)

    original_path = env.get("PATH", "")
    import glob

    path_hints = [
        "/usr/local/bin",
        "/usr/local/sbin",
        "/usr/bin",
        "/usr/sbin",
        "/bin",
        os.path.join(proj_root, "node_modules", ".bin"),
        os.path.join(proj_root, ".yarn", "bin"),
    ]
    
    # Explicit Node binary path override (if configured)
    explicit_node_bin = env.get("IFITWALA_DOC_NODE_BIN") or frappe.conf.get("docs_build_node_bin")
    if explicit_node_bin:
        explicit_node_dir = os.path.dirname(os.path.expanduser(str(explicit_node_bin)))
        if explicit_node_dir:
            path_hints.insert(0, os.path.normpath(explicit_node_dir))

    # Attempt to find NVM paths
    nvm_paths = glob.glob(os.path.expanduser("~/.nvm/versions/node/*/bin"))
    if not nvm_paths:
        # Fallback: check based on bench_root ownership if running as root/restricted
        possible_home = os.path.dirname(os.path.dirname(bench_root)) # /home/user or /opt
        nvm_paths = glob.glob(os.path.join(possible_home, ".nvm/versions/node/*/bin"))
    
    if nvm_paths:
        nvm_paths = _sort_nvm_bins(nvm_paths)
        path_hints.extend(nvm_paths)

    path_hints.extend(_normalize_path_entries(frappe.conf.get("docs_build_yarn_paths")))
    path_hints.extend(_normalize_path_entries(env.get("IFITWALA_DOC_YARN_PATHS")))
    if original_path:
        path_hints.append(original_path)
    env["PATH"] = os.pathsep.join(filter(None, path_hints))

    yarn_path, needs_node_wrapper = _resolve_yarn(env, proj_root)
    if not yarn_path:
        searched = "\n".join(f"  - {entry}" for entry in path_hints if entry)
        frappe.throw(
            "yarn not found for docs build.\n"
            "Checked:\n"
            f"{searched}\n"
            f"PATH={env.get('PATH', '')}"
        )
    yarn_prefix = f"node {shlex.quote(yarn_path)}" if needs_node_wrapper else shlex.quote(yarn_path)

    def run_yarn(args):
        command = yarn_prefix if not args else f"{yarn_prefix} {args}"
        _run(command, cwd=proj_root, env=env)

    # ─────────────────────── Status Update (Start) ────────────────
    settings = frappe.get_single("Ifitwala Website Settings")
    settings.last_build_status = "Pending"
    settings.save(ignore_permissions=True)
    frappe.db.commit()

    # ─────────────────────── Build step ──────────────────────
    try:
        # 1) Install with devDependencies so 'astro' exists
        run_yarn("install --frozen-lockfile --check-files --production=false")

        # (optional diagnostics)
        run_yarn("--version")
        _run("node --version", cwd=proj_root, env=env)

        # 2) Build via package.json script (runs marketing assets and Astro pages)
        try:
            run_yarn("build")
        except Exception as build_error:
            error_text = str(build_error).lower()
            # Astro can fail when stale compile artifacts are present in dist/.astro.
            # Retry once after clearing caches for known missing-generated-module patterns.
            missing_renderer = "renderers.mjs" in error_text
            missing_page_module = (
                "cannot find module" in error_text
                and "/dist/pages/" in error_text
                and ".astro.mjs" in error_text
            )
            if not (missing_renderer or missing_page_module):
                raise
            dist_dir = os.path.join(proj_root, "dist")
            astro_cache_dir = os.path.join(proj_root, ".astro")
            _run(
                f"rm -rf {shlex.quote(dist_dir)} {shlex.quote(astro_cache_dir)}",
                cwd="/",
                env=env,
            )
            run_yarn("build")

        # 3) Deploy built assets
        dist_root = os.path.join(proj_root, "dist")
        if not os.path.isdir(dist_root):
            frappe.throw("Astro build did not produce dist/")

        # Absolute paths; neutral cwd avoids accidental relatives
        _run(f"rsync -a --delete {shlex.quote(dist_root)}/ {shlex.quote(out_root)}/", cwd="/", env=env)

        # ─────────────────── Status Update (Success) ────────────────
        settings.last_build_status = "Success"
        settings.last_build_time = frappe.utils.now()
        settings.last_build_log = "Build completed successfully."
        settings.save(ignore_permissions=True)
        frappe.db.commit()

        frappe.publish_realtime(
            "astro_build_status",
            {"status": "completed", "message": "Website deployed successfully!"},
            user=frappe.session.user
        )

    except Exception as e:
        frappe.logger("ifitwala_doc").error(f"Build failed: {e}", exc_info=True)
        
        # ─────────────────── Status Update (Failure) ────────────────
        settings.last_build_status = "Failed"
        settings.last_build_time = frappe.utils.now()
        settings.last_build_log = str(e)
        settings.save(ignore_permissions=True)
        frappe.db.commit()

        frappe.publish_realtime(
            "astro_build_status",
            {"status": "failed", "message": f"Build failed: {str(e)}"},
            user=frappe.session.user
        )
        raise e


@frappe.whitelist(allow_guest=True)
def debug_headers():
    return {
        "headers": frappe.local.request.headers,
        "token": frappe.get_conf().get("docs_build_token"),
        "site": frappe.local.site
    }


@frappe.whitelist()
def kick_build():
    """Trigger the Astro build process directly from the Desk."""
    frappe.only_for(("System Manager", "Website Manager"))
    
    frappe.enqueue(
        "ifitwala_doc.api.build.run_astro_build",
        queue="long",
        timeout=1500
    )
    
    return {"queued": True, "message": "Build started. You will be notified when complete."}
