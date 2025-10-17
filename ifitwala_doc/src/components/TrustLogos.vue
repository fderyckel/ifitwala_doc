<script setup>
defineProps({
  title: { type: String, default: "Trusted by educators" },
  logos: { type: Array, default: () => [] } // [{src, alt, href, order}]
})
</script>

<template>
  <section class="py-12">
    <div class="mx-auto max-w-6xl px-4">
      <h2 class="text-sm tracking-widest text-gray-500 mb-6">{{ title }}</h2>
      <ul class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-6 items-center">
        <li v-for="l in logos" :key="l.order" class="flex items-center justify-center">
          <a v-if="l.href" :href="l.href" rel="noopener" target="_blank">
            <img :src="l.src" :alt="l.alt" loading="lazy" class="h-10 md:h-12 object-contain" />
          </a>
          <img v-else :src="l.src" :alt="l.alt" loading="lazy" class="h-10 md:h-12 object-contain" />
        </li>
      </ul>
    </div>
  </section>
</template>
