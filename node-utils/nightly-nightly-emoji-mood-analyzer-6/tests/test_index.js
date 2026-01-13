const assert = require('assert');
const {analyzeMood} = require('../src/index.js');

// Mock rationale: deterministic keyword matching
assert.strictEqual(analyzeMood('I am so happy today!'), 'ð');
assert.strictEqual(analyzeMood('This is terrible and sad.'), 'ð');
assert.strictEqual(analyzeMood('I am angry about the delay.'), 'ð ');
assert.strictEqual(analyzeMood('I just finished a marathon, wow!'), 'ð¤©');
assert.strictEqual(analyzeMood('Just an ordinary day.'), 'ð¤');

console.log('All tests passed.');
