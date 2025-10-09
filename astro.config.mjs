import { defineConfig } from 'astro/config'
import tailwind from '@astrojs/tailwind'

export default defineConfig({
  output: 'static',
  outDir: './dist',
  trailingSlash: 'always',   // so folders like /docs/en/slug/ work nicely
  integrations: [tailwind({
    config: './tailwind.config.cjs',   // reuse your Tailwind config
    applyBaseStyles: false             // you already have site.css; keep Astro minimal
  })],
})
