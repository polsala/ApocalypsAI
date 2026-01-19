const fs = require('fs');
const path = require('path');

/**
 * Resolve the path to the JSON data file.
 * If a custom path is supplied (used by tests), honour it; otherwise store
 * the file next to the utility in the repository root.
 */
function getDataFilePath(dataFile) {
  return dataFile || path.join(__dirname, '..', 'mood_data.json');
}

function loadData(dataFile) {
  const filePath = getDataFilePath(dataFile);
  if (!fs.existsSync(filePath)) return [];
  const raw = fs.readFileSync(filePath, 'utf8');
  try {
    return JSON.parse(raw);
  } catch {
    // Corrupted file – start fresh
    return [];
  }
}

function saveData(entries, dataFile) {
  const filePath = getDataFilePath(dataFile);
  fs.writeFileSync(filePath, JSON.stringify(entries, null, 2), 'utf8');
}

/**
 * Add a mood entry.
 * @param {string} emoji - Emoji representing the mood.
 * @param {Date} [date] - Date of the entry (defaults to now).
 * @param {string} [dataFile] - Optional custom data‑file path (for testing).
 */
function addEntry(emoji, date = new Date(), dataFile) {
  if (typeof emoji !== 'string' || !emoji.trim()) {
    throw new Error('Emoji must be a non‑empty string');
  }
  const entries = loadData(dataFile);
  entries.push({ emoji, timestamp: date.toISOString() });
  saveData(entries, dataFile);
}

/**
 * Compute simple statistics.
 * @param {string} [dataFile] - Optional custom data‑file path.
 * @returns {{total:number, topEmoji:string|null}}
 */
function getStats(dataFile) {
  const entries = loadData(dataFile);
  const total = entries.length;
  if (total === 0) {
    return { total: 0, topEmoji: null };
  }
  const counts = {};
  for (const e of entries) {
    counts[e.emoji] = (counts[e.emoji] || 0) + 1;
  }
  const topEmoji = Object.entries(counts).reduce((best, cur) =>
    cur[1] > best[1] ? cur : best
  )[0];
  return { total, topEmoji };
}

/**
 * Simple command‑line interface.
 *   node src/index.js add 😊
 *   node src/index.js stats
 */
if (require.main === module) {
  const [, , command, arg] = process.argv;
  try {
    if (command === 'add' && arg) {
      addEntry(arg);
      console.log('Mood logged:', arg);
    } else if (command === 'stats') {
      const stats = getStats();
      console.log('Total entries:', stats.total);
      console.log('Most common emoji:', stats.topEmoji || 'N/A');
    } else {
      console.log('Usage: node src/index.js add <emoji> | stats');
    }
  } catch (e) {
    console.error('Error:', e.message);
    process.exit(1);
  }
}

module.exports = { addEntry, getStats };
