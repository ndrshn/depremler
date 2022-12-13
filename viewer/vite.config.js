import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import path from "path";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: [
      {
        find: "@",
        replacement: path.resolve(__dirname, "./src"),
      },
      {
        find: "~",
        replacement: path.resolve(__dirname, "./src"),
      },
    ],
    optimizeDeps: {
      exclude: ["ant-design-vue", "@antv/g2plot"],
    },
  },
});
