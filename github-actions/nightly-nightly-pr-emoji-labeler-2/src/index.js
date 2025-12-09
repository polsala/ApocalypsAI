// src/index.js
// Simple PR title → emoji label mapper
// Exported for testing and usable as a GitHub Action entry point.

/**
 * Compute an emoji label based on a PR title.
 * @param {string} title - The pull‑request title.
 * @returns {string} Emoji label.
 */
function computeLabel(title) {
  if (!title) return "🤖 unknown";
  const lowered = title.toLowerCase();
  const mappings = [
    { keyword: "bug", label: "🐞 bug" },
    { keyword: "feature", label: "✨ feature" },
    { keyword: "docs", label: "📚 docs" },
    { keyword: "test", label: "✅ test" },
    { keyword: "refactor", label: "🔧 refactor" },
    { keyword: "chore", label: "🧹 chore" }
  ];
  for (const { keyword, label } of mappings) {
    if (lowered.includes(keyword)) {
      return label;
    }
  }
  return "🤖 unknown";
}

// When executed as a GitHub Action, inputs are provided via env vars prefixed with INPUT_
if (require.main === module) {
  const title = process.env["INPUT_TITLE"];
  const label = computeLabel(title);
  // GitHub Actions v2 uses core.setOutput, but we avoid extra deps.
  // The legacy "set-output" command still works in most runners.
  console.log(`::set-output name=label::${label}`);
}

module.exports = { computeLabel };
