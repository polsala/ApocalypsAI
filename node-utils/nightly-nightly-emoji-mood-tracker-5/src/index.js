const fs = require('fs');
const os = require('os');
const path = require('path');

// Path to the hidden JSON log in the user's home directory
function getLogPath() {
  return path.join(os.homedir(), '.emoji_mood_log.json');
}

function loadLog() {
  const logPath = getLogPath();
  try {
    const raw = fs.readFileSync(logPath, 'utf8');
    return JSON.parse(raw);
  } catch (e) {
    // If file does not exist or is malformed, start fresh
    return [];
  }
}

function saveLog(entries) {
  const logPath = getLogPath();
  fs.writeFileSync(logPath, JSON.stringify(entries, null, 2), 'utf8');
}

function addMood(emoji) {
  if (!emoji) {
    console.error('Please provide an emoji to log.');
    process.exit(1);
  }
  const entries = loadLog();
  entries.push({ date: new Date().toISOString(), mood: emoji });
  saveLog(entries);
  console.log(`Logged mood ${emoji}`);
}

function showStats() {
  const entries = loadLog();
  if (entries.length === 0) {
    console.log('No moods logged yet.');
    return;
  }
  const counts = {};
  for (const e of entries) {
    counts[e.mood] = (counts[e.mood] || 0) + 1;
  }
  console.log('Mood statistics:');
  for (const [mood, cnt] of Object.entries(counts)) {
    console.log(`${mood}: ${cnt}`);
  }
}

// CLI handling – only executed when run directly
if (require.main === module) {
  const [, , command, arg] = process.argv;
  switch (command) {
    case 'add':
      addMood(arg);
      break;
    case 'stats':
      showStats();
      break;
    default:
      console.error('Usage: node index.js <add|stats> [emoji]');
      process.exit(1);
  }
}

module.exports = { addMood, showStats, getLogPath };
