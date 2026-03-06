const assert = require('assert');
const { analyzeMood } = require('../src/index.js');

function testCase(text, expected) {
  const result = analyzeMood(text);
  assert.strictEqual(result, expected, `Expected "${expected}" for "${text}", got "${result}"`);
}

// Positive sentiment
testCase('I am happy and thrilled', '😊');
// Neutral sentiment
testCase('The sky is blue', '😐');
// Slightly negative sentiment
testCase('I feel sad today', '😢');
// Very negative sentiment
testCase('I hate this terrible awful situation', '😡');

console.log('All tests passed.');
