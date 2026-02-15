// tests/test_index.js
const { execFileSync } = require('child_process');
const path = require('path');
const assert = require('assert');

function runAction(labels) {
  const env = { ...process.env, INPUT_LABELS: labels };
  const scriptPath = path.resolve(__dirname, '..', 'src', 'index.js');
  const output = execFileSync('node', [scriptPath], { env, encoding: 'utf8' });
  return output;
}

// Test single label
let out = runAction('bug');
assert.ok(out.includes('Applying labels: bug'), 'Should log single label');

// Test multiple labels with spaces
out = runAction('bug, documentation , enhancement');
assert.ok(out.includes('Applying labels: bug, documentation, enhancement'), 'Should trim and join');

// Test empty input
out = runAction('');
assert.ok(out.includes('Applying labels: '), 'Should handle empty input');

console.log('All tests passed');
