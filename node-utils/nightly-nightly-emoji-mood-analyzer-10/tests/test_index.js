const assert = require('assert');
const {detectMood} = require('../src/index');

function testCase(text, expected) {
  const result = detectMood(text);
  assert.strictEqual(result, expected, `Expected ${expected} for "${text}", got ${result}`);
}

// Happy mood
testCase('I am so happy and excited!', 'ð');

// Sad mood
testCase('It is a sad day.', 'ð¢');

// Angry mood
testCase('I am angry about the delay.', 'ð ');

// Surprised mood
testCase('Wow, that was surprising!', 'ð²');

// Fear mood
testCase('I am scared of the dark.', 'ð±');

// Neutral fallback (no keywords)
testCase('Just an ordinary day.', 'ð');

console.log('All tests passed.');
