const typeToEmoji = {
  feat: "✨",
  fix: "🐛",
  docs: "📚",
  style: "🎨",
  refactor: "♻️",
  test: "✅",
  chore: "🔧",
  perf: "⚡️",
  build: "🏗️",
  ci: "🤖",
  revert: "⏪"
};

function extractType(message) {
  const match = message.split(":")[0].split("(")[0].trim();
  return match;
}

function computeEmojis(commitMessages) {
  const seen = new Set();
  const emojis = [];
  for (const msg of commitMessages) {
    const type = extractType(msg);
    const emoji = typeToEmoji[type];
    if (emoji && !seen.has(emoji)) {
      seen.add(emoji);
      emojis.push(emoji);
    }
  }
  return emojis;
}

module.exports = { computeEmojis, extractType, typeToEmoji };
