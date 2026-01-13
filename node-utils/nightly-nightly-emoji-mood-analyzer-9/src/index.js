#!/usr/bin/env node
const fs = require('fs');

function analyzeMood(text) {
  const positive = ['happy','joy','love','great','awesome','fantastic','good','wonderful','excellent','pleased'];
  const negative = ['sad','angry','hate','terrible','bad','awful','depressed','upset','mad','worst'];
  const words = text.toLowerCase().match(/\w+/g) || [];
  let posCount = 0;
  let negCount = 0;
  for (const w of words) {
    if (positive.includes(w)) posCount++;
    if (negative.includes(w)) negCount++;
  }
  if (posCount > negCount) return 'ð';
  if (negCount > posCount) return 'ð ';
  return 'ð¤';
}

// CLI handling
function main() {
  const args = process.argv.slice(2);
  let inputPromise;
  if (args.length > 0) {
    inputPromise = Promise.resolve(args.join(' '));
  } else {
    // read from stdin
    inputPromise = new Promise((resolve) => {
      let data = '';
      process.stdin.setEncoding('utf8');
      process.stdin.on('data', chunk => data += chunk);
      process.stdin.on('end', () => resolve(data.trim()));
    });
  }
  inputPromise.then(text => {
    if (!text) {
      console.error('No input provided.');
      process.exit(1);
    }
    const emoji = analyzeMood(text);
    console.log(emoji);
  });
}

if (require.main === module) {
  main();
}

module.exports = { analyzeMood };
