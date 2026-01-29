import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import vue from '@astrojs/vue';
import Icons from 'unplugin-icons/vite';
import { fileURLToPath } from 'node:url';

export default defineConfig({
  site: 'https://ifitwala.com',
  output: 'static',
  outDir: './dist',
  srcDir: './src',
  publicDir: './ifitwala_doc/public',
  trailingSlash: 'always',
  build: {
    assetsPrefix: '/assets/ifitwala_doc',
  },
  integrations: [
    // Update: Remove the 'config' path. Tailwind v4/PostCSS will find it automatically.
    tailwind({ applyBaseStyles: false }), 
    vue(),
  ],
  vite: {
    plugins: [
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