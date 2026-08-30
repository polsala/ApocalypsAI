#!/usr/bin/env node
const fs = require('fs');

const POSITIVE = new Set([
  'love','happy','joy','awesome','great','good','fantastic','wonderful','sunny','delight','excited','amazing','pleased','smile','smiling','cheer','cheerful','glad'
]);
const NEGATIVE = new Set([
  'hate','sad','bad','terrible','awful','depressed','angry','upset','pain','painful','disappointed','unhappy','sick','sucks','worst','mad'
]);

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

function main() {
  const argPath = process.argv[2];
  if (argPath) {
    try {
      const data = fs.readFileSync(argPath, 'utf8');
      process.stdout.write(analyzeMood(data) + '\n');
    } catch (e) {
      console.error('Error reading file:', e.message);
      process.exit(1);
    }
  } else {
    // read from stdin
    let input = '';
    process.stdin.setEncoding('utf8');
    process.stdin.on('data', chunk => input += chunk);
    process.stdin.on('end', () => {
      process.stdout.write(analyzeMood(input) + '\n');
    });
  }
}

if (require.main === module) {
  main();
}

module.exports = { analyzeMood };
