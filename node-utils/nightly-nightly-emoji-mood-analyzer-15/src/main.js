#!/usr/bin/env node
const fs = require('fs');

const positiveWords = ['love','happy','joy','awesome','great','good','fantastic','wonderful','sunny','excited','delight','pleased'];
const negativeWords = ['hate','sad','bad','terrible','awful','gloomy','depressed','angry','upset','pain','sick','worst'];

function analyzeMood(text) {
  const words = text.toLowerCase().match(/\b\w+\b/g) || [];
  let score = 0;
  for (const w of words) {
    if (positiveWords.includes(w)) score += 1;
    if (negativeWords.includes(w)) score -= 1;
  }
  if (score > 1) return '😊';
  if (score === 1) return '🙂';
  if (score === 0) return '😐';
  if (score === -1) return '🙁';
  return '😞';
}

// CLI handling
if (require.main === module) {
  let input = '';
  if (process.argv.length > 2) {
    input = process.argv.slice(2).join(' ');
    console.log(analyzeMood(input));
  } else {
    // read from stdin
    process.stdin.setEncoding('utf8');
    process.stdin.on('data', chunk => input += chunk);
    process.stdin.on('end', () => {
      console.log(analyzeMood(input.trim()));
    });
  }
}

module.exports = { analyzeMood };
