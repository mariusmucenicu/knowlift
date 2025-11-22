import { defineConfig } from "eslint/config";

import globals from "globals";
import js from "@eslint/js";
import stylistic from '@stylistic/eslint-plugin';


export default defineConfig([
  {
    files: ["**/*.js"],
    plugins: { js, "@stylistic": stylistic },
    extends: ["js/recommended", "@stylistic/recommended"],
    languageOptions: {
      globals: { ...globals.browser, ...globals.node },
    },
  },
]);
