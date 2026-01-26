const assert = require('assert');
const { analyze } = require('../src/index');

function runTests() {
  // Positive emoji
  assert.strictEqual(analyze('I am happy 😄'), 1, 'Single happy emoji should yield +1');
  // Negative emoji
  assert.strictEqual(analyze('Bad day 😢'), -1, 'Single sad emoji should yield -1');
  // Mixed emojis cancel out
  assert.strictEqual(analyze('Mixed feelings 😄😢'), 0, 'Opposite emojis should cancel to 0');
  // Multiple positives
  assert.strictEqual(analyze('Great! 😄👍'), 2, 'Two positive emojis should yield +2');
  // No emojis
  assert.strictEqual(analyze('Just plain text'), 0, 'No emojis should yield 0');
  console.log('All tests passed');
}

runTests();
