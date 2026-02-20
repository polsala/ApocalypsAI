// Simple test runner using Node's assert
const assert = require('assert');
const { analyzeMood } = require('../src/index.js');

// Mock rationale: deterministic tests with fixed strings
function runTests() {
  assert.strictEqual(analyzeMood('I love sunny days and feel great!'), '😊', 'Positive mood should be 😊');
  assert.strictEqual(analyzeMood('I hate rainy weather, it is terrible.'), '😢', 'Negative mood should be 😢');
  assert.strictEqual(analyzeMood('The sky is blue.'), '😐', 'Neutral mood should be 😐');
  console.log('All tests passed.');
}

runTests();
