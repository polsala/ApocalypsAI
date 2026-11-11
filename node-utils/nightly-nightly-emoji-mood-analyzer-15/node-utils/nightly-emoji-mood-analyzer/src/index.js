#!/usr/bin/env node
const fs = require('fs');

const happyWords = ['happy','joy','love','awesome','great','good','fantastic','wonderful','delight','smile','sunny'];
const sadWords = ['sad','bad','terrible','unhappy','depressed','gloom','cry','down','sorrow','pain'];
const angryWords = ['angry','mad','furious','hate','annoy','irritated','rage','storm','fury','upset'];

function analyzeMood(text) {
  const words = text.toLowerCase().match(/\b\w+\b/g) || [];
  let happy = 0, sad = 0, angry = 0;
  for (const w of words) {
    if (happyWords.includes(w)) happy++;
    if (sadWords.includes(w)) sad++;
    if (angryWords.includes(w)) angry++;
  }
  if (happy === 0 && sad === 0 && angry === 0) return '🤔';
  const max = Math.max(happy, sad, angry);
  if (max === happy) return '😊';
  if (max === sad) return '😢';
  return '😠';
}

// CLI handling
if (require.main === module) {
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
      process.stdin.on('end', () => resolve(data));
    });
  }
  inputPromise.then(text => {
    const emoji = analyzeMood(text);
    console.log(emoji);
  });
}

// Export for tests
module.exports = { analyzeMood };
