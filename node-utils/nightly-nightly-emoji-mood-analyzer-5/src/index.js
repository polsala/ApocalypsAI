// nightly-emoji-mood-analyzer
// Pure Node.js implementation – no external dependencies.

const POSITIVE_WORDS = [
  "love",
  "happy",
  "joy",
  "great",
  "awesome",
  "fantastic",
  "good",
  "wonderful",
  "excellent",
  "promotion",
  "celebrate",
  "win",
  "success",
  "sunny",
  "blessed",
];

const NEGATIVE_WORDS = [
  "sad",
  "bad",
  "terrible",
  "hate",
  "angry",
  "upset",
  "lost",
  "fail",
  "failure",
  "depressed",
  "unhappy",
  "rainy",
  "storm",
];

const ANGRY_WORDS = [
  "angry",
  "furious",
  "mad",
  "irate",
  "enraged",
  "outraged",
];

/**
 * Simple tokenizer that lower‑cases and splits on non‑word characters.
 * @param {string} text
 * @returns {string[]}
 */
function tokenize(text) {
  return text
    .toLowerCase()
    .split(/[^a-zA-Z]+/)
    .filter(Boolean);
}

/**
 * Determines sentiment score based on word lists.
 * @param {string[]} tokens
 * @returns {'positive'|'negative'|'angry'|'neutral'}
 */
function analyzeSentiment(tokens) {
  let pos = 0,
    neg = 0,
    angry = 0;
  for (const token of tokens) {
    if (POSITIVE_WORDS.includes(token)) pos++;
    if (NEGATIVE_WORDS.includes(token)) neg++;
    if (ANGRY_WORDS.includes(token)) angry++;
  }
  if (angry > Math.max(pos, neg)) return "angry";
  if (pos > neg) return "positive";
  if (neg > pos) return "negative";
  return "neutral";
}

/**
 * Maps sentiment to an emoji.
 * @param {'positive'|'negative'|'angry'|'neutral'} sentiment
 * @returns {string}
 */
function sentimentToEmoji(sentiment) {
  switch (sentiment) {
    case "positive":
      return "🎉";
    case "negative":
      return "😞";
    case "angry":
      return "😡";
    default:
      return "🤔";
  }
}

/**
 * Main entry point – reads CLI argument and prints emoji.
 */
function main() {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.error("Usage: node src/index.js \"Your text here\"");
    process.exit(1);
  }
  const input = args.join(" ");
  const tokens = tokenize(input);
  const sentiment = analyzeSentiment(tokens);
  const emoji = sentimentToEmoji(sentiment);
  console.log(emoji);
}

if (require.main === module) {
  main();
}

// Export functions for testing purposes
module.exports = { tokenize, analyzeSentiment, sentimentToEmoji };
