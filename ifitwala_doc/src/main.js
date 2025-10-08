import { createApp } from 'vue';
import { FrappeUI } from 'frappe-ui';


/**
 * Register your Vue islands here.
 * Each entry is lazy-loaded, so routes only download what they need.
 */
const registry = {
	Hero: () => import('@/components/Hero.vue'),
	TestimonialCarousel: () => import('@/components/TestimonialCarousel.vue'),
	DocToc: () => import('@/components/DocToc.vue'),
	DocsSidebar: () => import('@/components/DocsSidebar.vue')
};

function parseProps(el) {
	const raw = el.getAttribute('data-props');
	if (!raw) return {};
	try {
		return JSON.parse(raw);
	} catch (e) {
		console.warn('[ifitwala_doc] Invalid JSON in data-props:', e);
		return {};
	}
}

document.querySelectorAll('[data-vue]').forEach(async (el) => {
	const name = el.getAttribute('data-vue');
	const loader = registry[name];
	if (!loader) {
		console.warn(`[ifitwala_doc] No component registered for "${name}"`);
		return;
	}
	const mod = await loader();
	const Comp = mod.default || mod;
	const props = parseProps(el);

	const app = createApp(Comp, props);
	app.use(FrappeUI);
	app.mount(el);
});
