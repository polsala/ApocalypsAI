// tests/test_main.js
// Automated tests for nightly-emoji-decoder.
// These tests run offline and use child_process to invoke the CLI.

const assert = require('assert');
const { execSync } = require('child_process');
const path = require('path');

const CLI = path.resolve(__dirname, '..', 'src', 'main.js');

function run(args, input = null) {
  const cmd = `node ${CLI} ${args}`;
  if (input !== null) {
    // Pipe input via echo.
    return execSync(`echo "${input}" | ${cmd}`).toString();
  }
  return execSync(cmd).toString();
}

// Test 1: space‑separated emojis via argument.
let out = run('"😀 😃 😄"');
assert.strictEqual(out, 'ABC\n', 'Should decode spaced emojis to ABC');

// Test 2: concatenated emojis via argument.
out = run('"😀😃😄"');
assert.strictEqual(out, 'ABC\n', 'Should decode concatenated emojis to ABC');

// Test 3: unknown emoji should become "?".
out = run('"🧐"');
assert.strictEqual(out, '?\n', 'Unknown emoji should decode to ?');

// Test 4: input via stdin (pipe).
out = run('', '😀 😃 😄');
assert.strictEqual(out, 'ABC\n', 'Stdin input should decode to ABC');

console.log('All tests passed.');
