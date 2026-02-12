#!/usr/bin/env node
const fs = require('fs');

const POSITIVE = new Set(['happy','joy','love','great','good','awesome','fantastic','excellent','wonderful','pleased','delight']);
const NEGATIVE = new Set(['sad','bad','terrible','hate','angry','awful','horrible','depressed','upset','pain']);

function analyzeMood(text) {
  const words = text.toLowerCase().match(/\b\w+\b/g) || [];
  let score = 0;
  for (const w of words) {
    if (POSITIVE.has(w)) score++;
    else if (NEGATIVE.has(w)) score--;
  }
  if (score > 0) return '😊';
  if (score < 0) return '😞';
  return '😐';
}

// CLI mode
if (require.main === module) {
  const filePath = process.argv[2];
  if (!filePath) {
    console.error('Usage: node src/index.js <path-to-text-file>');
    process.exit(1);
  }
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    console.log(analyzeMood(content));
  } catch (err) {
    console.error('Error reading file:', err.message);
    process.exit(1);
  }
}

module.exports = { analyzeMood };
