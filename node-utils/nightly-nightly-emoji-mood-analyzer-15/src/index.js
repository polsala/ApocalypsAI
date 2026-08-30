#!/usr/bin/env node
const fs = require('fs');

function analyzeMood(text) {
  const lower = text.toLowerCase();
  const positive = ['happy','joy','love','awesome','great','fantastic','good','wonderful','😊','😀','😁'];
  const negative = ['sad','angry','hate','bad','terrible','awful','😢','😠','😭'];
  let score = 0;
  for (const word of positive) {
    if (lower.includes(word)) score++;
  }
  for (const word of negative) {
    if (lower.includes(word)) score--;
  }
  if (score > 0) return '😊';
  if (score < 0) return '😢';
  return '😐';
}

// CLI handling
if (require.main === module) {
  const input = process.argv.slice(2).join(' ');
  if (input) {
    console.log(analyzeMood(input));
  } else {
    // read from stdin
    let data = '';
    process.stdin.setEncoding('utf8');
    process.stdin.on('data', chunk => data += chunk);
    process.stdin.on('end', () => {
      console.log(analyzeMood(data.trim()));
    });
  }
}

// Export for tests
module.exports = { analyzeMood };
