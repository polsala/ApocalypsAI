const assert = require('assert');
const { analyzeMood } = require('../src/index');

// Mock rationale: deterministic tests using fixed strings

// Happy dominant
assert.strictEqual(analyzeMood('I am happy and love the sunny weather'), '😊');

// Sad dominant
assert.strictEqual(analyzeMood('It is a sad and terrible day'), '😢');

// Angry dominant
assert.strictEqual(analyzeMood('I am angry and mad at the traffic'), '😠');

// No keywords
assert.strictEqual(analyzeMood('Just a regular sentence with no mood words'), '🤔');

console.log('All tests passed');
