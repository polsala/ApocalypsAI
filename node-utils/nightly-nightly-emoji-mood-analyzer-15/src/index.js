#!/usr/bin/env node
const fs = require('fs');

const POSITIVE = new Set(['love','happy','joy','awesome','great','good','fantastic','wonderful','excellent','sunny','like','pleased','delight','smile']);
const NEGATIVE = new Set(['hate','sad','bad','terrible','awful','horrible','angry','mad','upset','depressed','rain','storm','pain','sick','worst']);

function analyzeMood(text) {
  const words = text.toLowerCase().match(/\\b\\w+\\b/g) || [];
  let score = 0;
  for (const w of words) {
    if (POSITIVE.has(w)) score++;
    if (NEGATIVE.has(w)) score--;
  }
  if (score > 1) return '😄';
  if (score === 1) return '😊';
  if (score === 0) return '😐';
  if (score === -1) return '🙁';
  return '😢';
}

// CLI mode
if (require.main === module) {
  const input = process.argv.slice(2).join(' ');
  if (!input) {
    console.error('Usage: node src/index.js "your sentence"');
    process.exit(1);
  }
  console.log(analyzeMood(input));
}

// Export for tests
module.exports = { analyzeMood };
