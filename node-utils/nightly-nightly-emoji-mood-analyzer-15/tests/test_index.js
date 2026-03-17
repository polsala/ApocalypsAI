// Tests for nightly-emoji-mood-analyzer
// No external dependencies; uses Node's built‑in assert.

const assert = require('assert');
const { analyzeMood } = require('../src/index.js');

// Mock rationale: deterministic inputs, no network calls.

function runTests() {
  // Happy sentence
  assert.strictEqual(
    analyzeMood('I love sunny days and fresh coffee'),
    '😊',
    'Expected happy emoji for positive words'
  );

  // Angry sentence
  assert.strictEqual(
    analyzeMood('I am frustrated with endless bugs'),
    '😠',
    'Expected angry emoji for negative words'
  );

  // Mixed but neutral overall
  assert.strictEqual(
    analyzeMood('The movie was good but the ending was bad'),
    '😐',
    'Expected neutral emoji for balanced sentiment'
  );

  // Slightly happy
  assert.strictEqual(
    analyzeMood('It was a great day'),
    '😊',
    'Slightly positive should still be happy emoji'
  );

  // Slightly sad
  assert.strictEqual(
    analyzeMood('I feel sad'),
    '🙁',
    'Slightly negative should be sad emoji'
  );

  // Empty input
  assert.strictEqual(
    analyzeMood(''),
    '🤔',
    'Empty input should return thinking emoji'
  );

  console.log('All tests passed.');
}

runTests();
