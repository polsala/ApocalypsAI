#!/usr/bin/env node

/**
 * nightly-emoji-storyboard
 * -----------------------
 * Convert a sentence into a space‑separated emoji storyboard.
 *
 * The utility ships with a small built‑in dictionary.  Unknown words are
 * represented by the ❓ emoji.  Plural forms ending with "s" are stripped
 * before lookup.
 */

const EMOJI_MAP = {
  love: '❤️',
  fire: '🔥',
  water: '💧',
  sun: '☀️',
  moon: '🌙',
  star: '⭐',
  happy: '😊',
  sad: '😢',
  cat: '🐱',
  dog: '🐶',
  rain: '🌧️',
  snow: '❄️',
  coffee: '☕',
  music: '🎵'
};

/**
 * Normalise a word: lower‑case and strip non‑alphabetic characters.
 * @param {string} word
 * @returns {string}
 */
function normalize(word) {
  return word.toLowerCase().replace(/[^a-z]/g, '');
}

/**
 * Map a single word to its emoji representation.
 * @param {string} word
 * @returns {string}
 */
function mapWord(word) {
  const base = normalize(word);
  if (EMOJI_MAP[base]) return EMOJI_MAP[base];
  // Try singular form if the word ends with 's'
  if (base.endsWith('s')) {
    const singular = base.slice(0, -1);
    if (EMOJI_MAP[singular]) return EMOJI_MAP[singular];
  }
  return '❓';
}

/**
 * Convert a full sentence into an emoji storyboard.
 * @param {string} text Input sentence.
 * @returns {string} Space‑separated emojis.
 */
function generateStoryboard(text) {
  if (typeof text !== 'string') return '';
  const words = text.trim().split(/\s+/);
  const emojis = words.map(mapWord);
  return emojis.join(' ');
}

// CLI handling – only runs when executed directly
if (require.main === module) {
  const input = process.argv.slice(2).join(' ');
  if (!input) {
    console.error('Usage: node src/index.js "Your sentence here"');
    process.exit(1);
  }
  console.log(generateStoryboard(input));
}

// Export for external use and testing
module.exports = { generateStoryboard };
