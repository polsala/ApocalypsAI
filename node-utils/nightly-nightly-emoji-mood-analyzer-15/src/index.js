#!/usr/bin/env node
const fs = require('fs');

function analyzeMood(text) {
  const categories = {
    happy: {words: ['love','joy','happy','great','awesome','fantastic','good','wonderful','delight','pleased','glad'], emoji: '😊'},
    sad: {words: ['sad','bad','terrible','unhappy','depressed','down','gloom','sorrow','cry','crying','miserable'], emoji: '😢'},
    angry: {words: ['angry','mad','furious','hate','annoyed','irritated','rage','outraged','disgust','resentful'], emoji: '😠'},
    surprised: {words: ['surprised','shocked','amazed','astonished','wow','unbelievable','unexpected'], emoji: '😲'}
  };
  const scores = {happy:0,sad:0,angry:0,surprised:0};
  const tokens = text.toLowerCase().split(/\W+/);
  for (const token of tokens) {
    for (const cat in categories) {
      if (categories[cat].words.includes(token)) {
        scores[cat] += 1;
      }
    }
  }
  let bestCat = null;
  let bestScore = 0;
  for (const cat in scores) {
    if (scores[cat] > bestScore) {
      bestScore = scores[cat];
      bestCat = cat;
    }
  }
  if (bestScore === 0) return '😐';
  return categories[bestCat].emoji;
}

// CLI handling
if (require.main === module) {
  const input = process.argv.slice(2).join(' ');
  if (!input) {
    console.error('Usage: node src/index.js "your text here"');
    process.exit(1);
  }
  const emoji = analyzeMood(input);
  console.log(emoji);
}

// Export for testing
module.exports = {analyzeMood};
