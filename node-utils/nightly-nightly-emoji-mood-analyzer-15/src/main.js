// nightly-emoji-mood-analyzer
// Reads text from stdin or a command‑line argument and outputs an emoji representing the overall mood.

const fs = require('fs');
const path = require('path');

// Simple sentiment word lists
const POSITIVE_WORDS = [
  'love', 'happy', 'joy', 'awesome', 'great', 'fantastic', 'good', 'wonderful', 'sunny', 'delight', 'pleased', 'smile', 'laugh', 'cheer', 'glad'
];
const NEGATIVE_WORDS = [
  'hate', 'sad', 'angry', 'bad', 'terrible', 'awful', 'worst', 'pain', 'mad', 'furious', 'upset', 'depress', 'gloom', 'cry', 'sick'
];

function getInput() {
  // If an argument is provided, use it as the text
  if (process.argv.length > 2) {
    return process.argv.slice(2).join(' ');
  }
  // Otherwise, read from stdin synchronously
  try {
    const data = fs.readFileSync(0, 'utf8'); // 0 = STDIN
    return data.trim();
  } catch (e) {
    return '';
  }
}

function scoreSentiment(text) {
  const words = text.toLowerCase().split(/\W+/);
  let score = 0;
  for (const w of words) {
    if (POSITIVE_WORDS.includes(w)) score += 1;
    else if (NEGATIVE_WORDS.includes(w)) score -= 1;
  }
  return score;
}

function moodEmoji(score) {
  if (score > 0) return '😊';
  if (score < 0) return '😡';
  return '😐';
}

function main() {
  const input = getInput();
  const score = scoreSentiment(input);
  const emoji = moodEmoji(score);
  console.log(emoji);
}

if (require.main === module) {
  main();
}
