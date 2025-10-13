// tailwind.config.cjs
const path = require('path');

const v = (name) => `var(${name})`;

module.exports = {
  content: [
    path.join(__dirname, 'ifitwala_doc', 'ifitwala_doc', 'www', '**/*.{md,html,js}'),
    path.join(__dirname, 'ifitwala_doc', 'ifitwala_doc', 'templates', '**/*.{html,md,js}'),
    path.join(__dirname, 'ifitwala_doc', 'src', '**/*.{vue,js,ts}'),
    path.join(__dirname, 'src', '**/*.{astro,md,mdx,vue,js,ts,tsx}'),
    path.join(__dirname, 'node_modules', 'frappe-ui', '**/*.{vue,js}'),
  ],
  safelist: ['prose','prose-docs','max-w-3xl','mx-auto','px-6','py-10','not-prose'],
  theme: {
    extend: {
      colors: {
        // map design tokens → semantic names
        primary:  v('--brand-500'),
        secondary:v('--brand-700'),
        accent:   v('--accent-500'),
        ink:      v('--neutral-900'),
        slate:    v('--neutral-500'),
        panel:    v('--neutral-50'),
        line:     v('--neutral-200'),

        // (optional) expose full brand & neutral scales
        brand: {
          50: v('--brand-50'), 100: v('--brand-100'), 200: v('--brand-200'),
          300: v('--brand-300'), 400: v('--brand-400'), 500: v('--brand-500'),
          600: v('--brand-600'), 700: v('--brand-700'), 800: v('--brand-800'), 900: v('--brand-900'),
        },
        neutral: {
          50: v('--neutral-50'), 100: v('--neutral-100'), 200: v('--neutral-200'),
          300: v('--neutral-300'), 400: v('--neutral-400'), 500: v('--neutral-500'),
          600: v('--neutral-600'), 700: v('--neutral-700'), 800: v('--neutral-800'), 900: v('--neutral-900'),
        },
        success: v('--success-500'),
        info:    v('--info-500'),
        warning: v('--warning-500'),
        danger:  v('--danger-500'),
      },
      borderRadius: { lg: '12px' },
      boxShadow: { card: '0 6px 24px rgba(0,0,0,0.06)' },
      typography: ({ theme }) => ({
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
            '--tw-prose-quote-borders': theme('colors.secondary'),
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

            figure: { margin: '1.25rem 0' },
            'figure img': {
              borderRadius: theme('borderRadius.lg'),
              boxShadow: '0 1px 2px rgba(0,0,0,.05)',
            },
            figcaption: {
              fontSize: '0.875rem',
              color: theme('colors.slate'),
              marginTop: '0.5rem',
            },
            blockquote: { borderLeftColor: theme('colors.secondary') },
            'thead th': { borderBottomColor: theme('colors.line'), color: theme('colors.slate') },
            'tbody td': { borderBottomColor: theme('colors.line'), verticalAlign: 'top' },
          },
        },
      }),
    },
  },
  plugins: [require('@tailwindcss/typography')],
};
