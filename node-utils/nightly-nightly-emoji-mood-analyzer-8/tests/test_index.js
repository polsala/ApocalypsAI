const assert = require('assert');
const { analyzeMood } = require('../src/index');

// Mock rationale: deterministic keyword matching

assert.strictEqual(analyzeMood('I am so happy today!'), 'ð');
assert.strictEqual(analyzeMood('Feeling sad and lonely.'), 'ð¢');
assert.strictEqual(analyzeMood('What a terrifying nightmare!'), 'ð±');
assert.strictEqual(analyzeMood('He shouted in anger.'), 'ð ');
assert.strictEqual(analyzeMood('Wow, that was unexpected!'), 'ð²');
assert.strictEqual(analyzeMood('Just a regular sentence.'), 'ð¤');

console.log('All tests passed.');
