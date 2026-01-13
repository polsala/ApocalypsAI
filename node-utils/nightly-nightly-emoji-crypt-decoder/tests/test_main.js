const assert = require('assert');
const { decode } = require('../src/main');
const { execSync } = require('child_process');

function runTests() {
  // Direct function tests
  assert.strictEqual(decode('ððð'), 'ABC', 'Basic decode failed');
  assert.strictEqual(decode('ð'), '?', 'Unknown emoji handling failed');

  // CLI argument test
  let out = execSync('node src/main.js ððð', { encoding: 'utf8' }).trim();
  assert.strictEqual(out, 'ABC', 'CLI argument test failed');

  // CLI stdin test
  out = execSync('echo ððð | node src/main.js', { encoding: 'utf8' }).trim();
  assert.strictEqual(out, 'ABC', 'CLI stdin test failed');

  console.log('All tests passed');
}

runTests();

