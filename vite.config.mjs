import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import path from 'node:path';
import Icons from 'unplugin-icons/vite';

export default defineConfig({
	plugins: [
		vue(),
		Icons({
			autoInstall: true,
			compiler: 'vue3'
		})
	],
	optimizeDeps: {
		include: ['vue-router']
	},
	build: {
		outDir: path.resolve(__dirname, 'ifitwala_doc/public/dist'),
		emptyOutDir: false,
		sourcemap: false,
		minify: 'esbuild',
		cssCodeSplit: true,
		rollupOptions: {
			input: {
				base: path.resolve(__dirname, 'ifitwala_doc/src/main.js'),
				site: path.resolve(__dirname, 'ifitwala_doc/src/styles/tailwind.css')
			},
			output: {
				entryFileNames: '[name].js',
				chunkFileNames: 'chunks/[name].js',
				assetFileNames: (assetInfo) => {
					if (assetInfo.name && assetInfo.name.endsWith('.css')) {
						return '[name][extname]';
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
