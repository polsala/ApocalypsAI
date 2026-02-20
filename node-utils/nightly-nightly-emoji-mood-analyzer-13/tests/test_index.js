const assert = require('assert');
const { analyzeMood } = require('../src/index');

function test(text, expected) {
  const result = analyzeMood(text);
  assert.strictEqual(result, expected, `Expected ${expected} for "${text}"`);
}

// Positive
test('I am very happy and love this great day', '😊');
// Negative
test('It was a terrible, sad, and awful experience', '😞');
// Neutral
test('The cat sits on the mat.', '😐');

console.log('All tests passed.');
