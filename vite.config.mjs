import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import path from 'node:path';
import Icons from 'unplugin-icons/vite';

export default defineConfig({
  base: '/assets/ifitwala_doc/dist/',
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
    // Correctly points to the Frappe public asset directory
    outDir: path.resolve(__dirname, 'ifitwala_doc/public/dist'),
    emptyOutDir: false,
    sourcemap: false,
    minify: 'esbuild',
    cssCodeSplit: true,
    rollupOptions: {
      input: {
        // Dual entry points for the Marketing pipeline
        base: path.resolve(__dirname, 'ifitwala_doc/src/main.js'),
        site: path.resolve(__dirname, 'ifitwala_doc/src/styles/tailwind.css')
      },
      output: {
        entryFileNames: '[name].js',
        chunkFileNames: 'chunks/[name].js',
        assetFileNames: (assetInfo) => {
          // Ensures clean naming for site.css in the final Frappe assets folder
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
      // Internal alias for the Marketing source folder
      '@': path.resolve(__dirname, 'ifitwala_doc/src')
    }
  }
});