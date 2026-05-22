Here’s a revised version of **AGENTS.md** that better reflects the dual-architecture setup of the repository and provides more actionable context for a coding‑focused agent:

---

# Project Architecture

## Overview

This repository is a hybrid monorepo that pairs a Frappe‑based backend with two distinct front‑end build pipelines:

* **Backend/CMS (Frappe App)** – lives under `ifitwala_doc/`
* **Static Documentation (Astro)** – source lives in the root `src/`
* **Hydrated Vue Marketing Components** – source lives in `ifitwala_doc/src/` and mounts into Astro pages

This dual‑architecture allows you to deliver zero‑JavaScript, SEO‑friendly documentation while still supporting rich interactivity on landing pages.

---

## 1. Frappe App (Backend/CMS)

* **Purpose:** Manages content, authentication and API endpoints.
* **Key Doctypes:**

  * `Ifitwala Web Page`
  * `Documentation`
* **Serving:** Dynamic routes are handled by Python/Gunicorn; static assets are served via Nginx.
* **Deployment:** Build artifacts (Astro docs and Vue marketing bundles) are synced into `frappe-bench/sites/assets/ifitwala_doc`.

---

## 2. Static Documentation Pipeline (Astro)

* **Source:** `src/` at the root of the repo.
* **Tech stack:** Astro SSG.
* **Goal:** Generate fully static HTML for docs with maximum SEO; default output is zero‑JS.
* **Content:** Markdown and MDX files under `src/pages/…`.
* **Entry points:** Global styles live in `src/styles/global.css` and are injected by Astro layouts.
* **Output:** Compiled into `dist/`; during deployment this is rsynced to `sites/assets/ifitwala_doc`.
* **Hydration:** Only when necessary; Astro islands (e.g. `<LeadForm client:visible />`) are used sparingly.

---

## 3. Dynamic Marketing Pipeline (Vite + Vue)

* **Source:** `ifitwala_doc/src/` inside the app.
* **Tech stack:** Vue 3 bundled via Vite.
* **Goal:** Deliver interactive marketing pages (home page, landing pages) that need client‑side state.
* **Mechanism:**

  * The entry point is `ifitwala_doc/src/main.js`.
  * Vue components are registered in a component registry.
  * On runtime, `main.js` scans the DOM for `data-vue="ComponentName"` attributes and hydrates those elements with the appropriate Vue component.
* **Styles:** Imported from `ifitwala_doc/src/styles/tailwind.css` and compiled into `site.css` for inclusion in Frappe templates.
* **Output:** Bundled JS/CSS is emitted to `ifitwala_doc/public/dist/` and referenced in Jinja templates (e.g. `/templates/www/index.html`).

---

## Content & Build Flow

1. **Documentation edits:** Use the `Documentation` DocType **Rebuild Docs** action for content changes. It rebuilds and deploys assets only; it should not refresh Nginx.
2. **File-based site edits:** Run `./deploy_docs.sh` from the app root after changing Astro, Vue, CSS, or static site source files. Existing Astro page edits, including `src/pages/index.astro`, do not need Nginx refresh.
3. **Serving:** Built pages are served through Frappe’s normal routing via `ifitwala_doc/www/index.py`, which reads the generated HTML from `sites/assets/ifitwala_doc`. Custom Nginx static routes are optional and should not be required for normal updates.
4. **Optional direct Nginx serving:** Run `./deploy_docs.sh --with-nginx` only when intentionally enabling or changing the optional Nginx static route snippet.
5. **Trigger:** A “Deploy Website” action in the Frappe Desk UI enqueues a build job (`api/build.py`).
6. **Build Commands:**

   * **Astro:** `yarn astro:build` generates static docs from `src/`.
   * **Vite:** `yarn build` compiles the Vue marketing bundle from `ifitwala_doc/src/`.
7. **Deployment:** Artifacts from both builds are rsynced to `frappe-bench/sites/assets/ifitwala_doc/`.
8. **Cleanup:** Build scripts remove any stale `dist/` and `.astro/` folders before building to avoid conflicts.

---

## Styling Architecture

* **Framework:** Tailwind CSS shared across both pipelines.
* **Configuration:** Defined in `tailwind.config.cjs` at the repo root.
* **Entry Points:**

  * Astro uses `src/styles/global.css`.
  * Vite/Vue uses `ifitwala_doc/src/styles/tailwind.css`.
* **Custom Tokens:** Colour, radius and shadow tokens are exposed via CSS variables (e.g. `--ink-rgb`) and referenced in Tailwind via helper functions.
* **Note:** Changes to tokens should be made in the Tailwind config so both pipelines stay in sync.

---

## Lessons Learned (Gotchas)

* **Build Artifacts:** Never commit `dist/`, `.astro/`, or `ifitwala_doc/public/dist/`. They should always be git‑ignored and cleaned before builds to prevent IDE crashes and version control noise.
* **Nginx Configuration:** Serve static assets via `.inc` snippets included in the SSL server block of your main `nginx.conf` to avoid conflicts.
* **Environment Path:** Worker processes (e.g. Celery/Redis) run with restricted environment variables. Ensure your build scripts locate `node` and `yarn` executables explicitly.
* **Colour Tokens:** If you introduce custom Tailwind colours, make sure they are accessible via `theme('colors.*')` syntax. When referencing nested values, quote the path (e.g. `theme('colors.blue.200')`) and provide a fallback if necessary.
* **Frappe DocTypes:** Every new DocType, including child tables, must include the full package shape: `__init__.py`, `<doctype>.json`, and `<doctype>.py` with the matching PascalCase controller class extending `Document`. Do not leave child-table controller files as comments-only stubs; Frappe migrate/orphan cleanup may delete the DocType even when the JSON exists.

---
