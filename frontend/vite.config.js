import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  esbuild: {
    loader: 'jsx',
    include: /src\/.*\.[jt]sx?$/,
    exclude: []
  },
  optimizeDeps: {
    esbuildOptions: {
      loader: {
        '.js': 'jsx',
      },
    },
  },
  server: {
    host: '0.0.0.0',
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://backend:8000',
        changeOrigin: true,
        secure: false,
        configure: (proxy, options) => {
          proxy.on('error', (err, req, res) => {
            console.log('🔴 Proxy error:', err);
          });
          proxy.on('proxyReq', (proxyReq, req, res) => {
            console.log('🟡 Proxy request:', req.method, req.url, '→', proxyReq.path);
          });
          proxy.on('proxyRes', (proxyRes, req, res) => {
            console.log('🟢 Proxy response:', proxyRes.statusCode, req.url);
          });
        },
        rewrite: (path) => {
          const newPath = path.replace(/^\/api/, '');
          console.log(`🔄 Rewriting ${path} → ${newPath}`);
          return newPath;
        }
      },
      '/auth': {
        target: 'http://backend:8000',
        changeOrigin: true,
        secure: false,
        configure: (proxy, options) => {
          proxy.on('error', (err, req, res) => {
            console.log('🔴 Auth proxy error:', err);
          });
          proxy.on('proxyReq', (proxyReq, req, res) => {
            console.log('🟡 Auth proxy request:', req.method, req.url, '→', proxyReq.path);
          });
          proxy.on('proxyRes', (proxyRes, req, res) => {
            console.log('🟢 Auth proxy response:', proxyRes.statusCode, req.url);
          });
        }
      },
      '/admin': {
        target: 'http://backend:8000',
        changeOrigin: true,
        secure: false,
        configure: (proxy, options) => {
          proxy.on('error', (err, req, res) => {
            console.log('🔴 Admin proxy error:', err);
          });
          proxy.on('proxyReq', (proxyReq, req, res) => {
            console.log('🟡 Admin proxy request:', req.method, req.url, '→', proxyReq.path);
          });
          proxy.on('proxyRes', (proxyRes, req, res) => {
            console.log('🟢 Admin proxy response:', proxyRes.statusCode, req.url);
          });
        }
      },
      '/user': {
        target: 'http://backend:8000',
        changeOrigin: true,
        secure: false,
        configure: (proxy, options) => {
          proxy.on('error', (err, req, res) => {
            console.log('🔴 User proxy error:', err);
          });
          proxy.on('proxyReq', (proxyReq, req, res) => {
            console.log('🟡 User proxy request:', req.method, req.url, '→', proxyReq.path);
          });
          proxy.on('proxyRes', (proxyRes, req, res) => {
            console.log('🟢 User proxy response:', proxyRes.statusCode, req.url);
          });
        }
      }
    }
  },
  build: {
    outDir: 'build',
  }
})
