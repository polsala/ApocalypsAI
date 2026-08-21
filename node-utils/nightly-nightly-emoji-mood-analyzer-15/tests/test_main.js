const assert = require('assert');
const { analyzeMood } = require('../src/main');

// Mock rationale: deterministic tests using fixed strings
assert.strictEqual(analyzeMood('I love this wonderful day'), '😊', 'Positive sentiment should yield happy emoji');
assert.strictEqual(analyzeMood('It is a terrible, horrible night'), '😢', 'Negative sentiment should yield sad emoji');
assert.strictEqual(analyzeMood('The sky is blue'), '😐', 'Neutral sentiment should yield neutral emoji');

console.log('All tests passed.');
