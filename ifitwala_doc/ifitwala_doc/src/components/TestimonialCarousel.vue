<script setup>
const props = defineProps({
	title: { type: String, default: 'What educators are saying' },
	testimonials: {
		type: Array,
		default: () => ([
			{
				quote: 'Ifitwala Ed helped us streamline schedules and guardian communication in a single week.',
				name: 'Amelia Brooks',
				role: 'Principal, Northview School'
			},
			{
				quote: 'Our teachers can focus on students instead of wrestling with fragmented systems.',
				name: 'Rashid Chowdhury',
				role: 'Director of Studies, Horizon College'
			},
			{
				quote: 'The rollout was the calmest software launch our team has experienced.',
				name: 'Clara Sola',
				role: 'Operations Lead, Bright River Academy'
			}
		])
	}
});
</script>

<template>
	<section class="rounded-2xl border border-line bg-panel p-6 md:p-10">
		<div class="flex flex-col gap-6 md:flex-row md:items-start md:justify-between">
			<div class="max-w-sm">
				<p class="text-xs font-semibold uppercase tracking-wider text-slate">
					{{ props.title }}
				</p>
				<p class="mt-3 text-sm text-slate">
					These are placeholder stories. Replace them with voices from your schools to make the carousel shine.
				</p>
			</div>

			<div class="grid flex-1 gap-6 md:grid-cols-3">
				<article
					v-for="(item, idx) in props.testimonials"
					:key="idx"
					class="flex h-full flex-col justify-between rounded-xl bg-white p-5 shadow-card"
				>
					<p class="text-base font-medium text-ink">
						“{{ item.quote }}”
					</p>
					<div class="mt-4 text-sm text-slate">
						<p class="font-semibold text-ink">{{ item.name }}</p>
						<p class="mt-1 leading-snug">{{ item.role }}</p>
					</div>
				</article>
			</div>
		</div>
	</section>
</template>

<style scoped>
/* carousel behavior can be added later; current layout is responsive grid */
</style>
