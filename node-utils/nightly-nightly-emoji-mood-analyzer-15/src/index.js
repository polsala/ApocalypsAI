#!/usr/bin/env node
const fs = require('fs');

function analyzeMood(text) {
  const lower = text.toLowerCase();
  const moods = [
    { keywords: ['happy', 'joy', 'glad', 'great', 'awesome', 'fantastic', 'good', 'love', 'excited', 'celebrate', 'win'], emoji: '😊' },
    { keywords: ['sad', 'unhappy', 'down', 'depressed', 'cry', 'tears', 'sorrow'], emoji: '😢' },
    { keywords: ['angry', 'mad', 'furious', 'irate', 'annoyed', 'hate'], emoji: '😠' },
    { keywords: ['surprised', 'shocked', 'wow', 'amazed', 'astonished'], emoji: '😲' },
    { keywords: ['fear', 'scared', 'afraid', 'terrified', 'panic'], emoji: '😨' },
    { keywords: ['tired', 'exhausted', 'sleepy', 'sleep', 'nap'], emoji: '😴' },
    { keywords: ['love', 'heart', 'romantic', 'cupid'], emoji: '❤️' },
    { keywords: ['run', 'marathon', 'jog', 'race'], emoji: '🏃‍♂️' }
  ];
  for (const mood of moods) {
    for (const kw of mood.keywords) {
      if (lower.includes(kw)) {
        return mood.emoji;
      }
    }
  }
  return '🤔';
}

// CLI handling
if (require.main === module) {
  const input = process.argv.slice(2).join(' ');
  if (!input) {
    console.error('Usage: emoji-mood "your text here"');
    process.exit(1);
  }
  const result = analyzeMood(input);
  console.log(result);
}

// Export for tests
module.exports = { analyzeMood };
