const assert = require('assert');
const { analyzeMood } = require('../src/index');

function test(input, expected) {
  const result = analyzeMood(input);
  assert.strictEqual(result, expected, `Expected ${expected} for "${input}", got ${result}`);
}

// Happy mood
test('I am so happy and excited!', '😄');
// Sad mood
test('It is a sad, gloomy day.', '😢');
// Angry mood
test('I am angry and upset.', '😠');
// Neutral (no keywords)
test('The sky is blue.', '🤔');

console.log('All tests passed.');
