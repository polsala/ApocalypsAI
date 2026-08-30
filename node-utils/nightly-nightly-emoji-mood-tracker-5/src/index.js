#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const os = require('os');

const DEFAULT_FILE = path.join(os.homedir(), '.emoji_mood_log.json');

const MOOD_EMOJI = {
  happy: '😊',
  sad: '😢',
  angry: '😠',
  excited: '🤩',
  neutral: '😐'
};

function loadLog(filePath = DEFAULT_FILE) {
  try {
    const data = fs.readFileSync(filePath, 'utf8');
    return JSON.parse(data);
  } catch (e) {
    return [];
  }
}

function saveLog(log, filePath = DEFAULT_FILE) {
  fs.writeFileSync(filePath, JSON.stringify(log, null, 2), 'utf8');
}

function addMood(mood, filePath = DEFAULT_FILE) {
  if (!MOOD_EMOJI[mood]) {
    throw new Error(`Unsupported mood: ${mood}`);
  }
  const log = loadLog(filePath);
  const entry = {
    timestamp: new Date().toISOString(),
    mood,
    emoji: MOOD_EMOJI[mood]
  };
  log.push(entry);
  saveLog(log, filePath);
  return entry;
}

function getStats(filePath = DEFAULT_FILE) {
  const log = loadLog(filePath);
  const stats = {};
  for (const entry of log) {
    stats[entry.mood] = (stats[entry.mood] || 0) + 1;
  }
  return stats;
}

// CLI handling
if (require.main === module) {
  const [,, cmd, arg] = process.argv;
  if (cmd === 'add' && arg) {
    try {
      const entry = addMood(arg);
      console.log(`Logged ${entry.mood} ${entry.emoji} at ${entry.timestamp}`);
    } catch (e) {
      console.error(e.message);
      process.exit(1);
    }
  } else if (cmd === 'stats') {
    const stats = getStats();
    console.log('Mood statistics:');
    for (const [mood, count] of Object.entries(stats)) {
      console.log(`${mood} (${MOOD_EMOJI[mood] || ''}): ${count}`);
    }
  } else {
    console.log('Usage: node src/index.js <add <mood>|stats>');
    process.exit(1);
  }
}

// Export for testing
module.exports = { addMood, getStats, MOOD_EMOJI };
