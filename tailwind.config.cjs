/** @type {import('tailwindcss').Config} */
const path = require('path');

module.exports = {
  content: [
    // 1) Frappe site assets (Jinja/HTML/inline JS/MD rendered by Frappe)
    path.join(__dirname, 'ifitwala_doc', 'ifitwala_doc', 'www', '**/*.{md,html,js}'),
    path.join(__dirname, 'ifitwala_doc', 'ifitwala_doc', 'templates', '**/*.{html,md,js}'),

    // 2) Vue code inside the app package (same level as templates/www)
    path.join(__dirname, 'ifitwala_doc', 'src', '**/*.{vue,js,ts}'),

    // 3) Astro code at repo root
    path.join(__dirname, 'src', '**/*.{astro,md,mdx,vue,js,ts,tsx}'),

    // 4) frappe-ui components
    path.join(__dirname, 'node_modules', 'frappe-ui', '**/*.{vue,js}'),
  ],
  safelist: [
    'prose', 'prose-docs', 'max-w-3xl', 'mx-auto', 'px-6', 'py-10',
  ],
  theme: {
    extend: {
      colors: {
        primary:  '#243B53',
        secondary:'#2A7F62',
        accent:   '#DFAF2B',
        ink:      '#1F2933',
        slate:    '#616E7C',
        panel:    '#F8FAFC',
        line:     '#E5E7EB'
      },
      borderRadius: { lg: '12px' },
      boxShadow: { card: '0 6px 24px rgba(0,0,0,0.06)' },
      typography: ({ theme }) => ({
        // use as: class="prose prose-docs"
        docs: {
          css: {
            '--tw-prose-body': theme('colors.ink'),
            '--tw-prose-headings': theme('colors.primary'),
            '--tw-prose-links': theme('colors.primary'),
            '--tw-prose-bold': theme('colors.ink'),
            '--tw-prose-counters': theme('colors.slate'),
            '--tw-prose-bullets': theme('colors.slate'),
            '--tw-prose-hr': theme('colors.line'),
            '--tw-prose-quotes': theme('colors.ink'),
            '--tw-prose-quote-borders': theme('colors.line'),
            '--tw-prose-captions': theme('colors.slate'),
            '--tw-prose-code': theme('colors.primary'),
            '--tw-prose-pre-bg': theme('colors.panel'),
            '--tw-prose-th-borders': theme('colors.line'),
            '--tw-prose-td-borders': theme('colors.line'),
            a: { textDecoration: 'none' },
            'a:hover': { textDecoration: 'underline' },
            h1: { color: theme('colors.primary') },
            h2: { color: theme('colors.primary') },
            h3: { color: theme('colors.primary') },
            code: { fontWeight: '600' },
            pre: { borderRadius: theme('borderRadius.lg') },
            blockquote: { borderLeftColor: theme('colors.secondary') },
          },
        },
      }),
    },
  },
  plugins: [require('@tailwindcss/typography')],
};
