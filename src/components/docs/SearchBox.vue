<template>
<div class="relative">
<input v-model="q" type="search" placeholder="Search docs…" class="w-full rounded-xl border px-3 py-2 focus:outline-none focus:ring-2 focus:ring-leaf/60" @keydown.down.prevent="down" @keydown.up.prevent="up" @keydown.enter.prevent="go" />
<ul v-if="open && results.length" class="absolute z-50 mt-1 w-full bg-white border rounded-xl shadow-lg max-h-80 overflow-auto">
<li v-for="(r,i) in results" :key="r.slug" @mousedown.prevent="navigate(r.slug)" :class="['px-3 py-2 cursor-pointer', i===idx ? 'bg-moss/30' : 'hover:bg-sand/80']">
<div class="text-sm font-medium">{{ r.title }}</div>
<div class="text-xs text-slate">{{ r.path }}</div>
</li>
</ul>
</div>
</template>
<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { search } from '@/lib/search'
const q = ref('')
const idx = ref(-1)
const open = ref(false)
const results = computed(()=> q.value ? search(q.value).slice(0,8) : [])
watch(q, (v)=> open.value = !!v)
function down(){ idx.value = Math.min(idx.value+1, results.value.length-1) }
function up(){ idx.value = Math.max(idx.value-1, 0) }
function go(){ if(results.value[idx.value]) navigate(results.value[idx.value].slug) }
function navigate(slug:string){ window.location.href = `/docs/${slug}` }
</script>
