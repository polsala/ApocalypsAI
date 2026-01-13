// Tests for emojiâmoodâtracker â deterministic and offline
// SPDXâLicenseâIdentifier: MIT

const assert = require('assert');
const fs = require('fs');
const os = require('os');
const path = require('path');

// Import the module under test
const tracker = require('../src/index.js');

// Use a temporary file to avoid polluting the real home directory
const tempFile = path.join(os.tmpdir(), `emoji_mood_test_${Date.now()}.json`);
process.env.EMOJI_MOOD_FILE = tempFile;

function cleanUp() {
  try { fs.unlinkSync(tempFile); } catch (_) {}
}

// Ensure clean state before each test
function reset() {
  cleanUp();
}

// Test 1 â logging creates an entry
reset();
const entry = tracker.logMood('ð', 'test note');
assert.strictEqual(entry.emoji, 'ð');
assert.strictEqual(entry.note, 'test note');
assert.ok(entry.timestamp);

// Test 2 â list returns the logged entry
const list = tracker.listMoods();
assert.strictEqual(list.length, 1);
assert.deepStrictEqual(list[0], entry);

// Test 3 â stats reflect the count
const stats = tracker.getStats();
assert.strictEqual(stats['ð'], 1);

// Test 4 â multiple logs aggregate correctly
tracker.logMood('ð¢');
tracker.logMood('ð');
const stats2 = tracker.getStats();
assert.strictEqual(stats2['ð'], 2);
assert.strictEqual(stats2['ð¢'], 1);

// Clean up after tests
cleanUp();
console.log('All tests passed');
