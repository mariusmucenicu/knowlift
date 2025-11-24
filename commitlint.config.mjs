const Configuration = {
  /* Resolve and load @commitlint/config-conventional from node_modules. */
  extends: ["@commitlint/config-conventional"],

  /* Resolve and load @commitlint/format from node_modules. */
  formatter: "@commitlint/format",

  /* Any rules defined here will override rules from the extended config */
  rules: {
    "subject-case": [2, "always", ["sentence-case", "lower-case"]],
  },

  /* Array of functions that return true if a message should be ignored. */
  ignores: [(commit) => commit === ""],

  /* To disable the ignores above and run rules always, set this to false */
  defaultIgnores: true,

  /* Custom URL to show upon failure */
  helpUrl:
    "https://github.com/conventional-changelog/commitlint/#what-is-commitlint",
};

export default Configuration;
