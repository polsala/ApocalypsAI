const assert = require('assert');
const fs = require('fs');
const os = require('os');
const path = require('path');

// Mock rationale: Use a temporary HOME directory to avoid polluting real user data.
const tmpHome = fs.mkdtempSync(path.join(os.tmpdir(), 'mood-test-'));
process.env.HOME = tmpHome;

// Mock rationale: Freeze time to a known ISO string for deterministic timestamps.
const FIXED_ISO = '2023-01-01T12:00:00.000Z';
const RealDate = Date;
global.Date = class extends RealDate {
  constructor(...args) {
    if (args.length === 0) {
      super(FIXED_ISO);
    } else {
      super(...args);
    }
  }
  static now() {
    return new RealDate(FIXED_ISO).getTime();
  }
  static parse(str) {
    return RealDate.parse(str);
  }
  static UTC(...args) {
    return RealDate.UTC(...args);
  }
};

const { addEntry, getSummary, loadData } = require('../src/index.js');

// Ensure a clean start (ignore if file does not exist).
try {
  fs.unlinkSync(path.join(tmpHome, '.mood_tracker.json'));
} catch (_) {}

// Test adding entries.
addEntry('😊', 'Feeling good');
addEntry('😢', 'Sad day');
addEntry('😊', 'Another happy moment');

// Verify data persisted correctly.
const data = loadData();
assert.strictEqual(data.length, 3, 'Should have three entries');
assert.strictEqual(data[0].emoji, '😊');
assert.strictEqual(data[0].date, FIXED_ISO);

// Verify summary counts.
const summary = getSummary();
assert.deepStrictEqual(summary, { '😊': 2, '😢': 1 }, 'Summary counts mismatch');

console.log('All tests passed.');
