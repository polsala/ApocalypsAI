// nightly-emoji-mood-analyzer
// Reads a line from stdin and prints an emoji representing the overall mood.

const readline = require('readline');

// Simple sentiment word lists (feel free to extend)
const POSITIVE_WORDS = [
  'love', 'happy', 'joy', 'awesome', 'great', 'fantastic', 'good', 'wonderful', 'excellent', 'sunny', 'delight', 'pleased', 'cheer', 'smile'
];
const NEGATIVE_WORDS = [
  'hate', 'sad', 'angry', 'bad', 'terrible', 'awful', 'horrible', 'pain', 'depress', 'rainy', 'storm', 'upset', 'cry', 'sick'
];

function sentimentScore(text) {
  const words = text.toLowerCase().split(/\s+/);
  let pos = 0;
  let neg = 0;
  for (const w of words) {
    if (POSITIVE_WORDS.includes(w)) pos++;
    if (NEGATIVE_WORDS.includes(w)) neg++;
  }
  return { pos, neg };
}

function chooseEmoji({ pos, neg }) {
  if (pos > neg) return 'ð';
  if (neg > pos) return 'ð¢';
  return 'ð';
}

function analyzeAndPrint(line) {
  const score = sentimentScore(line);
  const emoji = chooseEmoji(score);
  console.log(emoji);
}

// Read from stdin (supports piped input or interactive)
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  terminal: false
});

let collected = '';// accumulate all data (in case of multiâline)
rl.on('line', (line) => {
  if (collected) collected += ' ';
  collected += line;
});

rl.on('close', () => {
  if (collected.trim().length === 0) {
    // No input provided
    console.error('No input received. Provide text via stdin.');
    process.exit(1);
  }
  analyzeAndPrint(collected.trim());
});

