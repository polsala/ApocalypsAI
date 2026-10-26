#!/usr/bin/env node

/**
 * Simple mood analyzer that maps text to an emoji.
 * Exported function `analyzeMood(text)` can be used programmatically.
 * When executed directly, the script reads a string from the first CLI argument
 * or from STDIN (if no argument is provided) and prints the resulting emoji.
 */

const POSITIVE_WORDS = new Set([
  "love",
  "happy",
  "joy",
  "great",
  "awesome",
  "fantastic",
  "good",
  "wonderful",
  "excellent",
  "delight",
  "pleased",
  "glad",
  "sunny",
  "smile",
]);

const NEGATIVE_WORDS = new Set([
  "sad",
  "bad",
  "terrible",
  "horrible",
  "unhappy",
  "depressed",
  "down",
  "gloomy",
  "miserable",
  "sorrow",
]);

const ANGRY_WORDS = new Set([
  "angry",
  "mad",
  "furious",
  "irate",
  "annoyed",
  "frustrated",
  "hate",
  "rage",
  "outraged",
]);

/**
 * Tokenizes input text into lowercase words.
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
 * Computes a sentiment score based on word lists.
 * Positive word: +1, Negative word: -1, Angry word: -2.
 * @param {string} text
 * @returns {number}
 */
function computeScore(text) {
  let score = 0;
  for (const word of tokenize(text)) {
    if (POSITIVE_WORDS.has(word)) {
      score += 1;
    } else if (NEGATIVE_WORDS.has(word)) {
      score -= 1;
    } else if (ANGRY_WORDS.has(word)) {
      score -= 2;
    }
  }
  return score;
}

/**
 * Maps a numeric score to an emoji.
 * @param {number} score
 * @returns {string}
 */
function scoreToEmoji(score) {
  if (score >= 2) return "😊"; // happy
  if (score <= -2) return "😠"; // angry
  if (score < 0) return "😞"; // sad
  return "😐"; // neutral
}

/**
 * Public API: analyze a piece of text and return a mood emoji.
 * @param {string} text
 * @returns {string} Emoji representing the mood.
 */
function analyzeMood(text) {
  const score = computeScore(text || "");
  return scoreToEmoji(score);
}

// CLI handling
if (require.main === module) {
  // If an argument is supplied, use it; otherwise read from stdin.
  const arg = process.argv[2];
  if (arg) {
    console.log(analyzeMood(arg));
  } else {
    // Read all data from stdin.
    let data = "";
    process.stdin.setEncoding("utf8");
    process.stdin.on("data", chunk => (data += chunk));
    process.stdin.on("end", () => {
      console.log(analyzeMood(data.trim()));
    });
  }
}

module.exports = { analyzeMood };
