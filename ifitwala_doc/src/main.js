// src/main.js

import { createApp } from "vue";

import { FrappeUI } from 'frappe-ui';
import { createRouter, createWebHistory } from 'vue-router';

// Map RPC "type" → component
const registry = {
  "Hero": () => import("./components/Hero.vue"),
  "Feature Highlights": () => import("./components/FeatureHighlights.vue"), // create if not present
};

// Fetch a page from Frappe
async function getPage(slug = "/") {
  const res = await fetch(`/api/method/ifitwala_doc.api.site.get_page?slug=${encodeURIComponent(slug)}`);
  const { message } = await res.json();
  return message;
}

// Create and mount each section island
async function mountSection(type, props, parent) {
  const loader = registry[type];
  if (!loader) return;
  const mod = await loader();
  const Comp = mod.default || mod;
  const el = document.createElement("div");
  el.setAttribute("data-vue", type);
  parent.appendChild(el);
  createApp(Comp, props).mount(el);
}

// Boot on marketing pages
export async function renderMarketingPage() {
  const root = document.querySelector("#home-sections") || document.body;
  const slug = window.location.pathname || "/";
  const page = await getPage(slug);

  for (const { type, props } of page.sections || []) {
    // Mount in order coming from the Desk
    await mountSection(type, props, root);
  }

  // (Optional) set title/SEO on client; SSR later in Jinja
  if (page.seo?.title) document.title = page.seo.title;
}

if (document.documentElement.matches('[data-marketing="home"]')) {
  renderMarketingPage();
}
