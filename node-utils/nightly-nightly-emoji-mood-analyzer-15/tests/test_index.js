const assert = require('assert');
const { analyzeMood } = require('../src/index');

// Mock rationale: deterministic tests using fixed sentences.
assert.strictEqual(analyzeMood('I love sunny days'), '😄', 'Positive sentence should be very happy');
assert.strictEqual(analyzeMood('I am happy'), '😊', 'Mildly positive');
assert.strictEqual(analyzeMood('It is okay'), '😐', 'Neutral');
assert.strictEqual(analyzeMood('I am sad'), '🙁', 'Mildly negative');
assert.strictEqual(analyzeMood('I hate rain'), '😢', 'Strongly negative');

console.log('All tests passed');
