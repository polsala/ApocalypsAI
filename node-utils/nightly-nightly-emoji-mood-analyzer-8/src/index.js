#!/usr/bin/env node
const fs = require('fs');

function analyzeMood(text) {
  const lower = text.toLowerCase();
  const moods = [
    { keywords: ['happy','joy','glad','thrill','excited','delight','love','ð','smile'], emoji: 'ð' },
    { keywords: ['sad','unhappy','down','depressed','cry','tears','ð­','ð¢'], emoji: 'ð¢' },
    { keywords: ['angry','mad','furious','irate','hate','rage','ð¡','ð '], emoji: 'ð ' },
    { keywords: ['fear','scared','afraid','terrified','panic','ð±','ð¨'], emoji: 'ð±' },
    { keywords: ['surprise','shocked','wow','astonished','amazed','ð²','ð¤¯'], emoji: 'ð²' }
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

// CLI
if (require.main === module) {
  const input = process.argv.slice(2).join(' ') || fs.readFileSync(0, 'utf8');
  const result = analyzeMood(input.trim());
  console.log(result);
}

module.exports = { analyzeMood };
