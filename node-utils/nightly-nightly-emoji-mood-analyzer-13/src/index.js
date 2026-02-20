// nightly-emoji-mood-analyzer
// SPDX-License-Identifier: MIT

/**
 * Simple sentiment analysis based on handcrafted word lists.
 * Returns an emoji representing the overall mood.
 *
 * @param {string} text - Input text to analyse.
 * @returns {string} Emoji (😊, 😢, or 😐).
 */
function analyzeMood(text) {
  const positiveWords = [
    "happy",
    "joy",
    "love",
    "great",
    "awesome",
    "fantastic",
    "good",
    "wonderful",
    "excellent",
    "pleased"
  ];
  const negativeWords = [
    "sad",
    "angry",
    "hate",
    "terrible",
    "bad",
    "awful",
    "horrible",
    "depressed",
    "upset",
    "disappointed"
  ];

  const normalize = word => word.toLowerCase().replace(/[^a-z]/g, "");
  const tokens = text.split(/\s+/).map(normalize).filter(Boolean);

  let pos = 0;
  let neg = 0;
  for (const token of tokens) {
    if (positiveWords.includes(token)) pos++;
    if (negativeWords.includes(token)) neg++;
  }

  if (pos > neg) return "😊";
  if (neg > pos) return "😢";
  return "😐";
}

// CLI handling
if (require.main === module) {
  const fs = require("fs");
  const path = process.argv[2];
  let input = "";
  if (path) {
    try {
      input = fs.readFileSync(path, "utf8");
    } catch (e) {
      console.error(`Error reading file: ${e.message}`);
      process.exit(1);
    }
  } else {
    // Read from STDIN synchronously
    const stdin = fs.readFileSync(0, "utf8"); // 0 = STDIN
    input = stdin;
  }
  const mood = analyzeMood(input);
  console.log(mood);
}

module.exports = { analyzeMood };
