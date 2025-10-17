// src/main.js

// ifitwala_doc/src/main.js
import { createApp } from "vue";

// Map RPC "type" → component files
const registry = {
  "Hero": () => import("./components/Hero.vue"),
  "Feature Highlights": () => import("./components/FeatureHighlights.vue"),
};

// Fetch a page from our whitelisted RPC
async function getPage(slug = "/") {
  const res = await fetch(
    `/api/method/ifitwala_doc.api.site.get_page?slug=${encodeURIComponent(slug)}`
  );
  const { message } = await res.json();
  return message;
}

// Create and mount each section island
async function mountSection(type, props, parent) {
  const loader = registry[type];
  if (!loader) return; // unknown block type → skip
  const mod = await loader();
  const Comp = mod.default || mod;
  const el = document.createElement("div");
  el.setAttribute("data-vue", type);
  parent.appendChild(el);
  createApp(Comp, props).mount(el);
}

// Boot on marketing pages (home.html/index.html add the data hook if needed)
export async function renderMarketingPage() {
  const root = document.querySelector("#home-sections") || document.body;
  const slug = window.location.pathname || "/";
  const page = await getPage(slug);

  for (const { type, props } of page.sections || []) {
    await mountSection(type, props, root);
  }

  // (Optional) set document title from SEO
  if (page.seo?.title) document.title = page.seo.title;
}

// Run automatically when #home-sections exists
if (document.querySelector("#home-sections")) {
  renderMarketingPage();
}

