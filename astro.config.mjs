import { defineConfig } from 'astro/config'
import tailwind from '@astrojs/tailwind'
import { fileURLToPath } from 'node:url'

export default defineConfig({
  site: 'https://ifitwala.com',
  output: 'static',
  outDir: './dist',
  srcDir: './src',
  publicDir: './ifitwala_doc/public',
  trailingSlash: 'always',   // so folders like /docs/en/slug/ work nicely
  build: {
    assetsPrefix: '/assets/ifitwala_doc',
  },
  integrations: [tailwind({
    config: './tailwind.config.cjs',   // reuse your Tailwind config
    applyBaseStyles: false             // you already have site.css; keep Astro minimal
  })],
  vite: {
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      }
    }
  }
})
