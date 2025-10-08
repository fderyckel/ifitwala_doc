import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import Icons from 'unplugin-icons/vite';
import IconsResolver from 'unplugin-icons/resolver';
import path from 'node:path';

export default defineConfig({
	root: process.cwd(),
	plugins: [
		vue(),
		Icons({
			autoInstall: true,
			compiler: 'vue3'
		})
	],
	build: {
		outDir: path.resolve(__dirname, 'ifitwala_doc/ifitwala_doc/public/dist'),
		emptyOutDir: false, // keep any existing assets in dist
		sourcemap: false,
		minify: 'esbuild',
		cssCodeSplit: true,
		rollupOptions: {
			// We treat Tailwind CSS as its own entry so it becomes a stable file: site.css
			input: {
				base: path.resolve(__dirname, 'ifitwala_doc/src/main.js'),
				site: path.resolve(__dirname, 'ifitwala_doc/src/styles/tailwind.css')
			},
			output: {
				// Fixed names (no hashes) so you can reference them easily from Jinja
				entryFileNames: '[name].js',
				chunkFileNames: 'chunks/[name].js',
				assetFileNames: (assetInfo) => {
					if (assetInfo.name && assetInfo.name.endsWith('.css')) {
						return '[name][extname]'; // -> site.css
					}
					return 'assets/[name][extname]';
				}
			}
		}
	},
	resolve: {
		alias: {
			'@': path.resolve(__dirname, 'ifitwala_doc/src')
		}
	}
});
