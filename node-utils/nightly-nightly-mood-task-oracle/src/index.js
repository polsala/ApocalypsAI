#!/usr/bin/env node
const { getTaskSuggestion } = require('./task-oracle');

function parseArgs(args) {
  const result = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--')) {
      const key = args[i].substring(2);
      if (key === 'mood' && i + 1 < args.length && !args[i+1].startsWith('--')) {
        result[key] = args[i+1];
        i++; // Consume the next argument as value
      } else if (key === 'random') {
        result[key] = true;
      }
    }
  }
  return result;
}

const args = parseArgs(process.argv.slice(2));
const mood = args.mood;
const random = args.random;

let suggestion;
if (random) {
  suggestion = getTaskSuggestion(); // No specific mood, let it pick randomly
} else {
  suggestion = getTaskSuggestion(mood);
}

console.log(`\n✨ ApocalypsAI's Oracle for your ${suggestion.mood} mood:`);
console.log(`   "${suggestion.task}"\n`);
