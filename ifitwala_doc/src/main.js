// src/main.js

// ifitwala_doc/src/main.js
import { createApp } from "vue";

// Map RPC "type" → component files
const registry = {
  "Hero": () => import("./components/Hero.vue"),
  "Hero Block": () => import("./components/Hero.vue"),
  "Feature Highlights": () => import("./components/FeatureHighlights.vue"),
  "Feature Highlight": () => import("./components/FeatureHighlights.vue"),
  "Trust Logos": () => import("./components/TrustLogos.vue"),
  "Trust Logo": () => import("./components/TrustLogos.vue"),
  "Testimonial Group": () => import("./components/TestimonialCarousel.vue"),
};

const HEAD = typeof document !== "undefined" ? document.head : null;

function setMetaTag(selector, attributes) {
  if (!HEAD) return;
  let el = HEAD.querySelector(selector);
  if (!el) {
    const tagName = selector.startsWith("meta") ? "meta" : "link";
    el = document.createElement(tagName);
    HEAD.appendChild(el);
  }
  Object.entries(attributes).forEach(([key, value]) => {
    if (value) {
      el.setAttribute(key, value);
    }
  });
}

function applySeo(seo = {}, fallbackTitle = "") {
  if (seo.title) {
    document.title = seo.title;
  } else if (fallbackTitle) {
    document.title = fallbackTitle;
  }
  if (seo.description) {
    setMetaTag('meta[name="description"]', { name: "description", content: seo.description });
  }
  if (seo.canonical_url) {
    setMetaTag('link[rel="canonical"]', { rel: "canonical", href: seo.canonical_url });
  }
  if (seo.og_image) {
    setMetaTag('meta[property="og:image"]', { property: "og:image", content: seo.og_image });
  }
}


// Fetch a page from our whitelisted RPC
async function getPage(slug = "/", { includeDrafts = false } = {}) {
  const qp = new URLSearchParams({ slug });
  if (includeDrafts) {
    qp.set("include_unpublished", "1");
  }
  const res = await fetch(
    `/api/method/ifitwala_doc.api.site.get_page?${qp.toString()}`
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
export async function renderMarketingPage({ slug, includeDrafts } = {}) {
  const root = document.querySelector("#home-sections") || document.body;
  const targetSlug = slug || window.location.pathname || "/";
  const page = await getPage(targetSlug, { includeDrafts });

  if (!page || !Array.isArray(page.sections)) {
    return;
  }

  // Ensure deterministic order before mounting
  const sections = [...page.sections].sort(
    (a, b) => (a?.order ?? 0) - (b?.order ?? 0)
  );

  // Clear any existing dynamic mounts (useful for hot reload)
  if (root && root.dataset && !root.dataset.static) {
    root.innerHTML = "";
  }

  for (const section of sections) {
    await mountSection(section.type, section.props, root);
  }

  applySeo(page.seo, page.title);
}

// Run automatically when #home-sections exists
if (document.querySelector("#home-sections")) {
  renderMarketingPage();
}
