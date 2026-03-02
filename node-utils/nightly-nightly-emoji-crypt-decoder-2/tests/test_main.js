const assert = require('assert');
const { execSync } = require('child_process');
const path = require('path');
const { decode } = require('../src/main');

// Direct function tests
assert.strictEqual(decode('🌧️☢️'), 'rain radiation');
assert.strictEqual(decode('🧟🪦'), 'zombie grave');
assert.strictEqual(decode('❓'), '?');

// CLI execution tests (offline, no network calls)
function runCli(input) {
  const cmd = `node ${path.resolve(__dirname, '../src/main.js')} ${input}`;
  return execSync(cmd, { encoding: 'utf8' }).trim();
}

assert.strictEqual(runCli('🌧️☢️'), 'rain radiation');
assert.strictEqual(runCli('🧟🪦'), 'zombie grave');
assert.strictEqual(runCli('❓'), '?');

console.log('All tests passed');
