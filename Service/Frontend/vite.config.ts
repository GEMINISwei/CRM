import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',
    port: 8000,
    watch: {
      usePolling: true,
    }
  },
  resolve: {
    alias: {
      '@': path.join(__dirname, 'src'),
    },
  },
})
