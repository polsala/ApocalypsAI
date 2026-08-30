#!/usr/bin/env node
const fs = require('fs');

function analyzeMood(text) {
  const lower = text.toLowerCase();
  const happy = ['happy','joy','great','love','glad','awesome','fantastic','good','wonderful'];
  const sad = ['sad','down','upset','bad','unhappy','depressed','blue','miserable'];
  const angry = ['angry','mad','furious','irate','annoyed','hate','rage'];
  if (happy.some(w => lower.includes(w))) return '😊';
  if (sad.some(w => lower.includes(w))) return '😢';
  if (angry.some(w => lower.includes(w))) return '😠';
  return '🤔';
}

// CLI handling
if (require.main === module) {
  const input = process.argv[2];
  if (input) {
    console.log(analyzeMood(input));
  } else {
    let data = '';
    process.stdin.setEncoding('utf8');
    process.stdin.on('data', chunk => data += chunk);
    process.stdin.on('end', () => {
      console.log(analyzeMood(data.trim()));
    });
  }
}

module.exports = { analyzeMood };
