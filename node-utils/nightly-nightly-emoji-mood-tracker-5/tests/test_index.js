const fs = require('fs');
const os = require('os');
const path = require('path');
const assert = require('assert');
const {
  getDataFilePath,
  loadData,
  saveData,
  addEntry,
  getStats,
  listEntries,
} = require('../src/index');

// Helper to create a temporary directory for isolated tests
function withTempDir(callback) {
  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'emoji-mood-test-'));
  const originalEnv = process.env.EMOJI_MOOD_DATA_PATH;
  process.env.EMOJI_MOOD_DATA_PATH = path.join(tmpDir, 'data.json');
  try {
    callback(tmpDir);
  } finally {
    // Cleanup
    delete process.env.EMOJI_MOOD_DATA_PATH;
    if (originalEnv !== undefined) process.env.EMOJI_MOOD_DATA_PATH = originalEnv;
    fs.rmSync(tmpDir, { recursive: true, force: true });
  }
}

// Mock rationale: All file operations are confined to a temporary directory, ensuring
// the real user data file is never touched and tests remain deterministic.

describe('Emoji Mood Tracker', () => {
  test('addEntry stores data correctly', () => {
    withTempDir(() => {
      addEntry('😊', 'Feeling good');
      const data = loadData();
      assert.strictEqual(data.length, 1);
      assert.strictEqual(data[0].emoji, '😊');
      assert.strictEqual(data[0].note, 'Feeling good');
    });
  });

  test('getStats aggregates emoji counts', () => {
    withTempDir(() => {
      addEntry('😊');
      addEntry('😢');
      addEntry('😊');
      const stats = getStats();
      assert.deepStrictEqual(stats, { '😊': 2, '😢': 1 });
    });
  });

  test('listEntries returns recent entries in reverse chronological order', () => {
    withTempDir(() => {
      addEntry('😀', 'First');
      addEntry('😎', 'Second');
      addEntry('🤔', 'Third');
      const recent = listEntries(2);
      assert.strictEqual(recent.length, 2);
      assert.strictEqual(recent[0].emoji, '🤔'); // most recent
      assert.strictEqual(recent[1].emoji, '😎');
    });
  });
});
