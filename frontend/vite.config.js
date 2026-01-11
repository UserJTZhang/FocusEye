import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',  // 允许局域网访问
    port: 3000,
    strictPort: false,
    allowedHosts: [
      '6b8592772b5501.lhr.life',  // 添加您的特定主机
      '.lhr.life',  // 或允许所有 lhr.life 子域名
      '.vicp.fun',  // 或允许所有 lhr.life 子域名
      '37vruv671229.vicp.fun'  // 或允许所有 lhr.life 子域名
    ],
    hmr: {
      clientPort: 3000
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
