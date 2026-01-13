// emojiâmoodâtracker â record moods with emojis
// SPDXâLicenseâIdentifier: MIT

const fs = require('fs');
const path = require('path');

// Resolve storage file â env var overrides default
function getStoragePath() {
  const envPath = process.env.EMOJI_MOOD_FILE;
  if (envPath) return envPath;
  const home = process.env.HOME || process.env.USERPROFILE;
  return path.join(home, '.emoji_mood_tracker.json');
}

function loadData() {
  const file = getStoragePath();
  try {
    const raw = fs.readFileSync(file, 'utf8');
    return JSON.parse(raw);
  } catch (e) {
    // If file does not exist or is malformed, start fresh
    return [];// Mock rationale: start with empty array on any read error
  }
}

function saveData(data) {
  const file = getStoragePath();
  fs.writeFileSync(file, JSON.stringify(data, null, 2), 'utf8');
}

/**
 * Record a new mood entry.
 * @param {string} emoji â single emoji character
 * @param {string} note â optional freeâform note
 */
function logMood(emoji, note = '') {
  if (!emoji) throw new Error('Emoji is required');
  const entry = {
    timestamp: new Date().toISOString(),
    emoji,
    note
  };
  const data = loadData();
  data.push(entry);
  saveData(data);
  return entry;
}

/** Return all entries sorted by timestamp */
function listMoods() {
  const data = loadData();
  return data.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
}

/** Return a map of emoji â count */
function getStats() {
  const data = loadData();
  const stats = {};
  for (const e of data) {
    stats[e.emoji] = (stats[e.emoji] || 0) + 1;
  }
  return stats;
}

// CLI handling
if (require.main === module) {
  const [, , cmd, ...args] = process.argv;
  try {
    switch (cmd) {
      case 'log':
        const [emoji, ...noteParts] = args;
        const note = noteParts.join(' ');
        const entry = logMood(emoji, note);
        console.log('Logged:', entry);
        break;
      case 'list':
        const list = listMoods();
        list.forEach(e => {
          console.log(`${e.timestamp}	${e.emoji}	${e.note}`);
        });
        break;
      case 'stats':
        const stats = getStats();
        console.log('Mood statistics:');
        for (const [emoji, count] of Object.entries(stats)) {
          console.log(`${emoji}	${count}`);
        }
        break;
      default:
        console.error('Unknown command. Use log|list|stats');
        process.exit(1);
    }
  } catch (err) {
    console.error('Error:', err.message);
    process.exit(1);
  }
}

module.exports = { logMood, listMoods, getStats, getStoragePath };
