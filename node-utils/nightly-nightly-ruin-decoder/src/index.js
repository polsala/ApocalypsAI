#!/usr/bin/env node
const runeMap = {
  "☀": "a",
  "☁": "b",
  "☂": "c",
  "☃": "d",
  "★": "e",
  "✖": "f",
  "✿": "g",
  "♞": "h",
  "♣": "i",
  "♠": "j"
};

function decode(input) {
  return input.split('').map(ch => runeMap[ch] || ch).join('');
}

// CLI handling
if (require.main === module) {
  const fs = require('fs');
  const args = process.argv.slice(2);
  if (args.includes('--help') || args.includes('-h')) {
    console.log('Usage: node src/index.js [rune-string]');
    console.log('If no argument is given, reads from stdin.');
    process.exit(0);
  }
  const getInput = () => {
    if (args.length > 0) {
      return Promise.resolve(args[0]);
    }
    return new Promise((resolve, reject) => {
      let data = '';
      process.stdin.setEncoding('utf8');
      process.stdin.on('data', chunk => data += chunk);
      process.stdin.on('end', () => resolve(data.trim()));
      process.stdin.on('error', reject);
    });
  };
  getInput().then(input => {
    const output = decode(input);
    console.log(output);
  }).catch(err => {
    console.error('Error reading input:', err);
    process.exit(1);
  });
}

module.exports = { decode };
