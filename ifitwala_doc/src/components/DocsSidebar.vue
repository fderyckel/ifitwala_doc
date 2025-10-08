<script setup>
import { FeatherIcon } from 'frappe-ui';

const props = defineProps({
	title: { type: String, default: 'Documentation' },
	items: {
		type: Array,
		default: () => ([
			{ label: 'Getting started', href: '/docs', active: true },
			{ label: 'Programs & Courses', href: '/docs/curriculum/programs' },
			{ label: 'Scheduling & Attendance', href: '/docs/scheduling/intro' }
		])
	}
});
</script>

<template>
	<aside class="top-24 hidden w-full max-w-xs shrink-0 md:sticky md:block">
		<div class="rounded-2xl border border-line bg-white p-4">
			<div class="mb-3 flex items-center gap-2">
				<FeatherIcon name="book-open" class="h-4 w-4 text-slate" />
				<h2 class="text-sm font-semibold uppercase tracking-wider text-slate">{{ props.title }}</h2>
			</div>
			<nav class="space-y-1">
				<a
					v-for="(it, idx) in props.items"
					:key="idx"
					:href="it.href"
					class="block rounded-lg px-3 py-2 text-sm"
					:class="it.active
						? 'bg-panel font-medium text-ink'
						: 'text-slate hover:bg-panel hover:text-ink'"
				>
					{{ it.label }}
				</a>
			</nav>
		</div>
	</aside>
</template>

<style scoped>
/* kept intentionally minimal */
</style>
