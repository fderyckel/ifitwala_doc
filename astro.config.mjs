import { defineConfig } from 'astro/config';
// import tailwindcss from '@tailwindcss/vite'; // Import the v4 Vite plugin
import vue from '@astrojs/vue';
import Icons from 'unplugin-icons/vite';
import { fileURLToPath } from 'node:url';

export default defineConfig({
  site: 'https://ifitwala.com',
  output: 'static',
  outDir: './dist',
  srcDir: './src',
  publicDir: false, // Prevent copying of ifitwala_doc/public (output dir)
  trailingSlash: 'always',
  build: {
    assetsPrefix: '/assets/ifitwala_doc',
  },
  integrations: [
    // Removed @astrojs/tailwind integration to resolve PostCSS errors
    vue(),
  ],
  vite: {
    plugins: [
      // tailwindcss(), // Tailwind v4 now runs as a Vite plugin
      Icons({
        compiler: 'astro',
        autoInstall: true
      }),
    ],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url)),
      },
    },
  },
});