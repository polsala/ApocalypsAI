// Tests for Nightly Emoji Mood Analyzer
const assert = require('assert');
const { analyzeMood } = require('../src/main');

// Mock rationale: deterministic keyword matching ensures consistent output.

function testCase(input, expected) {
  const result = analyzeMood(input);
  assert.strictEqual(result, expected, `Input: "${input}"`);
}

// Happy cases
testCase('I am so happy and excited!', 'ð');
testCase('What a wonderful day', 'ð');

// Sad cases
testCase('I feel sad and down', 'ð¢');
testCase('It was a terrible mistake', 'ð¢');

// Angry cases
testCase('I am angry about this', 'ð ');
testCase('He is mad and furious', 'ð ');

// Scared cases
testCase('I am scared of the dark', 'ð±');
testCase('That was terrifying', 'ð±');

// Surprised cases
testCase('Wow, that was amazing!', 'ð²');
testCase('I am shocked', 'ð²');

// Neutral cases
testCase('It is okay, nothing special', 'ð');
testCase('Meh, just average', 'ð');

// Empty input
testCase('', 'ð¤');

console.log('All tests passed.');
