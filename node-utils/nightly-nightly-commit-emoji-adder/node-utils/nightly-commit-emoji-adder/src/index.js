#!/usr/bin/env node

/**
 * nightly-commit-emoji-adder
 * --------------------------
 * Reads a commit message (argument or stdin) and appends emojis based on detected keywords.
 */

const fs = require('fs');
const path = require('path');

// Mapping of keywords (lower‑case) to emojis. Multiple emojis per keyword are allowed.
const keywordMap = {
  fix: ['🛠️', '🐛'],
  bug: ['🛠️', '🐛'],
  add: ['➕'],
  remove: ['❌'],
  update: ['🔄'],
  docs: ['📚'],
  doc: ['📚'],
  test: ['✅'],
  refactor: ['♻️'],
  chore: ['🧹']
};

/**
 * Extract emojis for a given message.
 * @param {string} message
 * @returns {string[]} array of unique emojis
 */
function extractEmojis(message) {
  const found = new Set();
  const words = message.toLowerCase().split(/\s+/);
  for (const word of words) {
    if (keywordMap[word]) {
      for (const emoji of keywordMap[word]) {
        found.add(emoji);
      }
    }
  }
  return Array.from(found);
}

/**
 * Main function – reads input, processes, and writes output.
 */
function main() {
  // If arguments are provided after the script name, treat them as the message.
  const args = process.argv.slice(2);
  if (args.length > 0) {
    const message = args.join(' ');
    outputWithEmojis(message);
    return;
  }

  // Otherwise, read from stdin.
  let data = '';
  process.stdin.setEncoding('utf8');
  process.stdin.on('data', chunk => (data += chunk));
  process.stdin.on('end', () => {
    const message = data.trim();
    if (message.length === 0) {
      // No input – print usage hint.
      console.error('Usage: nightly-commit-emoji-adder "commit message"');
      process.exit(1);
    }
    outputWithEmojis(message);
  });
}

function outputWithEmojis(message) {
  const emojis = extractEmojis(message);
  const result = emojis.length ? `${message} ${emojis.join(' ')}` : message;
  console.log(result);
}

if (require.main === module) {
  main();
}

module.exports = { extractEmojis, outputWithEmojis };
