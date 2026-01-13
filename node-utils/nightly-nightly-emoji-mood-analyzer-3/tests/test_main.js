// tests/test_main.js
// Simple test suite using Node's builtâin assert module. No external dependencies.

const assert = require('assert');
const { analyzeMood, scoreText, scoreToEmoji } = require('../src/main.js');

// Mock rationale: deterministic word lists guarantee stable scores.

function runTests() {
  // Positive sentiment
  const posText = 'I love sunny days and wonderful coffee!';
  assert.strictEqual(scoreText(posText), 3, 'Positive score should be 3');
  assert.strictEqual(analyzeMood(posText), 'ð', 'Positive mood should map to ð');

  // Negative sentiment
  const negText = 'Everything is terrible, I am sad and angry.';
  assert.strictEqual(scoreText(negText), -3, 'Negative score should be -3');
  assert.strictEqual(analyzeMood(negText), 'ð¢', 'Negative mood should map to ð¢');

  // Neutral sentiment â mixed words cancel out
  const neuText = 'I am happy but also a bit sad.';
  // happy (+1) + sad (-1) => 0
  assert.strictEqual(scoreText(neuText), 0, 'Neutral score should be 0');
  assert.strictEqual(analyzeMood(neuText), 'ð', 'Neutral mood should map to ð');

  // Edge case â no recognizable words
  const unknown = 'xyz abc 123';
  assert.strictEqual(scoreText(unknown), 0, 'Unknown words yield score 0');
  assert.strictEqual(analyzeMood(unknown), 'ð', 'Unknown text yields neutral emoji');

  console.log('All tests passed.');
}

runTests();
