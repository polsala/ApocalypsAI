const { execSync } = require('child_process');
const assert = require('assert');
const path = require('path');

function run(args) {
  // Build the command string; emojis are passed directly to the shell.
  const cmd = `node ${path.join(__dirname, '..', 'src', 'main.js')} ${args}`;
  return execSync(cmd, { encoding: 'utf8' }).trim();
}

// ---------------------------------------------------------------------
// Test 1: basic decoding
// ---------------------------------------------------------------------
const out1 = run('🌞🔥🧟');
assert.strictEqual(out1, 'sun fire zombie', 'Decoding emojis failed');

// ---------------------------------------------------------------------
// Test 2: reading from stdin (pipe)
// ---------------------------------------------------------------------
const pipeCmd = `echo "🚀🛡️" | node ${path.join(__dirname, '..', 'src', 'main.js')}`;
const out2 = execSync(pipeCmd, { encoding: 'utf8' }).trim();
assert.strictEqual(out2, 'rocket shield', 'Decoding from stdin failed');

// ---------------------------------------------------------------------
// Test 3: --list flag contains expected mapping entry
// ---------------------------------------------------------------------
const listOut = run('--list');
assert.ok(listOut.includes('🌞: sun'), '--list output missing expected mapping');

console.log('All tests passed');
