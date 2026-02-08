const { computeEmojis } = require("../src/emoji");

test("computeEmojis returns correct emojis for commit types", () => {
  const messages = [
    "feat: add new login flow",
    "fix: correct typo",
    "docs: update README",
    "style: format code",
    "refactor: improve utils",
    "test: add unit tests",
    "chore: bump version",
    "perf: improve performance",
    "build: update CI config",
    "ci: add lint step",
    "revert: revert previous commit"
  ];
  const emojis = computeEmojis(messages);
  expect(emojis).toEqual([
    "✨",
    "🐛",
    "📚",
    "🎨",
    "♻️",
    "✅",
    "🔧",
    "⚡️",
    "🏗️",
    "🤖",
    "⏪"
  ]);
});

test("computeEmojis skips unknown types", () => {
  const messages = ["unknown: something", "feat: new feature"];
  const emojis = computeEmojis(messages);
  expect(emojis).toEqual(["✨"]);
});
