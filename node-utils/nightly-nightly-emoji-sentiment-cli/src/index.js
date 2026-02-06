#!/usr/bin/env node
const fs = require('fs');

// Simple emoji → sentiment map. Positive emojis = +1, negative emojis = -1.
const emojiSentiment = {
  "😀": 1, "😃": 1, "😄": 1, "😁": 1, "😂": 1, "🤣": 1, "😊": 1, "😇": 1, "🙂": 1, "🙃": 1, "👍": 1,
  "😞": -1, "😔": -1, "😟": -1, "😕": -1, "🙁": -1, "☹️": -1, "😢": -1, "😭": -1, "👎": -1
};

/**
 * Analyze a string and return the summed sentiment score of any emojis it contains.
 * @param {string} text Input text.
 * @returns {number} Sentiment score (positive, negative or zero).
 */
function analyze(text) {
  let score = 0;
  // Spread the string into an array of Unicode code points to correctly handle emojis.
  for (const char of [...text]) {
    if (Object.prototype.hasOwnProperty.call(emojiSentiment, char)) {
      score += emojiSentiment[char];
    }
  }
  return score;
}

function main() {
  // If arguments are supplied, join them as the input; otherwise read from stdin.
  const input = process.argv.slice(2).join(' ') || fs.readFileSync(0, 'utf8');
  const score = analyze(input);
  console.log(`Sentiment score: ${score}`);
}

if (require.main === module) {
  main();
}

module.exports = { analyze };
