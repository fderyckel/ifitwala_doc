/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    // Frappe-served pages & snippets
    "ifitwala_doc/ifitwala_doc/www/**/*.{md,html,js}",
    // Vue source
    "ifitwala_doc/src/**/*.{vue,js,ts}",
    // frappe-ui components
    "node_modules/frappe-ui/**/*.{vue,js}"
  ],
  theme: {
    extend: {
      colors: {
        primary:  '#243B53', // Indigo Ink
        secondary:'#2A7F62', // Forest Jade
        accent:   '#DFAF2B', // Saffron (sparingly)
        ink:      '#1F2933', // Body text
        slate:    '#616E7C', // Muted text
        panel:    '#F8FAFC', // Card bg
        line:     '#E5E7EB'  // Dividers
      },
      borderRadius: { lg: '12px' },
      boxShadow: { card: '0 6px 24px rgba(0,0,0,0.06)' }
    }
  },
  plugins: [require('@tailwindcss/typography')]
};
