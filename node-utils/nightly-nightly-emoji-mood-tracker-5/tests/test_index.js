const assert = require('assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { addMood, getStats, MOOD_EMOJI } = require('../src/index');

// Create a temporary directory for isolated storage
const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'mood-test-'));
const tempFile = path.join(tempDir, 'log.json');

// Test adding a supported mood
addMood('happy', tempFile);
let log = JSON.parse(fs.readFileSync(tempFile, 'utf8'));
assert.strictEqual(log.length, 1);
assert.strictEqual(log[0].mood, 'happy');
assert.strictEqual(log[0].emoji, MOOD_EMOJI['happy']);

// Test stats aggregation
addMood('sad', tempFile);
addMood('happy', tempFile);
const stats = getStats(tempFile);
assert.deepStrictEqual(stats, { happy: 2, sad: 1 });

// Test unsupported mood throws
let threw = false;
try {
  addMood('confused', tempFile);
} catch (e) {
  threw = true;
}
assert.strictEqual(threw, true);

console.log('All tests passed.');
