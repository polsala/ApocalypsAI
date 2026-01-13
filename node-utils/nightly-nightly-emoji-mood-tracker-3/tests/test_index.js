const assert = require('assert');
const os = require('os');
const path = require('path');
const fs = require('fs');

// Import the functions to test
const { logMood, getSummary } = require('../src/index.js');

// Helper to create a unique temp file for each test run
function createTempFile() {
  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'mood-test-'));
  return path.join(tmpDir, 'mood.json');
}

(async () => {
  // Set up isolated environment
  const tempFile = createTempFile();
  process.env.MOOD_FILE = tempFile;

  // Ensure clean start
  let summary = await getSummary();
  assert.deepStrictEqual(summary, {}, 'Initial summary should be empty');

  // Log a few moods
  await logMood('ð', 'Happy');
  await logMood('ð', 'Sad');
  await logMood('ð', 'Even happier');

  // Verify summary counts
  summary = await getSummary();
  assert.strictEqual(summary['ð'], 2, 'ð should appear twice');
  assert.strictEqual(summary['ð'], 1, 'ð should appear once');

  // Clean up
  delete process.env.MOOD_FILE;
  fs.rmSync(path.dirname(tempFile), { recursive: true, force: true });

  console.log('All tests passed.');
})();
