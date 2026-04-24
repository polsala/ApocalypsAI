const assert = require('assert');
const { analyzeMood } = require('../src/main');

// Mock rationale: deterministic tests using fixed strings
function testPositive() {
  const result = analyzeMood('I love this awesome sunny day');
  assert.strictEqual(result, '😊');
}
function testNeutral() {
  const result = analyzeMood('The sky is blue');
  assert.strictEqual(result, '😐');
}
function testNegative() {
  const result = analyzeMood('I feel sad and gloomy');
  assert.strictEqual(result, '😞');
}
function testSlightPositive() {
  const result = analyzeMood('It is good');
  assert.strictEqual(result, '🙂');
}
function testSlightNegative() {
  const result = analyzeMood('It is bad');
  assert.strictEqual(result, '🙁');
}
function run() {
  testPositive();
  testNeutral();
  testNegative();
  testSlightPositive();
  testSlightNegative();
  console.log('All tests passed');
}
run();
