const assert = require('assert');
const { analyzeMood } = require('../src/main');

// Mock rationale: deterministic tests without external dependencies

assert.strictEqual(analyzeMood('I am so happy today!'), '😊', 'Happy mood');
assert.strictEqual(analyzeMood('Feeling sad and down.'), '😢', 'Sad mood');
assert.strictEqual(analyzeMood('What a surprise!'), '😲', 'Surprise mood');
assert.strictEqual(analyzeMood('I love this project'), '❤️', 'Love mood');
assert.strictEqual(analyzeMood('I am scared of bugs'), '😨', 'Fear mood');
assert.strictEqual(analyzeMood('This makes me angry'), '😠', 'Angry mood');
assert.strictEqual(analyzeMood('Just an ordinary day.'), '🤔', 'Neutral default');

console.log('All tests passed.');
