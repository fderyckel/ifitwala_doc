// tailwind.config.cjs
const path = require('path');

const color = (token) => `rgb(var(--${token}-rgb) / <alpha-value>)`;
const raw = (token) => `var(${token})`;

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
        // semantic aliases
        ink:      color('ink'),
        slate:    color('slate'),
        canopy:   color('canopy'),
        leaf:     color('leaf'),
        moss:     color('moss'),
        sky:      color('sky'),
        sand:     color('sand'),
        border:   color('border'),

        primary:  color('canopy'),
        secondary:color('leaf'),
      },
      borderRadius: {
        lg: raw('--radius-lg'),
        xl: raw('--radius-xl'),
      },
      boxShadow: {
        card: raw('--shadow-soft'),
        soft: raw('--shadow-soft'),
        strong: raw('--shadow-strong'),
      },
      typography: ({ theme }) => ({
        docs: {
          css: {
            '--tw-prose-body': theme('colors.ink'),
            '--tw-prose-headings': theme('colors.ink'),
            '--tw-prose-links': theme('colors.canopy'),
            '--tw-prose-bold': theme('colors.ink'),
            '--tw-prose-counters': theme('colors.slate'),
            '--tw-prose-bullets': theme('colors.slate'),
            '--tw-prose-hr': theme('colors.border'),
            '--tw-prose-quotes': theme('colors.ink'),
            '--tw-prose-quote-borders': theme('colors.leaf'),
            '--tw-prose-captions': theme('colors.slate'),
            '--tw-prose-code': theme('colors.canopy'),
            '--tw-prose-pre-bg': theme('colors.sky'),
            '--tw-prose-th-borders': theme('colors.border'),
            '--tw-prose-td-borders': theme('colors.border'),

            a: { textDecoration: 'none' },
            'a:hover': { textDecoration: 'underline' },
            h1: { color: theme('colors.ink') },
            h2: { color: theme('colors.ink') },
            h3: { color: theme('colors.ink') },

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
            blockquote: { borderLeftColor: theme('colors.leaf') },
            'thead th': { borderBottomColor: theme('colors.border'), color: theme('colors.slate') },
            'tbody td': { borderBottomColor: theme('colors.border'), verticalAlign: 'top' },
          },
        },
      }),
    },
  },
  plugins: [require('@tailwindcss/typography')],
};
