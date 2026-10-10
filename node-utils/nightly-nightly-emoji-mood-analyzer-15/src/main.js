#!/usr/bin/env node
const fs = require('fs');

const POSITIVE = ['love', 'happy', 'joy', 'great', 'good', 'awesome', 'fantastic', 'wonderful', 'excellent', 'sunny'];
const NEGATIVE = ['hate', 'sad', 'bad', 'terrible', 'awful', 'horrible', 'depressed', 'angry', 'pain', 'rainy'];

function analyzeMood(text) {
  const words = text.toLowerCase().match(/\b\w+\b/g) || [];
  let score = 0;
  for (const w of words) {
    if (POSITIVE.includes(w)) score++;
    if (NEGATIVE.includes(w)) score--;
  }
  if (score > 0) return '😊';
  if (score < 0) return '😢';
  return '😐';
}

// CLI mode
if (require.main === module) {
  // Read from stdin
  let input = '';
  process.stdin.setEncoding('utf8');
  process.stdin.on('data', chunk => input += chunk);
  process.stdin.on('end', () => {
    const result = analyzeMood(input.trim());
    console.log(result);
  });
} else {
  module.exports = { analyzeMood };
}
