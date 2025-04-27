import js from "@eslint/js";
import globals from "globals";
import pluginVue from "eslint-plugin-vue";
import { defineConfig } from "eslint/config";


export default defineConfig([
  { files: ["**/*.{js,mjs,cjs,vue}"], plugins: { js }, extends: ["js/recommended"] },
  { files: ["**/*.{js,mjs,cjs,vue}"], languageOptions: { globals: globals.browser } },
  pluginVue.configs["flat/essential"],
]);
// .eslintrc.js 或 .eslintrc.json
module.exports = {
  // 旧配置方式（已废弃）
  // reportUnusedDisableDirectives: 'warn',

  // 新配置方式（v8.55.0+）
  overrideConfig: {
    linterOptions: {
      reportUnusedDisableDirectives: 'warn' // 可选值：'off'/'warn'/'error'
    }
  }
}