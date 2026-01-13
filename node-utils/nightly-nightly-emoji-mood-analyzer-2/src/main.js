// nightly-emoji-mood-analyzer
// Reads stdin, evaluates simple sentiment, and prints an emoji.

const fs = require('fs');

// Simple lexicon
const POSITIVE = [
  'happy', 'joy', 'love', 'thrilled', 'excited', 'great', 'good', 'awesome', 'fantastic'
];
const NEGATIVE = [
  'sad', 'angry', 'bad', 'terrible', 'hate', 'upset', 'depressed', 'worried', 'annoyed'
];

function sentimentScore(text) {
  const words = text.toLowerCase().split(/\W+/);
  let score = 0;
  for (const w of words) {
    if (POSITIVE.includes(w)) score++;
    if (NEGATIVE.includes(w)) score--;
  }
  return score;
}

function emojiForScore(score) {
  if (score > 1) return 'ð'; // strong positive
  if (score > 0) return 'ð'; // mild positive
  if (score < -1) return 'ð'; // strong negative
  if (score < 0) return 'ð'; // mild negative
  return 'ð'; // neutral
}

function main() {
  const input = fs.readFileSync(0, 'utf8'); // stdin
  const score = sentimentScore(input);
  const emoji = emojiForScore(score);
  process.stdout.write(emoji + '
');
}

main();

