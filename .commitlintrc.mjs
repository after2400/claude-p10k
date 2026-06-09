export default {
  extends: ["@commitlint/config-conventional"],
  rules: {
    // 0 = off, 1 = warn, 2 = error  |  "always" / "never"
    "scope-enum": [
      2,
      "always",
      [
        "statusline", // statusline.py changes
        "ci",         // GitHub Actions workflows
        "docs",       // README and documentation
        "config",     // commitlint, ruff, pre-commit config
      ],
    ],
    "scope-empty": [0, "never"], // scope is optional
    "type-enum": [
      2,
      "always",
      [
        // conventional commits standard types
        "feat",
        "fix",
        "docs",
        "style",
        "refactor",
        "perf",
        "test",
        "build",
        "ci",
        "chore",
        "revert",
        // add custom types below
      ],
    ],
  },
};
