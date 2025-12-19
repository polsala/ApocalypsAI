#!/usr/bin/env node
const fs = require('fs');

const POSITIVE = [
  'happy','joy','love','great','good','awesome','fantastic','wonderful','excited','glad','pleased','delight','smile'
];
const NEGATIVE = [
  'sad','bad','terrible','hate','angry','upset','depressed','unhappy','miserable','pain','sorrow','cry','gloom','annoyed'
];

function analyze(text) {
  const words = text.toLowerCase().match(/\b\w+\b/g) || [];
  let pos = 0, neg = 0;
  for (const w of words) {
    if (POSITIVE.includes(w)) pos++;
    if (NEGATIVE.includes(w)) neg++;
  }
  if (pos > neg) return '😊';
  if (neg > pos) return '☹️';
  return '😐';
}

function main() {
  let input = '';
  process.stdin.setEncoding('utf8');
  process.stdin.on('data', chunk => input += chunk);
  process.stdin.on('end', () => {
    const result = analyze(input);
    console.log(result);
  });
}

if (require.main === module) {
  main();
}
