/** @type {import('tailwindcss').Config} */
module.exports = {
	content: [
		'./ifitwala_doc/ifitwala_doc/www/**/*.{md,html,js}',
		'./ifitwala_doc/ifitwala_doc/templates/**/*.{html,md,js}',
		'./ifitwala_doc/src/**/*.{vue,js,ts}',
		'./node_modules/frappe-ui/**/*.{vue,js}'
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
			boxShadow: { card: '0 6px 24px rgba(0,0,0,0.06)' }
		}
	},
	plugins: [require('@tailwindcss/typography')]
};
