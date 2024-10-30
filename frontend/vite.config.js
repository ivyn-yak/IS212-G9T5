import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [
    react({
      jsxImportSource: '@emotion/react',
      babel: {
        plugins: ['@emotion/babel-plugin'],
      },
    }),
  ],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:5001',  // Forward to the Flask backend
        changeOrigin: true,               // Change the origin of the host header to the target URL
        // No rewrite, keep the /api prefix in the request
      },
    },
  },
})


