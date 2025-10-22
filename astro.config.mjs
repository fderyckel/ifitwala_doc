// astro.config.mjs
import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
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
  integrations: [tailwind({ config: './tailwind.config.cjs', applyBaseStyles: false })],
  vite: {
    // Add the unplugin-icons plugin here
    plugins: [
      Icons({
        compiler: 'astro',     // tells the plugin to generate Astro components
        autoInstall: true      // (optional) automatically installs missing icon sets
      }),
    ],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url)),
      },
    },
  },
});

