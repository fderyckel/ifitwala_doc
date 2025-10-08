<script setup>
const props = defineProps({
	title: { type: String, default: 'On this page' },
	items: {
		type: Array,
		default: () => ([])
	}
});
</script>

<template>
	<nav class="top-24 hidden max-w-xs shrink-0 md:sticky md:block">
		<div class="rounded-2xl border border-line bg-white p-4">
			<h2 class="text-xs font-semibold uppercase tracking-wider text-slate">
				{{ props.title }}
			</h2>
			<ul class="mt-4 space-y-2 text-sm">
				<li
					v-for="(item, idx) in props.items"
					:key="idx"
					class="leading-snug text-slate hover:text-ink"
				>
					<a :href="item.href">
						{{ item.label }}
					</a>
				</li>
			</ul>
			<p v-if="!props.items?.length" class="text-xs text-slate">
				Add headings with `data-toc` to populate this list.
			</p>
		</div>
	</nav>
</template>

<style scoped>
/* minimal styling; inherits layout from surrounding page */
</style>
