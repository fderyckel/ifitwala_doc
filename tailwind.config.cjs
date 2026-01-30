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
    // Define color palettes explicitly for Tailwind 4 compatibility
    colors: {
      // Explicit blue palette to fix theme(colors.blue.200) errors
      blue: {
        50: '#eff6ff',
        100: '#dbeafe',
        200: '#bfdbfe',
        300: '#93c5fd',
        400: '#60a5fa',
        500: '#3b82f6',
        600: '#2563eb',
        700: '#1d4ed8',
        800: '#1e40af',
        900: '#1e3a8a',
        950: '#172554',
      },
      gray: {
        50: '#f9fafb',
        100: '#f3f4f6',
        200: '#e5e7eb',
        300: '#d1d5db',
        400: '#9ca3af',
        500: '#6b7280',
        600: '#4b5563',
        700: '#374151',
        800: '#1f2937',
        900: '#111827',
        950: '#030712',
      },
      slate: {
        50: '#f8fafc',
        100: '#f1f5f9',
        200: '#e2e8f0',
        300: '#cbd5e1',
        400: '#94a3b8',
        500: '#64748b',
        600: '#475569',
        700: '#334155',
        800: '#1e293b',
        900: '#0f172a',
        950: '#020617',
      },
      sky: {
        50: '#f0f9ff',
        100: '#e0f2fe',
        200: '#bae6fd',
        300: '#7dd3fc',
        400: '#38bdf8',
        500: '#0ea5e9',
        600: '#0284c7',
        700: '#0369a1',
        800: '#075985',
        900: '#0c4a6e',
        950: '#082f49',
      },
    },

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
      // Use theme('colors.ink') etc. in your CSS for these.
      colors: {
        ink:       color('ink'),
        slate:     color('slate'),
        canopy:    color('canopy'),
        leaf:      color('leaf'),
        moss:      color('moss'),
        sky:       color('sky'),
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
