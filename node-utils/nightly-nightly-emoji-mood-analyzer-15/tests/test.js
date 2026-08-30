// Simple test runner using Node's built‑in assert module
const assert = require('assert');
const { tokenize, sentimentScore, scoreToEmoji } = require('../src/index.js');

// Helper to run a test and report failures
function runTest(name, fn) {
  try {
    fn();
    console.log(`✅ ${name}`);
  } catch (err) {
    console.error(`❌ ${name}`);
    console.error(err);
    process.exitCode = 1;
  }
}

// Tests
runTest('tokenize splits words and lowercases', () => {
  const result = tokenize('Hello, World! 123');
  assert.deepStrictEqual(result, ['hello', 'world', '123']);
});

runTest('sentimentScore positive words', () => {
  const score = sentimentScore('I love sunny days and great coffee');
  // love, sunny, great => +3
  assert.strictEqual(score, 3);
});

runTest('sentimentScore negative words', () => {
  const score = sentimentScore('I am sad and frustrated with terrible bugs');
  // sad, frustrated, terrible => -3
  assert.strictEqual(score, -3);
});

runTest('sentimentScore mixed words', () => {
  const score = sentimentScore('I love the rain but hate the storm');
  // love (+1), rain (neutral), hate (-1), storm (-1) => -1
  assert.strictEqual(score, -1);
});

runTest('scoreToEmoji happy', () => {
  assert.strictEqual(scoreToEmoji(2), '😄');
});

runTest('scoreToEmoji sad', () => {
  assert.strictEqual(scoreToEmoji(-2), '😞');
});

runTest('scoreToEmoji neutral', () => {
  assert.strictEqual(scoreToEmoji(0), '😐');
  assert.strictEqual(scoreToEmoji(1), '😐');
  assert.strictEqual(scoreToEmoji(-1), '😐');
});

// Mock rationale: tests are deterministic, no external I/O, and cover core logic.
