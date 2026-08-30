const assert = require('assert');
const { analyzeMood } = require('../src/index.js');

// Mock rationale: deterministic keyword matching
assert.strictEqual(analyzeMood('I am feeling great!'), '😊', 'Happy keyword should return 😊');
assert.strictEqual(analyzeMood('This is terrible, I am sad.'), '😢', 'Sad keyword should return 😢');
assert.strictEqual(analyzeMood('I am so mad right now'), '😠', 'Angry keyword should return 😠');
assert.strictEqual(analyzeMood('Just an ordinary day'), '🤔', 'No keyword should return 🤔');

console.log('All tests passed.');
