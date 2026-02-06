// Mock rationale: Tests run offline, invoking the CLI via child_process.execSync.
// They verify that known keywords produce the expected emojis.

const assert = require('assert');
const { execSync } = require('child_process');
const path = require('path');

// Resolve the CLI entry point.
const cliPath = path.resolve(__dirname, '..', '..', 'src', 'index.js');

function runCli(input) {
  // When input contains spaces, we pass it as a single argument.
  // For stdin tests we pipe the string.
  if (input.mode === 'arg') {
    return execSync(`node ${cliPath} "${input.message}"`, { encoding: 'utf8' }).trim();
  } else if (input.mode === 'stdin') {
    return execSync(`echo "${input.message}" | node ${cliPath}`, { encoding: 'utf8' }).trim();
  }
  throw new Error('Invalid test mode');
}

// Test 1: single keyword via argument.
const out1 = runCli({ mode: 'arg', message: 'Add new feature' });
assert.strictEqual(out1, 'Add new feature ➕', 'Should append ➕ for "add"');

// Test 2: multiple keywords via stdin.
const out2 = runCli({ mode: 'stdin', message: 'Fix bug in parser' });
// Order of emojis follows detection order; both 🛠️ and 🐛 should appear.
assert.strictEqual(out2, 'Fix bug in parser 🛠️ 🐛', 'Should append 🛠️ and 🐛 for "fix" and "bug"');

// Test 3: no matching keywords – message unchanged.
const out3 = runCli({ mode: 'arg', message: 'Initial commit' });
assert.strictEqual(out3, 'Initial commit', 'Message without keywords should stay unchanged');

console.log('All tests passed.');
