#!/usr/bin/env node
const fs = require('fs');

const moodMap = {
  happy: { keywords: ['happy','joy','excited','glad','delighted','pleased','cheer','smile','laugh'], emoji: '😄' },
  sad: { keywords: ['sad','unhappy','down','depressed','cry','tears','sorrow','gloom','melancholy'], emoji: '😢' },
  angry: { keywords: ['angry','mad','furious','irritated','annoyed','rage','hate','upset'], emoji: '😠' },
  neutral: { keywords: [], emoji: '🤔' }
};

function analyzeMood(text) {
  const lower = text.toLowerCase();
  const scores = { happy: 0, sad: 0, angry: 0 };
  for (const mood of Object.keys(scores)) {
    const { keywords } = moodMap[mood];
    for (const kw of keywords) {
      const regex = new RegExp('\\b' + kw + '\\b', 'g');
      const matches = lower.match(regex);
      if (matches) scores[mood] += matches.length;
    }
  }
  const maxMood = Object.entries(scores).reduce((a, [m, s]) => s > a[1] ? [m, s] : a, ['neutral', 0]);
  return moodMap[maxMood[0]].emoji;
}

// CLI entry point
if (require.main === module) {
  const args = process.argv.slice(2);
  let input = args.join(' ');
  if (!input && !process.stdin.isTTY) {
    input = fs.readFileSync(0, 'utf8');
  }
  if (!input) {
    console.error('Usage: node src/index.js <text> or pipe text via stdin');
    process.exit(1);
  }
  console.log(analyzeMood(input));
}

module.exports = { analyzeMood };
