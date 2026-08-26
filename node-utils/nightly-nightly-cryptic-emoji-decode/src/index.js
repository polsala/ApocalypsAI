// nightly-cryptic-emoji-decoder – core implementation
// No external dependencies; uses only Node's built‑in modules.

const emojiMap = {
  "C": "🐱",
  "D": "🐶",
  "F": "🦊",
  "R": "🐰",
  "P": "🐼",
  "L": "🦁",
  "A": "🐸",
  "M": "🐵",
  "E": "🐔",
  "N": "🐧"
};

// Build reverse lookup for decoding
const reverseMap = Object.entries(emojiMap).reduce((acc, [letter, emoji]) => {
  acc[emoji] = letter;
  return acc;
}, {});

/**
 * Encode a plain‑text string into its emoji representation.
 * Unmapped characters are left unchanged.
 * @param {string} text
 * @returns {string}
 */
function encode(text) {
  return text
    .toUpperCase()
    .split("")
    .map(ch => emojiMap[ch] || ch)
    .join("");
}

/**
 * Decode an emoji string back to plain text.
 * Unmapped emojis/characters are left unchanged.
 * @param {string} emojiStr
 * @returns {string}
 */
function decode(emojiStr) {
  // Split by Unicode code points to correctly handle emojis
  const chars = Array.from(emojiStr);
  return chars
    .map(ch => reverseMap[ch] || ch)
    .join("");
}

// Simple CLI handling
if (require.main === module) {
  const [, , command, input] = process.argv;
  if (!command || !input) {
    console.error("Usage: node src/index.js <encode|decode> <string>");
    process.exit(1);
  }
  if (command === "encode") {
    console.log(encode(input));
  } else if (command === "decode") {
    console.log(decode(input));
  } else {
    console.error("Unknown command. Use 'encode' or 'decode'.");
    process.exit(1);
  }
}

module.exports = { encode, decode };
