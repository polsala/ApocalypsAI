// tests/test_main.js
// Tests for nightly-emoji-mood-analyzer

const assert = require('assert');
const { spawnSync } = require('child_process');
const path = require('path');

function runTool(args, input) {
  const result = spawnSync('node', [path.resolve(__dirname, '..', 'src', 'main.js'), ...args], {
    input: input,
    encoding: 'utf8'
  });
  if (result.error) throw result.error;
  return result.stdout.trim();
}

// Test 1: Positive sentiment should yield 😊
const out1 = runTool([], 'I love sunshine and wonderful days');
assert.strictEqual(out1, '😊', 'Positive text should return happy emoji');

// Test 2: Negative sentiment should yield 😡
const out2 = runTool([], 'I hate rainy days and feel angry');
assert.strictEqual(out2, '😡', 'Negative text should return angry emoji');

// Test 3: Neutral sentiment should yield 😐
const out3 = runTool([], 'It is a day');
assert.strictEqual(out3, '😐', 'Neutral text should return neutral emoji');

// Test 4: Argument mode – positive
const out4 = runTool(['I am glad and happy'], null);
assert.strictEqual(out4, '😊', 'Argument positive text should return happy emoji');

console.log('All tests passed.');
