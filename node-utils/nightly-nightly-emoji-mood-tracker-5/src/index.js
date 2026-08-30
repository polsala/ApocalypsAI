#!/usr/bin/env node

/**
 * nightly-emoji-mood-tracker
 *
 * A simple CLI for logging moods with emojis and viewing statistics.
 * No external dependencies – uses only the Node.js standard library.
 */

const fs = require('fs');
const path = require('path');

// Resolve the data file location. Allows overriding via env var for testing.
const DATA_FILE = process.env.DATA_FILE || path.join(process.cwd(), 'mood_data.json');

// Helper: load existing entries or start with an empty array.
function loadData() {
  try {
    const raw = fs.readFileSync(DATA_FILE, 'utf8');
    return JSON.parse(raw);
  } catch (e) {
    // If file does not exist or is malformed, start fresh.
    return [];
  }
}

// Helper: persist entries to disk.
function saveData(entries) {
  const json = JSON.stringify(entries, null, 2);
  fs.writeFileSync(DATA_FILE, json, 'utf8');
}

// Command: add <emoji> <note> [--timestamp <ms>]
function cmdAdd(args) {
  if (args.length < 2) {
    console.error('Usage: add <emoji> <note> [--timestamp <ms>]');
    process.exit(1);
  }
  const emoji = args[0];
  const note = args[1];
  let timestamp = Date.now();
  // Optional flag handling
  if (args[2] === '--timestamp' && args[3]) {
    const ts = Number(args[3]);
    if (!isNaN(ts)) {
      timestamp = ts;
    }
  }
  const entries = loadData();
  entries.push({ timestamp, emoji, note });
  saveData(entries);
  console.log('Logged mood.');
}

// Command: stats
function cmdStats() {
  const entries = loadData();
  if (entries.length === 0) {
    console.log('No entries.');
    return;
  }
  const counts = {};
  for (const e of entries) {
    counts[e.emoji] = (counts[e.emoji] || 0) + 1;
  }
  const lines = Object.entries(counts)
    .map(([emoji, cnt]) => `${emoji}: ${cnt}`)
    .join('\n');
  console.log(lines);
}

function printHelp() {
  console.log('nightly-emoji-mood-tracker');
  console.log('Commands:');
  console.log('  add <emoji> <note> [--timestamp <ms>]   Log a new mood entry');
  console.log('  stats                                   Show emoji usage statistics');
}

function main() {
  const [, , command, ...rest] = process.argv;
  if (!command) {
    printHelp();
    process.exit(0);
  }
  switch (command) {
    case 'add':
      cmdAdd(rest);
      break;
    case 'stats':
      cmdStats();
      break;
    case 'help':
    case '--help':
    case '-h':
      printHelp();
      break;
    default:
      console.error(`Unknown command: ${command}`);
      printHelp();
      process.exit(1);
  }
}

if (require.main === module) {
  main();
}
