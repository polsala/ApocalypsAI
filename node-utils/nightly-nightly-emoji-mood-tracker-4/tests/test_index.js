const assert = require('assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { addEntry, getStats } = require('../src/index');

/**
 * Helper that creates a temporary directory, runs a callback with a path to a
 * fresh JSON file, and then cleans up. All file‑system interactions stay inside
 * the temp folder, making the test deterministic and offline.
 */
function withTempFile(fn) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'mood-'));
  const file = path.join(dir, 'data.json');
  try {
    fn(file);
  } finally {
    // Remove the temporary directory recursively.
    fs.rmSync(dir, { recursive: true, force: true });
  }
}

// Test: single entry should be recorded correctly.
withTempFile((dataFile) => {
  addEntry('😊', new Date('2023-01-01T12:00:00Z'), dataFile);
  const stats = getStats(dataFile);
  assert.strictEqual(stats.total, 1);
  assert.strictEqual(stats.topEmoji, '😊');
});

// Test: multiple entries and most‑common emoji calculation.
withTempFile((dataFile) => {
  addEntry('😊', new Date('2023-01-01T12:00:00Z'), dataFile);
  addEntry('😢', new Date('2023-01-02T12:00:00Z'), dataFile);
  addEntry('😊', new Date('2023-01-03T12:00:00Z'), dataFile);
  const stats = getStats(dataFile);
  assert.strictEqual(stats.total, 3);
  assert.strictEqual(stats.topEmoji, '😊');
});

console.log('All tests passed');
