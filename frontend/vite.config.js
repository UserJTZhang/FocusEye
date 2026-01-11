import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',  // 允许局域网访问
    port: 3000,
    strictPort: false,
    allowedHosts: [
      '6b8592772b5501.lhr.life',
      '.lhr.life',
      '.vicp.fun',
      '37vruv671229.vicp.fun'
    ],
    hmr: {
      // 禁用 WebSocket overlay，避免在隧道环境下的连接失败警告
      overlay: false
    },
    proxy: {
      '/api': {
        target: 'http://localhost:5001',
        changeOrigin: true
      }
    }
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets'
  }
})
