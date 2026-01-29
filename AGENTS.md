# AGENTS.md

## Project Architecture: Dual-Mode Hybrid

This repository (`ifitwala_doc`) implements a **Hybrid Monorepo** pattern combining a Frappe backend with two distinct frontend build pipelines. This ensures maximum SEO for documentation while allowing rich interactivity for marketing pages.

### 1. Frappe App (Backend/CMS)
- **Role**: Manages content, authentication, and dynamic API endpoints.
- **Source of Truth**: DocTypes (`Ifitwala Web Page`, `Documentation`).
- **Serving**: Python/Gunicorn handles dynamic requests; Nginx handles static assets.

### 2. Frontend Pipeline A: Static Documentation (Astro)
- **Scope**: `/docs/*`, `/features/*`.
- **Tech**: Astro SSG (`astro.config.mjs`).
- **Goal**: **Maximum SEO**, zero-JS by default (HTML-first).
- **Hydration**: Uses standard Astro Islands (e.g., `<LeadForm client:visible />`) only where strictly necessary.
- **Output**: `dist/` (Synced to `sites/assets/ifitwala_doc` via rsync).

### 3. Frontend Pipeline B: Dynamic Marketing (Vite + Vue)
- **Scope**: Homepage (`/`), Landing Pages.
- **Tech**: Frappe Jinja Templates + Vue "Islands" (`vite.config.mjs`).
- **Goal**: Rich interactivity, complex state management.
- **Mechanism**:
    - **Entry**: `src/main.js`.
    - **Hydration**: Manual. `main.js` scans the DOM for data attributes (e.g., `data-vue="Hero"`) and mounts specific Vue components from the `registry`.
- **Output**: `ifitwala_doc/public/dist/` (Bundled JS/CSS loaded by Jinja templates).

---

## Content & Build Flow

### Integration Points
- **Trigger**: "Deploy Website" button in `Ifitwala Website Settings` (Desk UI).
- **Execution**: Python `frappe.enqueue` $\rightarrow$ `api/build.py`.
- **Build Commands**:
    1. `yarn build` (Vite): Compiles `base.js` and `site.css` for the dynamic marketing pages.
    2. `yarn astro:build` (Astro): Generates the static HTML for documentation.
- **Deployment**: `rsync` moves artifacts to `frappe-bench/sites/assets/ifitwala_doc`.

### Styling Architecture
- **Framework**: Tailwind CSS.
- **Configuration**: `tailwind.config.cjs` (Shared config).
- **Entry Points**:
    - **Astro**: `src/styles/global.css` (Injected into Astro layouts).
    - **Vite**: `src/styles/tailwind.css` (Bundled into `site.css` for non-Astro pages).
    - *Note: Ensure token changes are reflected in both entry points until fully unified.*

---

## Lessons Learned (The "Gotchas")

### 1. Build Artifact Management (The "React Error #62")
**Issue**: Committing heavy build folders (`dist/`, `.astro/`) or leaving them in the workspace causes web-based IDEs (Gravity) to crash with "Minified React error #62".
**Solution**:
- **Git**: Ensure `dist/`, `.astro/`, and `ifitwala_doc/public/dist/` are in `.gitignore`.
- **Cleanup**: Build scripts should run `rm -rf dist` before starting to ensure a clean slate.

### 2. Nginx Configuration
**Issue**: `location` directives inside `/etc/nginx/conf.d/*.conf` cause global errors.
**Solution**:
- Generate `.inc` snippets (e.g., `ifitwala_doc_static.inc`).
- **Manually include** them inside the **SSL (Port 443)** server block of the main site config.

### 3. Execution Environment (PATH & Env Vars)
**Issue**: Background workers (Supervisor/Redis) run with restricted `PATH` and don't load `.bashrc`.
**Solution**:
- **Explicit Discovery**: Python build scripts must explicitly find `node`/`yarn` binaries (e.g., in `~/.nvm/...`).
- **Env Vars**: Python scripts must manually load `.env` variables (like `PUBLIC_DOCS_API`) before invoking build commands.

---

## Deployment Commands

To manually deploy or debug (runs both pipelines):
```bash
# 1. Ensure .env has PUBLIC_DOCS_API
# 2. Run the deployment script    deploy_docs.sh