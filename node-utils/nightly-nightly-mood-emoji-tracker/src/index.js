const fs = require('fs');
const path = require('path');
const os = require('os');

function getDataFilePath() {
  const home = process.env.HOME || os.homedir();
  return path.join(home, '.mood_tracker.json');
}

function loadData() {
  const file = getDataFilePath();
  if (!fs.existsSync(file)) return [];
  const raw = fs.readFileSync(file, 'utf8');
  try {
    return JSON.parse(raw);
  } catch {
    return [];
  }
}

function saveData(data) {
  const file = getDataFilePath();
  fs.writeFileSync(file, JSON.stringify(data, null, 2), 'utf8');
}

/**
 * Add a mood entry.
 * @param {string} emoji
 * @param {string} note
 * @param {string} [date] ISO string for testing.
 */
function addEntry(emoji, note, date) {
  if (!emoji) throw new Error('emoji required');
  const entry = {
    date: date || new Date().toISOString(),
    emoji,
    note: note || ''
  };
  const data = loadData();
  data.push(entry);
  saveData(data);
}

/**
 * Get summary counts per emoji.
 * @returns {Object} mapping emoji -> count
 */
function getSummary() {
  const data = loadData();
  return data.reduce((acc, e) => {
    acc[e.emoji] = (acc[e.emoji] || 0) + 1;
    return acc;
  }, {});
}

// CLI handling
if (require.main === module) {
  const [, , cmd, ...args] = process.argv;
  if (cmd === 'add') {
    const [emoji, ...noteParts] = args;
    const note = noteParts.join(' ');
    try {
      addEntry(emoji, note);
      console.log('Mood recorded.');
    } catch (err) {
      console.error('Error:', err.message);
      process.exit(1);
    }
  } else if (cmd === 'summary') {
    console.log(JSON.stringify(getSummary(), null, 2));
  } else {
    console.error('Usage: node src/index.js add <emoji> <note>');
    console.error('       node src/index.js summary');
    process.exit(1);
  }
}

module.exports = { addEntry, getSummary, loadData, saveData };
