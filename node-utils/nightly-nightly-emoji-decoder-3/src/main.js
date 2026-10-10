#!/usr/bin/env node

const fs = require('fs');

// ---------------------------------------------------------------------
// Emoji‑to‑word mapping (whimsical post‑apocalyptic lexicon)
// ---------------------------------------------------------------------
const mapping = {
  "🌞": "sun",
  "🌧️": "rain",
  "🔥": "fire",
  "💧": "water",
  "🧟": "zombie",
  "⚔️": "battle",
  "🛡️": "shield",
  "🚀": "rocket",
  "🌍": "world",
  "🕰️": "time"
};

function printList() {
  for (const [emoji, word] of Object.entries(mapping)) {
    console.log(`${emoji}: ${word}`);
  }
}

function decode(input) {
  // Split the string into Unicode grapheme clusters (handles surrogate pairs)
  const chars = Array.from(input);
  const words = chars.map(ch => mapping[ch] || "?");
  return words.join(' ');
}

// ---------------------------------------------------------------------
// Argument handling
// ---------------------------------------------------------------------
const args = process.argv.slice(2);

if (args.includes('--list')) {
  printList();
  process.exit(0);
}

let input = '';
if (args.length > 0) {
  // Concatenate all arguments (allows space‑separated emojis)
  input = args.join('');
} else {
  // Read from stdin when no arguments are supplied
  try {
    input = fs.readFileSync(0, 'utf8').trim(); // 0 = STDIN
  } catch (e) {
    console.error('Failed to read from stdin:', e.message);
    process.exit(1);
  }
}

const result = decode(input);
console.log(result);
