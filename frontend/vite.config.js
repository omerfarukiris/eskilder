import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

const backend = "http://127.0.0.1:8000";

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/api": backend,
      "/yonetim": backend,
      "/media": backend,
      "/sitemap.xml": backend,
      "/robots.txt": backend,
    },
  },
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: ["./src/test-kurulum.js"],
    css: { modules: { classNameStrategy: "non-scoped" } },
  },
});
