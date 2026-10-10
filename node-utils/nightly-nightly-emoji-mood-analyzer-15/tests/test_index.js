// tests/test_index.js
// Simple deterministic tests – no external resources.

const assert = require('assert');
const { analyzeMood } = require('../src/index');

// Mock rationale: using a fixed set of inputs ensures deterministic outcomes.

function runTests() {
  // Positive sentiment
  assert.strictEqual(analyzeMood('I love sunny days'), '😊', 'Positive sentence should yield 😊');

  // Negative sentiment
  assert.strictEqual(analyzeMood('I hate rainy weather'), '😢', 'Negative sentence should yield 😢');

  // Neutral / unknown sentiment
  assert.strictEqual(analyzeMood('It is a day'), '😐', 'Neutral sentence should yield 😐');

  // Mixed sentiment – more positive words
  assert.strictEqual(analyzeMood('I love the great sunshine but the rain makes me sad'), '😊', 'Mixed with more positives should yield 😊');

  // Mixed sentiment – more negative words
  assert.strictEqual(analyzeMood('The awesome view is ruined by terrible, awful clouds'), '😢', 'Mixed with more negatives should yield 😢');

  // Empty string
  assert.strictEqual(analyzeMood(''), '😐', 'Empty input should yield neutral emoji');

  // Non‑string input
  assert.strictEqual(analyzeMood(null), '😐', 'Non‑string input should yield neutral emoji');

  console.log('All tests passed.');
}

runTests();
