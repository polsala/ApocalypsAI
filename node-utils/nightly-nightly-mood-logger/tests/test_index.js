const fs = require('fs');
const os = require('os');
const path = require('path');
const assert = require('assert');

// Import the library functions
const { addMood, getStats, getLogPath } = require('../src/index.js');

// Helper: create a temporary HOME directory for isolation
function withTempHome(callback) {
  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'moodlog-test-'));
  const originalHome = process.env.HOME;
  process.env.HOME = tmpDir; // Override HOME for the duration of the test
  try {
    callback();
  } finally {
    // Cleanup
    process.env.HOME = originalHome;
    fs.rmSync(tmpDir, { recursive: true, force: true });
  }
}

// Test suite
withTempHome(() => {
  // Ensure a clean start
  const logPath = getLogPath();
  assert(!fs.existsSync(logPath), 'Log file should not exist before first operation');

  // Add two moods
  addMood('happy');
  addMood('sad');

  // Verify file was created
  assert(fs.existsSync(logPath), 'Log file should exist after adding moods');

  // Verify stats
  const stats = getStats();
  assert.deepStrictEqual(stats, { happy: 1, sad: 1 }, 'Stats should reflect added moods');

  // Add another "happy"
  addMood('happy');
  const updatedStats = getStats();
  assert.deepStrictEqual(updatedStats, { happy: 2, sad: 1 }, 'Stats should update correctly after additional entries');

  console.log('All Mood Logger tests passed.');
});
