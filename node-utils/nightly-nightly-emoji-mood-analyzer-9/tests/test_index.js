const assert = require('assert');
const { analyzeMood } = require('../src/index.js');

// Mock rationale: deterministic tests using fixed strings

function testPositive() {
  const result = analyzeMood('I am very happy and love this great product');
  assert.strictEqual(result, 'ð', 'Positive text should yield happy emoji');
}

function testNegative() {
  const result = analyzeMood('This is terrible, I hate it and feel sad');
  assert.strictEqual(result, 'ð ', 'Negative text should yield angry emoji');
}

function testNeutral() {
  const result = analyzeMood('The sky is blue and the grass is green');
  assert.strictEqual(result, 'ð¤', 'Neutral text should yield thinking emoji');
}

function run() {
  testPositive();
  testNegative();
  testNeutral();
  console.log('All tests passed');
}

run();
