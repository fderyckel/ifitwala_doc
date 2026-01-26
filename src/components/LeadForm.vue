<script setup>
import { ref } from 'vue';

const props = defineProps({
  source: { type: String, default: 'Website' },
  title: { type: String, default: 'Book a Demo' },
  subtitle: { type: String, default: 'See how Ifitwala Ed can transform your school.' }
});

const form = ref({
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
  school_name: '',
  job_title: '',
  message: ''
});

const loading = ref(false);
const success = ref(false);
const error = ref(null);

const submitForm = async () => {
  loading.value = true;
  error.value = null;
  
  try {
    const response = await fetch('/api/method/ifitwala_doc.crm.api.capture_lead', {
      method: 'POST',
      credentials: 'omit', // Bypass CSRF check by not sending cookies (public form)
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        ...form.value,
        source: props.source,
        notes: form.value.message // Map message to notes
      })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.message || data.exception || 'Something went wrong');
    }

    success.value = true;
    form.value = { first_name: '', last_name: '', email: '', phone: '', school_name: '', job_title: '', message: '' }; // Reset
  } catch (err) {
    console.error(err);
    error.value = "Failed to submit. Please try again or email us directly.";
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="rounded-2xl border border-line bg-white p-6 md:p-10 shadow-card">
    <div v-if="success" class="flex flex-col items-center justify-center text-center py-10">
      <div class="h-16 w-16 rounded-full bg-green-100 flex items-center justify-center text-green-600 mb-4">
        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
      </div>
      <h3 class="text-2xl font-bold text-ink">Thank You!</h3>
      <p class="mt-2 text-slate">We've received your inquiry and will be in touch shortly.</p>
      <button @click="success = false" class="mt-6 text-sm font-semibold text-canopy hover:underline">
        Send another message
      </button>
    </div>

    <form v-else @submit.prevent="submitForm" class="space-y-5">
      <div class="text-center mb-6">
        <h3 class="text-xl font-bold text-ink">{{ title }}</h3>
        <p class="text-sm text-slate mt-1">{{ subtitle }}</p>
      </div>

      <div class="grid md:grid-cols-2 gap-4">
        <div>
          <label class="block text-xs font-semibold uppercase text-slate mb-1">First Name</label>
          <input 
            v-model="form.first_name" 
            type="text" 
            required
            class="w-full rounded-md border border-border bg-transparent px-3 py-2 text-sm text-ink placeholder-slate/50 focus:border-leaf focus:outline-none focus:ring-1 focus:ring-leaf"
            placeholder="Jane"
          />
        </div>
        <div>
          <label class="block text-xs font-semibold uppercase text-slate mb-1">Last Name</label>
          <input 
            v-model="form.last_name" 
            type="text" 
            class="w-full rounded-md border border-border bg-transparent px-3 py-2 text-sm text-ink placeholder-slate/50 focus:border-leaf focus:outline-none focus:ring-1 focus:ring-leaf"
            placeholder="Doe"
          />
        </div>
      </div>

      <div>
        <label class="block text-xs font-semibold uppercase text-slate mb-1">Work Email</label>
        <input 
          v-model="form.email" 
          type="email" 
          required
          class="w-full rounded-md border border-border bg-transparent px-3 py-2 text-sm text-ink placeholder-slate/50 focus:border-leaf focus:outline-none focus:ring-1 focus:ring-leaf"
          placeholder="jane@school.edu"
        />
      </div>

      <div class="grid md:grid-cols-2 gap-4">
        <div>
          <label class="block text-xs font-semibold uppercase text-slate mb-1">School Name</label>
          <input 
            v-model="form.school_name" 
            type="text" 
            class="w-full rounded-md border border-border bg-transparent px-3 py-2 text-sm text-ink placeholder-slate/50 focus:border-leaf focus:outline-none focus:ring-1 focus:ring-leaf"
            placeholder="Sunrise Academy"
          />
        </div>
        <div>
          <label class="block text-xs font-semibold uppercase text-slate mb-1">Job Title</label>
          <input 
            v-model="form.job_title" 
            type="text" 
            class="w-full rounded-md border border-border bg-transparent px-3 py-2 text-sm text-ink placeholder-slate/50 focus:border-leaf focus:outline-none focus:ring-1 focus:ring-leaf"
            placeholder="Principal"
          />
        </div>
      </div>

      <div>
        <label class="block text-xs font-semibold uppercase text-slate mb-1">Phone (Optional)</label>
        <input 
          v-model="form.phone" 
          type="tel" 
          class="w-full rounded-md border border-border bg-transparent px-3 py-2 text-sm text-ink placeholder-slate/50 focus:border-leaf focus:outline-none focus:ring-1 focus:ring-leaf"
          placeholder="+1 (555) 000-0000"
        />
      </div>
      
      <div>
        <label class="block text-xs font-semibold uppercase text-slate mb-1">Anything else?</label>
        <textarea 
          v-model="form.message" 
          rows="3"
          class="w-full rounded-md border border-border bg-transparent px-3 py-2 text-sm text-ink placeholder-slate/50 focus:border-leaf focus:outline-none focus:ring-1 focus:ring-leaf"
          placeholder="Tell us about your needs..."
        ></textarea>
      </div>

      <div v-if="error" class="text-sm text-red-600 bg-red-50 p-2 rounded border border-red-100">
        {{ error }}
      </div>

      <button 
        type="submit" 
        :disabled="loading"
        class="w-full rounded-full bg-canopy py-3 text-sm font-bold text-white shadow-md transition hover:bg-canopy/90 hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <span v-if="loading">Sending...</span>
        <span v-else>Book Demo</span>
      </button>
      
      <p class="text-xs text-center text-slate">
        We respect your privacy. No spam, ever.
      </p>
    </form>
  </div>
</template>
