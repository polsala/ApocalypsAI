#!/usr/bin/env node

const fs = require('fs');
const filePath = process.argv[2];

if (!filePath) {
  console.error('Usage: node src/index.js <file>');
  process.exit(1);
}

let text;
try {
  text = fs.readFileSync(filePath, 'utf8');
} catch (e) {
  console.error('Error reading file:', e.message);
  process.exit(1);
}

const positive = ['happy','joy','love','wonderful','great','good','awesome','fantastic','delight','smile'];
const negative = ['sad','bad','terrible','hate','angry','pain','sorrow','depress','cry','upset'];

function countWords(words, txt) {
  const regex = new RegExp(`\\b(${words.join('|')})\\b`, 'gi');
  const matches = txt.match(regex);
  return matches ? matches.length : 0;
}

const posCount = countWords(positive, text);
const negCount = countWords(negative, text);

let emoji;
if (posCount > negCount) {
  emoji = '😊';
} else if (negCount > posCount) {
  emoji = '😢';
} else {
  emoji = '😐';
}

console.log(emoji);

module.exports = {
  countWords,
  positive,
  negative,
  analyzeMood: (txt) => {
    const p = countWords(positive, txt);
    const n = countWords(negative, txt);
    return p > n ? '😊' : n > p ? '😢' : '😐';
  }
};
