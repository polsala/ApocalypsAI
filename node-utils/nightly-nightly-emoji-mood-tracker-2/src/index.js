#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const os = require('os');

const LOG_PATH = path.join(os.homedir(), '.emoji_mood_log.json');

function loadLog() {
  try {
    const data = fs.readFileSync(LOG_PATH, 'utf8');
    return JSON.parse(data);
  } catch (e) {
    return [];
  }
}

function saveLog(entries) {
  fs.writeFileSync(LOG_PATH, JSON.stringify(entries, null, 2), 'utf8');
}

/**
 * Log a mood entry.
 * @param {string} emoji - Emoji representing the mood.
 * @param {string} note - Optional note.
 */
function logMood(emoji, note = '') {
  if (!emoji) {
    throw new Error('Emoji is required');
  }
  const entries = loadLog();
  entries.push({ emoji, note, timestamp: new Date().toISOString() });
  saveLog(entries);
}

/**
 * Get mood statistics as a map from emoji to count.
 * @returns {Object} stats
 */
function getStats() {
  const entries = loadLog();
  const stats = {};
  for (const e of entries) {
    stats[e.emoji] = (stats[e.emoji] || 0) + 1;
  }
  return stats;
}

// CLI handling
if (require.main === module) {
  const [, , command, ...args] = process.argv;
  try {
    if (command === 'log') {
      const [emoji, ...noteParts] = args;
      const note = noteParts.join(' ');
      logMood(emoji, note);
      console.log('Mood logged.');
    } else if (command === 'stats') {
      const stats = getStats();
      console.log('Mood stats:');
      for (const [emoji, count] of Object.entries(stats)) {
        console.log(`${emoji}: ${count}`);
      }
    } else {
      console.error('Unknown command. Use "log" or "stats".');
      process.exit(1);
    }
  } catch (err) {
    console.error('Error:', err.message);
    process.exit(1);
  }
}

module.exports = { logMood, getStats, LOG_PATH };
