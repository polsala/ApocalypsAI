const fs = require('fs');
const path = require('path');
const os = require('os');
const assert = require('assert');

// Path to the JSON file that stores mood entries
function getLogPath() {
  const home = os.homedir();
  return path.join(home, '.moodlog.json');
}

// Load the log file, creating a default structure if it does not exist
function loadLog() {
  const logPath = getLogPath();
  try {
    const raw = fs.readFileSync(logPath, 'utf8');
    return JSON.parse(raw);
  } catch (e) {
    // If file does not exist or is malformed, start fresh
    return { entries: [] };
  }
}

// Persist the log object to disk
function saveLog(log) {
  const logPath = getLogPath();
  const data = JSON.stringify(log, null, 2);
  fs.writeFileSync(logPath, data, 'utf8');
}

/**
 * Add a mood entry for today.
 * @param {string} mood - The mood description (e.g., "happy").
 */
function addMood(mood) {
  assert(typeof mood === 'string' && mood.length > 0, 'Mood must be a non‑empty string');
  const log = loadLog();
  const today = new Date().toISOString().slice(0, 10); // YYYY‑MM‑DD
  log.entries.push({ date: today, mood });
  saveLog(log);
}

/**
 * Compute a simple count of each mood logged.
 * @returns {Object<string, number>} Mapping from mood to occurrence count.
 */
function getStats() {
  const log = loadLog();
  const counts = {};
  for (const entry of log.entries) {
    counts[entry.mood] = (counts[entry.mood] || 0) + 1;
  }
  return counts;
}

/**
 * Pretty‑print the stats to stdout.
 */
function printStats() {
  const stats = getStats();
  if (Object.keys(stats).length === 0) {
    console.log('No moods logged yet.');
    return;
  }
  console.log('Mood statistics:');
  for (const [mood, count] of Object.entries(stats)) {
    console.log(`- ${mood}: ${count}`);
  }
}

// CLI handling
if (require.main === module) {
  const args = process.argv.slice(2);
  const command = args[0];
  if (command === 'add' && args[1]) {
    addMood(args[1]);
    console.log(`Added mood "${args[1]}" for today.`);
  } else if (command === 'stats') {
    printStats();
  } else {
    console.error('Usage: node index.js add <mood> | stats');
    process.exit(1);
  }
}

module.exports = { addMood, getStats, getLogPath };
