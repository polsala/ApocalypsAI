// decoder.js
const EMOJI_MAP = {
  "🍎": "A",
  "🍌": "B",
  "🍒": "C",
  "🍇": "D",
  "🍉": "E",
  "🍓": "F",
  "🍑": "G",
  "🍍": "H",
  "🥝": "I",
  "🥭": "J"
};

/**
 * Decode a string of emojis into letters.
 * Unmapped emojis become '?'.
 * @param {string} input
 * @returns {string}
 */
function decodeEmojis(input) {
  // Spread to correctly handle surrogate pairs
  const chars = [...input];
  return chars.map(ch => EMOJI_MAP[ch] || "?").join("");
}

module.exports = { decodeEmojis };
