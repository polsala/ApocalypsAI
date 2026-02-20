#!/usr/bin/env node
const fs = require('fs');

const positiveWords = ['love', 'happy', 'joy', 'great', 'good', 'awesome', 'fantastic', 'wonderful', 'excellent', 'sunny'];
const negativeWords = ['hate', 'sad', 'bad', 'terrible', 'awful', 'worst', 'depressed', 'angry', 'pain', 'rainy'];

function analyzeMood(text) {
  const words = text.toLowerCase().match(/\b\w+\b/g) || [];
  let pos = 0, neg = 0;
  for (const w of words) {
    if (positiveWords.includes(w)) pos++;
    if (negativeWords.includes(w)) neg++;
  }
  if (pos > neg) return '😊';
  if (neg > pos) return '😢';
  return '😐';
}

// CLI mode
if (require.main === module) {
  let input = '';
  if (process.argv.length > 2) {
    input = process.argv.slice(2).join(' ');
    console.log(analyzeMood(input));
  } else {
    // read from stdin
    process.stdin.setEncoding('utf8');
    process.stdin.on('data', chunk => { input += chunk; });
    process.stdin.on('end', () => {
      console.log(analyzeMood(input.trim()));
    });
  }
}

// Export for testing
module.exports = { analyzeMood };
