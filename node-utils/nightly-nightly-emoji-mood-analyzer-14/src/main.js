#!/usr/bin/env node
/**
 * nightly-emoji-mood-analyzer
 * Analyze a short text and return an emoji representing the mood.
 */

function analyzeMood(text) {
  if (!text) return '🤔';
  const lower = text.toLowerCase();
  const moods = [
    { keywords: ['happy', 'joy', 'glad', 'excited', 'great', 'fantastic', 'awesome'], emoji: '😊' },
    { keywords: ['sad', 'down', 'unhappy', 'depressed', 'blue'], emoji: '😢' },
    { keywords: ['angry', 'mad', 'furious', 'irate'], emoji: '😠' },
    { keywords: ['love', 'loving', 'adore', 'cherish', 'heart'], emoji: '❤️' },
    { keywords: ['scared', 'fear', 'afraid', 'terrified', 'frightened'], emoji: '😨' },
    { keywords: ['surprised', 'wow', 'amazed', 'astonished', 'shocked'], emoji: '😲' },
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
  const args = process.argv.slice(2);
  if (args.length > 0) {
    console.log(analyzeMood(args.join(' ')));
  } else {
    // read from stdin
    let data = '';
    process.stdin.setEncoding('utf8');
    process.stdin.on('data', chunk => data += chunk);
    process.stdin.on('end', () => {
      console.log(analyzeMood(data.trim()));
    });
  }
}

module.exports = { analyzeMood };
