const assert = require('assert');
const fs = require('fs');
const os = require('os');
const path = require('path');

// Use a temporary file for isolation
const tempLog = path.join(os.tmpdir(), `emoji_mood_test_${Date.now()}.json`);
process.env.EMOJI_MOOD_LOG_PATH = tempLog;

// Import after setting the env var so the module picks up the temp path
const { addMood, listMoods, stats, LOG_PATH } = require('../src/index.js');

// Verify that the module is using our temporary path
assert.strictEqual(LOG_PATH, tempLog);

// Test adding moods
const entry1 = addMood('happy', '😊');
assert.strictEqual(entry1.mood, 'happy');
assert.strictEqual(entry1.emoji, '😊');

const entry2 = addMood('sad', '😢');
assert.strictEqual(entry2.mood, 'sad');
assert.strictEqual(entry2.emoji, '😢');

// Test listMoods returns both entries
const all = listMoods();
assert.strictEqual(all.length, 2);
assert.deepStrictEqual(all[0].mood, 'happy');
assert.deepStrictEqual(all[1].mood, 'sad');

// Test stats calculation
const s = stats();
assert.strictEqual(s.total, 2);
assert.deepStrictEqual(s.mostCommon, { mood: 'happy', count: 1 }); // tie resolved by first entry

// Clean up temporary file
fs.unlinkSync(tempLog);
console.log('All tests passed');
