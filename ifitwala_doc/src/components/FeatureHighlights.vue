<script setup>
import { computed } from 'vue';
import { FeatherIcon } from 'frappe-ui';

const props = defineProps({
	eyebrow: { type: String, default: '' },
	intro: { type: String, default: '' },
	items: {
		type: Array,
		default: () => []
	}
});

const sortedItems = computed(() => {
	const list = Array.isArray(props.items) ? [...props.items] : [];
	return list.sort((a, b) => (a?.order || 0) - (b?.order || 0));
});

const fallbackIcon = 'sparkles';

function iconName(icon) {
	if (typeof icon === 'string' && icon.trim()) {
		return icon.trim().toLowerCase();
	}
	return fallbackIcon;
}
</script>

<template>
	<section class="rounded-2xl border border-line bg-panel p-6 md:p-10">
		<header class="max-w-3xl">
			<p v-if="props.eyebrow" class="text-xs font-semibold uppercase tracking-[0.3em] text-primary">
				{{ props.eyebrow }}
			</p>
			<p v-if="props.intro" class="mt-4 text-lg leading-relaxed text-slate md:text-xl">
				{{ props.intro }}
			</p>
		</header>

		<div
			v-if="sortedItems.length"
			class="mt-8 grid gap-4 sm:grid-cols-2 xl:grid-cols-4"
		>
			<article
				v-for="(item, idx) in sortedItems"
				:key="item.href || item.label || idx"
				class="flex h-full flex-col gap-4 rounded-xl border border-line bg-white p-5 shadow-card transition hover:-translate-y-0.5 hover:shadow-lg"
			>
				<div class="flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10 text-primary">
					<FeatherIcon :name="iconName(item.icon)" class="h-6 w-6" />
				</div>

				<div class="space-y-2">
					<h3 class="text-base font-semibold text-ink">
						{{ item.label }}
					</h3>
					<p v-if="item.description" class="text-sm leading-relaxed text-slate">
						{{ item.description }}
					</p>
				</div>

				<a
					v-if="item.href"
					:href="item.href"
					class="mt-auto inline-flex items-center gap-1 text-sm font-semibold text-primary hover:underline"
				>
					Learn more
					<FeatherIcon name="arrow-up-right" class="h-3.5 w-3.5" />
				</a>
			</article>
		</div>

		<p v-else class="mt-6 text-sm text-slate">
			No feature highlights yet. Add items from the desk to populate this section.
		</p>
	</section>
</template>

<style scoped>
/* layout handled via utility classes */
</style>
