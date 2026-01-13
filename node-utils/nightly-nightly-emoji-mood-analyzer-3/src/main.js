/*
  nightly-emoji-mood-analyzer
  --------------------------------
  A tiny utility that maps a short piece of text to an emoji representing its mood.
  No external dependencies â pure JavaScript.
*/

// Simple word lists for sentiment scoring
const POSITIVE_WORDS = [
  'love', 'happy', 'joy', 'joyful', 'glad', 'great', 'awesome', 'fantastic', 'good', 'wonderful', 'excellent', 'amazing', 'thrilled', 'excited', 'sunny', 'delight', 'pleased', 'cheer', 'smile'
];

const NEGATIVE_WORDS = [
  'sad', 'bad', 'terrible', 'awful', 'hate', 'angry', 'upset', 'depressed', 'gloomy', 'rainy', 'pain', 'hurt', 'sick', 'unhappy', 'miserable', 'worst', 'disappointed', 'cry', 'crying'
];

/**
 * Normalizes a string: lowerâcases and removes punctuation.
 * @param {string} text
 * @returns {string[]} Array of words
 */
function tokenize(text) {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, ' ')
    .split(/\s+/)
    .filter(Boolean);
}

/**
 * Calculates a simple sentiment score based on the word lists.
 * @param {string} text
 * @returns {number} Positive, zero, or negative integer
 */
function scoreText(text) {
  const words = tokenize(text);
  let score = 0;
  for (const w of words) {
    if (POSITIVE_WORDS.includes(w)) score += 1;
    else if (NEGATIVE_WORDS.includes(w)) score -= 1;
  }
  return score;
}

/**
 * Maps a sentiment score to an emoji.
 * @param {number} score
 * @returns {string} Emoji character
 */
function scoreToEmoji(score) {
  if (score > 0) return 'ð';
  if (score < 0) return 'ð¢';
  return 'ð';
}

/**
 * Public API â analyzes mood of a given text and returns an emoji.
 * @param {string} text
 * @returns {string} Emoji representing the mood
 */
function analyzeMood(text) {
  const score = scoreText(text);
  return scoreToEmoji(score);
}

// CLI handling â when executed directly
if (require.main === module) {
  const input = process.argv.slice(2).join(' ');
  if (!input) {
    console.error('Usage: node src/main.js "Your text here"');
    process.exit(1);
  }
  console.log(analyzeMood(input));
}

module.exports = { analyzeMood, scoreText, scoreToEmoji };
