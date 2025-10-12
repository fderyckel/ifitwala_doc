/** @type {import('tailwindcss').Config} */
const path = require('path');

module.exports = {
  content: [
    path.join(__dirname, 'ifitwala_doc', 'ifitwala_doc', 'www', '**/*.{md,html,js}'),
    path.join(__dirname, 'ifitwala_doc', 'ifitwala_doc', 'templates', '**/*.{html,md,js}'),
    path.join(__dirname, 'ifitwala_doc', 'src', '**/*.{vue,js,ts}'),
    path.join(__dirname, 'src', '**/*.{astro,md,mdx,vue,js,ts,tsx}'),
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
            /* tokens */
            '--tw-prose-body': theme('colors.ink'),
            '--tw-prose-headings': theme('colors.primary'),
            '--tw-prose-links': theme('colors.primary'),
            '--tw-prose-bold': theme('colors.ink'),
            '--tw-prose-counters': theme('colors.slate'),
            '--tw-prose-bullets': theme('colors.slate'),
            '--tw-prose-hr': theme('colors.line'),
            '--tw-prose-quotes': theme('colors.ink'),
            '--tw-prose-quote-borders': theme('colors.secondary'),
            '--tw-prose-captions': theme('colors.slate'),
            '--tw-prose-code': theme('colors.primary'),
            '--tw-prose-pre-bg': theme('colors.panel'),
            '--tw-prose-th-borders': theme('colors.line'),
            '--tw-prose-td-borders': theme('colors.line'),

            /* headings & links */
            a: { textDecoration: 'none' },
            'a:hover': { textDecoration: 'underline' },
            h1: { color: theme('colors.primary') },
            h2: { color: theme('colors.primary') },
            h3: { color: theme('colors.primary') },

            /* code */
            code: { fontWeight: '600' },
            pre: { borderRadius: theme('borderRadius.lg') },

            /* figures (screenshots) */
            figure: { margin: '1.25rem 0' },
            'figure img': {
              borderRadius: theme('borderRadius.lg'),
              boxShadow: theme('boxShadow.sm', '0 1px 2px rgba(0,0,0,.05)'),
            },
            figcaption: {
              fontSize: theme('fontSize.sm')[0],
              color: theme('colors.slate'),
              marginTop: '0.5rem',
            },

            /* blockquotes */
            blockquote: { borderLeftColor: theme('colors.secondary') },

            /* tables */
            'thead th': {
              borderBottomColor: theme('colors.line'),
              color: theme('colors.slate'),
            },
            'tbody td': {
              borderBottomColor: theme('colors.line'),
              verticalAlign: 'top',
            },
          },
        },
      }),
    },
  },
  plugins: [require('@tailwindcss/typography')],
};
