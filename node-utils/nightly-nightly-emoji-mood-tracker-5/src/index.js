const fs = require('fs');
const path = require('path');
const os = require('os');
const assert = require('assert');

// Helper to locate the data file. Allows override via ENV for testing.
function getDataFilePath() {
  const customPath = process.env.EMOJI_MOOD_DATA_PATH;
  if (customPath) return customPath;
  return path.join(os.homedir(), '.emoji_mood_tracker.json');
}

function loadData() {
  const filePath = getDataFilePath();
  try {
    const raw = fs.readFileSync(filePath, 'utf8');
    return JSON.parse(raw);
  } catch (e) {
    // If file doesn't exist or is malformed, start fresh.
    return [];
  }
}

function saveData(data) {
  const filePath = getDataFilePath();
  const dir = path.dirname(filePath);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf8');
}

function addEntry(emoji, note = '') {
  assert(typeof emoji === 'string' && emoji.length > 0, 'Emoji must be a non‑empty string');
  const entry = {
    timestamp: new Date().toISOString(),
    emoji,
    note,
  };
  const data = loadData();
  data.push(entry);
  saveData(data);
  console.log('Added entry:', entry);
}

function getStats() {
  const data = loadData();
  const counts = {};
  data.forEach(e => {
    counts[e.emoji] = (counts[e.emoji] || 0) + 1;
  });
  return counts;
}

function listEntries(limit = 10) {
  const data = loadData();
  const recent = data.slice(-limit).reverse();
  return recent;
}

function printStats() {
  const stats = getStats();
  if (Object.keys(stats).length === 0) {
    console.log('No entries recorded yet.');
    return;
  }
  console.log('Mood statistics:');
  for (const [emoji, count] of Object.entries(stats)) {
    console.log(`${emoji}\t${count}`);
  }
}

function printList(limit) {
  const entries = listEntries(limit);
  if (entries.length === 0) {
    console.log('No entries to show.');
    return;
  }
  entries.forEach(e => {
    const notePart = e.note ? ` – ${e.note}` : '';
    console.log(`[${e.timestamp}] ${e.emoji}${notePart}`);
  });
}

function showHelp() {
  console.log('Usage:');
  console.log('  node src/index.js add <emoji> [note]   Add a mood entry');
  console.log('  node src/index.js stats                Show emoji counts');
  console.log('  node src/index.js list [limit]         List recent entries (default 10)');
  console.log('  node src/index.js help                 Show this help');
}

function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  switch (command) {
    case 'add':
      const emoji = args[1];
      const note = args.slice(2).join(' ');
      if (!emoji) {
        console.error('Error: Emoji is required for add command.');
        process.exit(1);
      }
      addEntry(emoji, note);
      break;
    case 'stats':
      printStats();
      break;
    case 'list':
      const limit = args[1] ? parseInt(args[1], 10) : 10;
      printList(limit);
      break;
    case 'help':
    case undefined:
      showHelp();
      break;
    default:
      console.error(`Unknown command: ${command}`);
      showHelp();
      process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = {
  getDataFilePath,
  loadData,
  saveData,
  addEntry,
  getStats,
  listEntries,
};
