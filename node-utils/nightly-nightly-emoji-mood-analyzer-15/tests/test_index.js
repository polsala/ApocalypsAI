const assert = require('assert');
const { analyzeMood } = require('../src/index.js');
function testCase(text, expected) {
  const result = analyzeMood(text);
  assert.strictEqual(result, expected, `Expected ${expected} for "${text}", got ${result}`);
}
// Happy
testCase('I am so happy today!', '😊');
// Sad
testCase('It is a sad day.', '😢');
// Angry
testCase('I am angry about the delay.', '😠');
// Surprised
testCase('Wow, that was unexpected!', '😲');
// Fear
testCase('I am scared of the dark.', '😨');
// Default (no keywords)
testCase('Just a neutral statement.', '🤔');
console.log('All tests passed.');
