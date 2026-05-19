<script setup>
import { computed, ref } from 'vue';

const props = defineProps({
  mode: { type: String, default: 'company' },
  source: { type: String, default: 'Website' },
  title: { type: String, default: '' },
  subtitle: { type: String, default: '' },
  submitLabel: { type: String, default: '' },
});

const isProductDemo = computed(() => props.mode === 'ifitwala-ed');

const resolvedTitle = computed(() =>
  props.title || (isProductDemo.value ? 'Book a Demo' : 'Book a Call')
);
const resolvedSubtitle = computed(() =>
  props.subtitle ||
  (isProductDemo.value
    ? 'Tell us about your school and what you want to see.'
    : 'Tell us what system, workflow, or data problem you want to discuss.')
);
const resolvedSubmitLabel = computed(() =>
  props.submitLabel || (isProductDemo.value ? 'Book Demo' : 'Send Inquiry')
);

const interestOptions = [
  'ERP implementation',
  'Ifitwala Ed',
  'Data governance / privacy',
  'Education systems',
  'Not sure yet',
];

const organizationTypes = [
  'Company',
  'School',
  'Education group',
  'Training organization',
  'NGO',
  'Other',
];

const emptyForm = () => ({
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
  organization: '',
  organization_type: isProductDemo.value ? 'School' : '',
  job_title: '',
  interest_area: isProductDemo.value ? 'Ifitwala Ed' : '',
  current_system: '',
  message: '',
});

const form = ref(emptyForm());
const loading = ref(false);
const success = ref(false);
const error = ref(null);

const buildNotes = () => {
  const lines = [];
  if (form.value.interest_area) lines.push(`Interest: ${form.value.interest_area}`);
  if (form.value.organization_type) lines.push(`Organization type: ${form.value.organization_type}`);
  if (form.value.current_system) lines.push(`Current system: ${form.value.current_system}`);
  if (form.value.message) lines.push(`Message: ${form.value.message}`);
  return lines.join('\n');
};

const submitForm = async () => {
  loading.value = true;
  error.value = null;

  try {
    const response = await fetch('/api/method/ifitwala_doc.crm.api.capture_lead', {
      method: 'POST',
      credentials: 'omit',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        ...form.value,
        school_name: isProductDemo.value ? form.value.organization : '',
        source: props.source,
        notes: buildNotes(),
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.message || data.exception || 'Something went wrong');
    }

    success.value = true;
    form.value = emptyForm();
  } catch (err) {
    console.error(err);
    error.value = 'Failed to submit. Please try again or email us directly.';
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="rounded-lg border border-line bg-white p-6 shadow-card md:p-8">
    <div v-if="success" class="flex flex-col items-center justify-center py-10 text-center">
      <div class="mb-4 flex h-14 w-14 items-center justify-center rounded-md bg-green-100 text-green-700">
        <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <polyline points="20 6 9 17 4 12"></polyline>
        </svg>
      </div>
      <h3 class="text-2xl font-bold text-ink">Thank you</h3>
      <p class="mt-2 text-slate">We have received your inquiry and will be in touch shortly.</p>
      <button @click="success = false" class="mt-6 text-sm font-semibold text-canopy hover:underline">
        Send another message
      </button>
    </div>

    <form v-else @submit.prevent="submitForm" class="space-y-5">
      <div class="text-center">
        <h3 class="text-xl font-bold text-ink">{{ resolvedTitle }}</h3>
        <p class="mt-1 text-sm text-slate">{{ resolvedSubtitle }}</p>
      </div>

      <div class="grid gap-4 md:grid-cols-2">
        <div>
          <label class="mb-1 block text-xs font-semibold uppercase text-slate">First name</label>
          <input
            v-model="form.first_name"
            type="text"
            required
            class="w-full rounded-md border border-border bg-transparent px-3 py-2 text-sm text-ink placeholder-slate/50 focus:border-leaf focus:outline-none focus:ring-1 focus:ring-leaf"
            placeholder="Jane"
          />
        </div>
        <div>
          <label class="mb-1 block text-xs font-semibold uppercase text-slate">Last name</label>
          <input
            v-model="form.last_name"
            type="text"
            class="w-full rounded-md border border-border bg-transparent px-3 py-2 text-sm text-ink placeholder-slate/50 focus:border-leaf focus:outline-none focus:ring-1 focus:ring-leaf"
            placeholder="Doe"
          />
        </div>
      </div>

      <div>
        <label class="mb-1 block text-xs font-semibold uppercase text-slate">Work email</label>
        <input
          v-model="form.email"
          type="email"
          required
          class="w-full rounded-md border border-border bg-transparent px-3 py-2 text-sm text-ink placeholder-slate/50 focus:border-leaf focus:outline-none focus:ring-1 focus:ring-leaf"
          placeholder="jane@example.org"
        />
      </div>

      <div class="grid gap-4 md:grid-cols-2">
        <div>
          <label class="mb-1 block text-xs font-semibold uppercase text-slate">
            {{ isProductDemo ? 'School name' : 'Organization' }}
          </label>
          <input
            v-model="form.organization"
            type="text"
            required
            class="w-full rounded-md border border-border bg-transparent px-3 py-2 text-sm text-ink placeholder-slate/50 focus:border-leaf focus:outline-none focus:ring-1 focus:ring-leaf"
            :placeholder="isProductDemo ? 'Sunrise Academy' : 'Organization name'"
          />
        </div>
        <div>
          <label class="mb-1 block text-xs font-semibold uppercase text-slate">Role</label>
          <input
            v-model="form.job_title"
            type="text"
            class="w-full rounded-md border border-border bg-transparent px-3 py-2 text-sm text-ink placeholder-slate/50 focus:border-leaf focus:outline-none focus:ring-1 focus:ring-leaf"
            :placeholder="isProductDemo ? 'Principal' : 'Operations lead'"
          />
        </div>
      </div>

      <div class="grid gap-4 md:grid-cols-2">
        <div>
          <label class="mb-1 block text-xs font-semibold uppercase text-slate">Organization type</label>
          <select
            v-model="form.organization_type"
            class="w-full rounded-md border border-border bg-white px-3 py-2 text-sm text-ink focus:border-leaf focus:outline-none focus:ring-1 focus:ring-leaf"
          >
            <option value="">Select one</option>
            <option v-for="option in organizationTypes" :key="option" :value="option">{{ option }}</option>
          </select>
        </div>
        <div>
          <label class="mb-1 block text-xs font-semibold uppercase text-slate">What do you need help with?</label>
          <select
            v-model="form.interest_area"
            class="w-full rounded-md border border-border bg-white px-3 py-2 text-sm text-ink focus:border-leaf focus:outline-none focus:ring-1 focus:ring-leaf"
          >
            <option value="">Select one</option>
            <option v-for="option in interestOptions" :key="option" :value="option">{{ option }}</option>
          </select>
        </div>
      </div>

      <div class="grid gap-4 md:grid-cols-2">
        <div>
          <label class="mb-1 block text-xs font-semibold uppercase text-slate">Current system</label>
          <input
            v-model="form.current_system"
            type="text"
            class="w-full rounded-md border border-border bg-transparent px-3 py-2 text-sm text-ink placeholder-slate/50 focus:border-leaf focus:outline-none focus:ring-1 focus:ring-leaf"
            placeholder="Odoo, ERPNext, Moodle, spreadsheets..."
          />
        </div>
        <div>
          <label class="mb-1 block text-xs font-semibold uppercase text-slate">Phone optional</label>
          <input
            v-model="form.phone"
            type="tel"
            class="w-full rounded-md border border-border bg-transparent px-3 py-2 text-sm text-ink placeholder-slate/50 focus:border-leaf focus:outline-none focus:ring-1 focus:ring-leaf"
            placeholder="+1 555 000 0000"
          />
        </div>
      </div>

      <div>
        <label class="mb-1 block text-xs font-semibold uppercase text-slate">Message</label>
        <textarea
          v-model="form.message"
          rows="4"
          class="w-full rounded-md border border-border bg-transparent px-3 py-2 text-sm text-ink placeholder-slate/50 focus:border-leaf focus:outline-none focus:ring-1 focus:ring-leaf"
          placeholder="Tell us what you are trying to improve..."
        ></textarea>
      </div>

      <div v-if="error" class="rounded-md border border-red-100 bg-red-50 p-3 text-sm text-red-600">
        {{ error }}
      </div>

      <button
        type="submit"
        :disabled="loading"
        class="w-full rounded-md bg-canopy py-3 text-sm font-bold text-white shadow-md transition hover:bg-canopy/90 hover:shadow-lg disabled:cursor-not-allowed disabled:opacity-50"
      >
        <span v-if="loading">Sending...</span>
        <span v-else>{{ resolvedSubmitLabel }}</span>
      </button>

      <p class="text-center text-xs text-slate">
        We respect your privacy. No spam.
      </p>
    </form>
  </div>
</template>
