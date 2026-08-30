const assert = require('assert');
const { analyzeMood } = require('../src/index');

// Mock rationale: deterministic keyword matching
assert.strictEqual(analyzeMood('I am very happy today'), '😄');
assert.strictEqual(analyzeMood('Feeling sad and blue'), '😢');
assert.strictEqual(analyzeMood('He is angry!'), '😠');
assert.strictEqual(analyzeMood('She is scared of the dark'), '😱');
assert.strictEqual(analyzeMood('I love this!'), '❤️');
assert.strictEqual(analyzeMood('Just a neutral statement'), '🤔');

console.log('All tests passed.');
