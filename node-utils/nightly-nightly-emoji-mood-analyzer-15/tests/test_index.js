const assert = require('assert');
const { analyzeMood } = require('../src/index');

function testCase(input, expected) {
  const result = analyzeMood(input);
  assert.strictEqual(result, expected, `Input: "${input}"`);
}

// Happy
testCase('I am feeling great today!', '😊');
// Sad
testCase('It is a rainy and sad day.', '😢');
// Angry
testCase('I am so mad about the delay.', '😠');
// Surprise
testCase('Wow, that was unexpected!', '😲');
// Fear
testCase('I am scared of the dark.', '😨');
// Tired
testCase('I need a nap after this.', '😴');
// Love
testCase('Love is in the air.', '❤️');
// Run
testCase('Just completed a marathon.', '🏃‍♂️');
// Neutral fallback
testCase('Just a regular sentence.', '🤔');

console.log('All tests passed.');
