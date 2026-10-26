#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const os = require('os');

const LOG_PATH = process.env.EMOJI_MOOD_LOG_PATH || path.join(os.homedir(), '.emoji_mood_log.json');

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

function addMood(mood, emoji) {
  if (!mood || !emoji) {
    throw new Error('Both mood and emoji are required');
  }
  const entries = loadLog();
  const entry = { mood, emoji, timestamp: new Date().toISOString() };
  entries.push(entry);
  saveLog(entries);
  return entry;
}

function listMoods() {
  return loadLog();
}

function stats() {
  const entries = loadLog();
  const total = entries.length;
  const counts = {};
  entries.forEach(e => {
    counts[e.mood] = (counts[e.mood] || 0) + 1;
  });
  const mostCommon = Object.entries(counts)
    .sort((a, b) => b[1] - a[1])
    .shift();
  return {
    total,
    mostCommon: mostCommon ? { mood: mostCommon[0], count: mostCommon[1] } : null,
  };
}

// CLI handling
if (require.main === module) {
  const [cmd, ...args] = process.argv.slice(2);
  try {
    switch (cmd) {
      case 'add':
        const [mood, emoji] = args;
        const entry = addMood(mood, emoji);
        console.log('Added:', entry);
        break;
      case 'list':
        console.log(listMoods());
        break;
      case 'stats':
        console.log(stats());
        break;
      default:
        console.error('Unknown command. Use add|list|stats');
        process.exit(1);
    }
  } catch (err) {
    console.error('Error:', err.message);
    process.exit(1);
  }
}

module.exports = { addMood, listMoods, stats, LOG_PATH };
