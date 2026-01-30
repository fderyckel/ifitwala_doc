// tailwind.config.cjs

/** @type {import('tailwindcss').Config} */
const path = require('path');

// Helper functions to reference CSS custom properties.
const color = (token) => `rgb(var(--${token}-rgb) / <alpha-value>)`;
const raw   = (token) => `var(${token})`;

module.exports = {
  content: [
    // Astro docs (root-level src)
    path.join(__dirname, 'src', '**/*.{astro,md,mdx,vue,js,ts,tsx}'),

    // Frappe web templates and pages
    path.join(__dirname, 'ifitwala_doc', 'ifitwala_doc', 'www', '**/*.{md,html,js}'),
    path.join(__dirname, 'ifitwala_doc', 'ifitwala_doc', 'templates', '**/*.{html,md,js}'),

    // Vue marketing components
    path.join(__dirname, 'ifitwala_doc', 'src', '**/*.{vue,js,ts}'),

    // Frappe‑UI components from node_modules
    path.join(__dirname, 'node_modules', 'frappe-ui', '**/*.{vue,js}'),
  ],

  // Classes you know Tailwind should generate even if not found in templates
  safelist: [
    'prose',
    'prose-docs',
    'max-w-3xl',
    'mx-auto',
    'px-6',
    'py-10',
    'not-prose',
  ],

  theme: {
    // Extend the default theme with custom values
    extend: {
      fontFamily: {
        serif: [
          '"Merriweather"',
          '"Source Serif Pro"',
          'Georgia',
          'serif',
        ],
      },

      // Semantic colours mapped to CSS custom properties.
      // Color palettes (blue, gray, slate, sky) are defined in CSS using @theme
      colors: {
        ink:       color('ink'),
        canopy:    color('canopy'),
        leaf:      color('leaf'),
        moss:      color('moss'),
        sand:      color('sand'),
        border:    color('border'),

        primary:   color('canopy'),
        secondary: color('leaf'),
      },

      // Custom border radii using CSS vars.
      borderRadius: {
        lg: raw('--radius-lg'),
        xl: raw('--radius-xl'),
      },

      // Custom shadows using CSS vars.
      boxShadow: {
        card:   raw('--shadow-soft'),
          soft:   raw('--shadow-soft'),
        strong: raw('--shadow-strong'),
      },

      // Define a "docs" typography variant that uses your tokens.
      typography: ({ theme }) => ({
        docs: {
          css: {
            '--tw-prose-body':         theme('colors.ink'),
            '--tw-prose-headings':     theme('colors.ink'),
            '--tw-prose-links':        theme('colors.canopy'),
            '--tw-prose-bold':         theme('colors.ink'),
            '--tw-prose-counters':     theme('colors.slate'),
            '--tw-prose-bullets':      theme('colors.slate'),
            '--tw-prose-hr':           theme('colors.border'),
            '--tw-prose-quotes':       theme('colors.ink'),
            '--tw-prose-quote-borders': theme('colors.leaf'),
            '--tw-prose-captions':     theme('colors.slate'),
            '--tw-prose-code':         theme('colors.canopy'),
            '--tw-prose-pre-bg':       theme('colors.sky'),
            '--tw-prose-th-borders':   theme('colors.border'),
            '--tw-prose-td-borders':   theme('colors.border'),

            a: { textDecoration: 'none' },
            'a:hover': { textDecoration: 'underline' },

            h1: {
              color: theme('colors.canopy'),
              fontFamily: '"Merriweather", "Source Serif Pro", "Georgia", serif',
              fontWeight: '700',
              letterSpacing: '-0.02em',
              fontSize: 'clamp(2.25rem, 3.5vw, 2.875rem)',
              marginTop: '2.5rem',
              marginBottom: '1.25rem',
              lineHeight: '1.2',
            },

            h2: {
              color: theme('colors.ink'),
              fontFamily: '"Merriweather", "Source Serif Pro", "Georgia", serif',
              fontWeight: '700',
              fontSize: 'clamp(1.75rem, 2.5vw, 2.125rem)',
              marginTop: '2.25rem',
              marginBottom: '1rem',
              lineHeight: '1.25',
            },

            h3: {
              color: theme('colors.ink'),
              fontFamily: '"Merriweather", "Source Serif Pro", "Georgia", serif',
              fontWeight: '600',
              fontSize: 'clamp(1.35rem, 2vw, 1.6rem)',
              marginTop: '1.75rem',
              marginBottom: '0.75rem',
              lineHeight: '1.3',
            },

            h4: {
              color: theme('colors.slate'),
              fontWeight: '600',
              textTransform: 'uppercase',
              letterSpacing: '0.12em',
              marginTop: '1.5rem',
              marginBottom: '0.5rem',
              fontSize: '0.875rem',
            },

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
            'thead th': {
              borderBottomColor: theme('colors.border'),
              color: theme('colors.slate'),
            },
            'tbody td': {
              borderBottomColor: theme('colors.border'),
              verticalAlign: 'top',
            },
          },
        },
      }),
    },
  },

  plugins: [
    require('@tailwindcss/typography'),
  ],
};
