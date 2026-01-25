# AGENTS.md

## Project Architecture: Frappe + Astro Hybrid

This repository (`ifitwala_doc`) implements a **Hybrid Monorepo** pattern combining:
1.  **Frappe App** (Backend/CMS): Manages content, authentication, and dynamic API endpoints.
2.  **Astro Project** (Frontend/SSG): Consumes Frappe content via API and builds static marketing/documentation pages.

### Content Flow
- **Source of Truth**: Frappe DocTypes (`Ifitwala Web Page`, `Documentation`).
- **Build Process**: Astro fetches content from `https://ifitwala.com` (defined in `.env` as `PUBLIC_DOCS_API`) and generates static HTML.
- **Serving**:
    - **Dynamic**: Handled by Frappe (Python/Gunicorn).
    - **Static (`/docs`, `/features`)**: Handled by Nginx, serving pre-built assets from `sites/assets/ifitwala_doc`.

### Integration Points
- **Trigger**: "Deploy Website" button in `Ifitwala Website Settings` (Desk UI).
- **Execution**: Python `frappe.enqueue` $\rightarrow$ `api/build.py` $\rightarrow$ `yarn astro:build`.
- **Deployment**: `rsync` moves `dist/` $\rightarrow$ `frappe-bench/sites/assets/ifitwala_doc`.

---

## Lessons Learned (The "Gotchas")

### 1. Nginx Configuration Management
**Issue**: Placing a file with `location` directives directly into `/etc/nginx/conf.d/*.conf` causes global config errors ("location directive not allowed here").
**Solution**:
- Generate config snippets as `.inc` files (e.g., `ifitwala_doc_static.inc`).
- **Manually include** them inside the specific `server { ... }` block of the main site config.
- **Critical**: Ensure the include is placed in the **SSL (Port 443)** block, not just the HTTP redirect block, or users won't see the changes.

### 2. Execution Environment (PATH & Env Vars)
**Issue**: Background workers (Supervisor/Redis Queue) often run with a restricted `PATH` and do not source shell profiles (`.bashrc`, `.zshrc`).
**Solution**:
- **Explicit Path Discovery**: Do not assume `yarn` or `node` are in the path. Checks must explicitly look for NVM directories (`~/.nvm/...`) and add them to `os.environ["PATH"]`.
- **Manual .env Loading**: Python scripts running outside a shell setup must manually parse and load `.env` files. Failing to do so can lead to "silent successes" where the build runs but generates empty pages because API URLs were missing.

### 3. Permissions & Context
**Issue**: Scripts created by the agent might lack execution permissions (`chmod +x`).
**Solution**: Always verify or explicitly set permissions when creating shell scripts.

---

## Deployment Commands
To manually deploy or debug:
```bash
# 1. Ensure .env has PUBLIC_DOCS_API
# 2. Run the deployment script
./deploy_docs.sh
```

To update Nginx mapping:
```bash
./install_ifitwala_nginx.sh
# Then follow instructions to edit frappe-bench.conf
```
