const assert = require('assert');
const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

// Helper to run the CLI with a custom DATA_FILE env var.
function runCli(args, env = {}) {
  const cliPath = path.resolve(__dirname, '..', 'src', 'index.js');
  const envVars = Object.assign({ DATA_FILE: testDataFile }, process.env, env);
  const cmd = `node ${cliPath} ${args.join(' ')}`;
  return execSync(cmd, { env: envVars, encoding: 'utf8' }).trim();
}

// Temporary data file for isolation.
const testDataFile = path.join(__dirname, 'mood_test_data.json');

// Ensure a clean state before each test.
function resetDataFile() {
  if (fs.existsSync(testDataFile)) {
    fs.unlinkSync(testDataFile);
  }
}

// ----- Tests -----

// Test adding entries with explicit timestamps.
resetDataFile();
runCli(['add', '😊', 'Happy day', '--timestamp', '1609459200000']);
runCli(['add', '😢', 'Sad night', '--timestamp', '1609545600000']);

// Verify the data file content.
const rawData = fs.readFileSync(testDataFile, 'utf8');
const entries = JSON.parse(rawData);
assert.strictEqual(entries.length, 2, 'Two entries should be recorded');
assert.deepStrictEqual(entries[0], { timestamp: 1609459200000, emoji: '😊', note: 'Happy day' });
assert.deepStrictEqual(entries[1], { timestamp: 1609545600000, emoji: '😢', note: 'Sad night' });

// Test stats output.
const statsOutput = runCli(['stats']);
// Order is not guaranteed; split lines and sort for comparison.
const lines = statsOutput.split('\n').sort();
assert.deepStrictEqual(lines, ['😊: 1', '😢: 1'].sort(), 'Stats should reflect one entry per emoji');

// Clean up after tests.
resetDataFile();
console.log('All tests passed.');
