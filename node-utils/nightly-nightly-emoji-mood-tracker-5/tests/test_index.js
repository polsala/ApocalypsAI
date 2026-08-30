const { execSync } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');
const assert = require('assert');

// Use a temporary file for storage to keep tests deterministic
const tempFile = path.join(os.tmpdir(), `emoji_mood_test_${Date.now()}.json`);
process.env.EMOJI_MOOD_FILE = tempFile;

function run(args) {
  // Execute the CLI script with the provided arguments
  return execSync(`node ${path.resolve(__dirname, '../src/index.js')} ${args}`, { env: process.env })
    .toString()
    .trim();
}

// Ensure a clean start
if (fs.existsSync(tempFile)) fs.unlinkSync(tempFile);

// Add several mood entries
run('add 😊 Feeling happy');
run('add 😢 Sad day');
run('add 😊 Another happy moment');

// Verify summary counts
const summary = run('summary');
assert(summary.includes('😊: 2'), 'Summary should count two 😊');
assert(summary.includes('😢: 1'), 'Summary should count one 😢');

// Verify list output contains all notes
const list = run('list');
assert(list.includes('Feeling happy'), 'List should contain first note');
assert(list.includes('Sad day'), 'List should contain second note');
assert(list.includes('Another happy moment'), 'List should contain third note');

console.log('All tests passed.');
