#!/usr/bin/env node
const fs = require('fs');

const POSITIVE_WORDS = new Set(['happy','joy','love','great','good','fantastic','thrilled','awesome','wonderful','delight','excited','glad']);
const NEGATIVE_WORDS = new Set(['sad','bad','terrible','hate','angry','upset','depressed','gloomy','miserable','unhappy','worst','awful']);

function scoreText(text) {
  const words = text.toLowerCase().match(/\b\w+\b/g) || [];
  let score = 0;
  for (const w of words) {
    if (POSITIVE_WORDS.has(w)) score += 1;
    if (NEGATIVE_WORDS.has(w)) score -= 1;
  }
  return score;
}

function moodEmoji(score) {
  if (score >= 2) return '😊';
  if (score <= -2) return '😡';
  if (score < 0) return '😢';
  if (score > 0) return '😊';
  return '😐';
}

function analyzeMood(text) {
  const s = scoreText(text);
  return moodEmoji(s);
}

// CLI handling
if (require.main === module) {
  const input = process.argv.slice(2).join(' ');
  if (!input) {
    console.error('Usage: emoji-mood "<text>"');
    process.exit(1);
  }
  console.log(analyzeMood(input));
}

// Export for tests
module.exports = { analyzeMood };
