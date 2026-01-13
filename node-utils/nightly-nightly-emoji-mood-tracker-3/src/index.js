const fs = require('fs');
const path = require('path');

// Resolve storage file â default to ./mood.json in cwd
function getStoragePath() {
  return process.env.MOOD_FILE || path.resolve(process.cwd(), 'mood.json');
}

async function readData() {
  const file = getStoragePath();
  try {
    const raw = await fs.promises.readFile(file, 'utf-8');
    return JSON.parse(raw);
  } catch (err) {
    // If file does not exist or is malformed, start fresh
    return [];// # Mock rationale: start with empty array on any read error
  }
}

async function writeData(data) {
  const file = getStoragePath();
  const dir = path.dirname(file);
  await fs.promises.mkdir(dir, { recursive: true });
  await fs.promises.writeFile(file, JSON.stringify(data, null, 2), 'utf-8');
}

/**
 * Log a mood entry.
 * @param {string} emoji - The emoji representing the mood.
 * @param {string} [note] - Optional freeâform note.
 */
async function logMood(emoji, note) {
  if (!emoji) {
    throw new Error('Emoji is required');
  }
  const data = await readData();
  data.push({
    timestamp: new Date().toISOString(),
    emoji,
    note: note || ''
  });
  await writeData(data);
}

/**
 * Get a summary count of each emoji used.
 * @returns {Promise<Object>} Mapping emoji => count
 */
async function getSummary() {
  const data = await readData();
  const summary = {};
  for (const entry of data) {
    summary[entry.emoji] = (summary[entry.emoji] || 0) + 1;
  }
  return summary;
}

// CLI handling
async function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  if (command === 'log') {
    const emoji = args[1];
    const note = args.slice(2).join(' ');
    try {
      await logMood(emoji, note);
      console.log(`Logged mood ${emoji}` + (note ? `: ${note}` : ''));
    } catch (e) {
      console.error('Error:', e.message);
      process.exit(1);
    }
  } else if (command === 'summary') {
    const summary = await getSummary();
    console.log('Mood summary:');
    for (const [emoji, count] of Object.entries(summary)) {
      console.log(`${emoji}: ${count}`);
    }
  } else {
    console.error('Usage: node src/index.js <log|summary> [args]');
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { logMood, getSummary };
