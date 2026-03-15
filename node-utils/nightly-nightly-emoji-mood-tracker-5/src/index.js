#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const os = require('os');

function getDataFile() {
  return process.env.EMOJI_MOOD_FILE || path.join(os.homedir(), '.emoji_mood_tracker.json');
}

function loadData() {
  const file = getDataFile();
  if (!fs.existsSync(file)) return [];
  const raw = fs.readFileSync(file, 'utf8');
  try {
    return JSON.parse(raw);
  } catch {
    return [];
  }
}

function saveData(data) {
  const file = getDataFile();
  fs.writeFileSync(file, JSON.stringify(data, null, 2), 'utf8');
}

function addEntry(emoji, note) {
  const data = loadData();
  data.push({ emoji, note, timestamp: new Date().toISOString() });
  saveData(data);
  console.log('Entry added.');
}

function listEntries() {
  const data = loadData();
  if (data.length === 0) {
    console.log('No entries.');
    return;
  }
  data.forEach((e, i) => {
    console.log(`${i + 1}. ${e.timestamp} ${e.emoji} - ${e.note}`);
  });
}

function summary() {
  const data = loadData();
  const counts = {};
  data.forEach(e => {
    counts[e.emoji] = (counts[e.emoji] || 0) + 1;
  });
  if (Object.keys(counts).length === 0) {
    console.log('No entries.');
    return;
  }
  console.log('Mood summary:');
  for (const [emoji, cnt] of Object.entries(counts)) {
    console.log(`${emoji}: ${cnt}`);
  }
}

function printHelp() {
  console.log('Usage: emoji-mood <command> [args]');
  console.log('Commands:');
  console.log('  add <emoji> <note>   Add a mood entry');
  console.log('  list                 List all entries');
  console.log('  summary              Show emoji counts');
  console.log('  help                 Show this help');
}

function main() {
  const args = process.argv.slice(2);
  const cmd = args[0];
  switch (cmd) {
    case 'add':
      if (args.length < 3) {
        console.error('add requires <emoji> and <note>');
        process.exit(1);
      }
      const emoji = args[1];
      const note = args.slice(2).join(' ');
      addEntry(emoji, note);
      break;
    case 'list':
      listEntries();
      break;
    case 'summary':
      summary();
      break;
    case 'help':
    case undefined:
      printHelp();
      break;
    default:
      console.error(`Unknown command: ${cmd}`);
      printHelp();
      process.exit(1);
  }
}

if (require.main === module) {
  main();
}
