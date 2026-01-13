#!/usr/bin/env node
const fs = require('fs');

function analyzeMood(text) {
  const lower = text.toLowerCase();
  const moods = [
    {emoji: 'ð', keywords: ['happy', 'joy', 'love', 'great', 'awesome', 'fantastic', 'good', 'glad']},
    {emoji: 'ð', keywords: ['sad', 'terrible', 'bad', 'unhappy', 'depressed', 'down', 'miserable']},
    {emoji: 'ð ', keywords: ['angry', 'mad', 'furious', 'irate', 'annoyed', 'hate']},
    {emoji: 'ð¤©', keywords: ['excited', 'thrilled', 'amazing', 'awesome', 'wow', 'fantastic', 'marathon']}
  ];
  for (const mood of moods) {
    for (const kw of mood.keywords) {
      if (lower.includes(kw)) {
        return mood.emoji;
      }
    }
  }
  return 'ð¤';
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

module.exports = {analyzeMood};
