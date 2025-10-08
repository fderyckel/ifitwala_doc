<script setup>
import { Button } from 'frappe-ui';

const props = defineProps({
	title: { type: String, default: 'A campus where curiosity blooms.' },
	subtitle: { type: String, default: '' },
	actions: {
		type: Array,
		default: () => ([])
	}
});
</script>

<template>
	<div class="relative">
		<!-- subtle background flourish (future-proofed for animation) -->
		<div class="pointer-events-none absolute inset-0 -z-10 bg-gradient-to-b from-white to-panel"></div>

		<h1 class="max-w-3xl text-4xl font-semibold tracking-tight md:text-5xl">
			{{ props.title }}
		</h1>

		<p v-if="props.subtitle" class="mt-4 max-w-2xl text-lg text-slate">
			{{ props.subtitle }}
		</p>

		<div v-if="props.actions?.length" class="mt-8 flex flex-wrap gap-3">
			<template v-for="(a, i) in props.actions" :key="i">
				<Button
					:href="a.href"
					:label="a.label"
					class="rounded-lg px-5 py-2.5"
					:class="a.variant === 'primary'
						? 'bg-primary text-white shadow hover:opacity-95'
						: 'border border-line text-ink hover:bg-panel'"
				/>
			</template>
		</div>
	</div>
</template>

<style scoped>
/* keep it minimal; layout handled by page */
</style>
