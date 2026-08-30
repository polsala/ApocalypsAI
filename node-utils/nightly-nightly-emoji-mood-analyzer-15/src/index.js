#!/usr/bin/env node

function analyzeMood(text) {
  if (!text) return '🤔';
  const lower = text.toLowerCase();
  const moodMap = [
    { keywords: ['happy', 'joy', 'excited', 'glad', 'great', 'fantastic', 'awesome'], emoji: '😄' },
    { keywords: ['sad', 'down', 'unhappy', 'depressed', 'blue'], emoji: '😢' },
    { keywords: ['angry', 'mad', 'furious', 'irate'], emoji: '😠' },
    { keywords: ['scared', 'afraid', 'fearful', 'terrified'], emoji: '😱' },
    { keywords: ['love', 'loving', 'adore', 'cherish'], emoji: '❤️' }
  ];
  for (const entry of moodMap) {
    for (const kw of entry.keywords) {
      if (lower.includes(kw)) return entry.emoji;
    }
  }
  return '🤔';
}

// CLI mode
if (require.main === module) {
  const input = process.argv.slice(2).join(' ');
  const result = analyzeMood(input);
  console.log(result);
}

module.exports = { analyzeMood };
