const assert = require('assert');
const { analyzeMood } = require('../src/index.js');

// Mock rationale: deterministic inputs
assert.strictEqual(analyzeMood('I am so happy and love this!'), '😊', 'Positive sentiment should yield 😊');
assert.strictEqual(analyzeMood('This is terrible and I hate it.'), '😢', 'Negative sentiment should yield 😢');
assert.strictEqual(analyzeMood('Just an ordinary day.'), '😐', 'Neutral sentiment should yield 😐');

console.log('All tests passed.');
