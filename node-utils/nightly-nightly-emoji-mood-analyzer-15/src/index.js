//!/usr/bin/env node

/**
 * nightly-emoji-mood-analyzer
 *
 * Simple sentiment analysis that maps a sentence to an emoji.
 * No external dependencies – pure JavaScript.
 */

const fs = require('fs');

// Tiny word lists for demonstration purposes
const POSITIVE_WORDS = new Set([
  'love', 'happy', 'joy', 'joyful', 'great', 'good', 'awesome', 'fantastic', 'excellent', 'wonderful', 'sunny', 'delight', 'delighted', 'pleased', 'smile', 'smiles', 'laugh', 'laughs', 'fun', 'funny', 'cheer', 'cheerful', 'bright', 'optimistic', 'hope', 'hopeful', 'peace', 'peaceful'
]);

const NEGATIVE_WORDS = new Set([
  'hate', 'sad', 'angry', 'bad', 'terrible', 'awful', 'horrible', 'depressed', 'frustrated', 'annoyed', 'upset', 'pain', 'painful', 'sick', 'sickly', 'storm', 'rainy', 'gloom', 'gloomy', 'dark', 'pessimistic', 'fear', 'fearful', 'worried', 'stress', 'stressful'
]);

/**
 * Tokenises a string into lower‑cased words, stripping punctuation.
 * @param {string} text
 * @returns {string[]}
 */
function tokenize(text) {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, ' ') // replace punctuation with space
    .split(/\s+/)
    .filter(Boolean);
}

/**
 * Computes a simple sentiment score.
 * Positive matches add +1, negative matches add -1.
 * @param {string} text
 * @returns {number}
 */
function sentimentScore(text) {
  const words = tokenize(text);
  let score = 0;
  for (const w of words) {
    if (POSITIVE_WORDS.has(w)) score += 1;
    else if (NEGATIVE_WORDS.has(w)) score -= 1;
  }
  return score;
}

/**
 * Maps a sentiment score to an emoji.
 * @param {number} score
 * @returns {string}
 */
function scoreToEmoji(score) {
  if (score > 1) return '😄';
  if (score < -1) return '😞';
  return '😐';
}

/**
 * Main entry point – reads input from argv or stdin and prints the emoji.
 */
function main() {
  const args = process.argv.slice(2);
  if (args.length > 0) {
    const input = args.join(' ');
    const emoji = scoreToEmoji(sentimentScore(input));
    console.log(emoji);
  } else {
    // No arguments – read from stdin
    let data = '';
    process.stdin.setEncoding('utf8');
    process.stdin.on('data', chunk => data += chunk);
    process.stdin.on('end', () => {
      const emoji = scoreToEmoji(sentimentScore(data.trim()));
      console.log(emoji);
    });
  }
}

if (require.main === module) {
  main();
}

// Export for testing purposes
module.exports = { tokenize, sentimentScore, scoreToEmoji };
