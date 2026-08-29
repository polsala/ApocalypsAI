const assert = require('assert');
const { analyzeSentiment, moodDefinitions } = require('../src/index.js');

// Mock rationale: The CLI tool's core logic (sentiment analysis) is a pure function.
// We are testing this function directly, not the CLI input/output mechanism.
// The `moodDefinitions` are also static data, so no mocking is needed for them.

function runTest(name, fn) {
  try {
    fn();
    console.log(`✅ ${name}`);
  } catch (error) {
    console.error(`❌ ${name}`);
    console.error(error.stack);
    process.exit(1);
  }
}

runTest('should return Blue for strongly positive text', () => {
  const result = analyzeSentiment('This is a wonderful, fantastic, amazing day!');
  assert.strictEqual(result.mood, 'blue');
});

runTest('should return Green for moderately positive text', () => {
  const result = analyzeSentiment('I am happy with the progress.');
  assert.strictEqual(result.mood, 'green');
});

runTest('should return Yellow for neutral text', () => {
  const result = analyzeSentiment('The report was submitted.');
  assert.strictEqual(result.mood, 'yellow');
});

runTest('should return Yellow for empty text', () => {
  const result = analyzeSentiment('');
  assert.strictEqual(result.mood, 'yellow');
});

runTest('should return Yellow for text with only stop words', () => {
  const result = analyzeSentiment('is the a and but');
  assert.strictEqual(result.mood, 'yellow');
});

runTest('should return Orange for moderately negative text', () => {
  const result = analyzeSentiment('I am worried about the issue.');
  assert.strictEqual(result.mood, 'orange');
});

runTest('should return Red for strongly negative text', () => {
  const result = analyzeSentiment('This is a terrible, horrible, awful failure!');
  assert.strictEqual(result.mood, 'red');
});

runTest('should handle mixed sentiment leaning positive', () => {
  const result = analyzeSentiment('Great success, but a minor problem.'); // +1 (great, success) -1 (problem) = +1
  assert.strictEqual(result.mood, 'green');
});

runTest('should handle mixed sentiment leaning negative', () => {
  const result = analyzeSentiment('A terrible bug, but we hope to fix it.'); // -1 (terrible, bug) +1 (hope) = -1
  assert.strictEqual(result.mood, 'orange');
});

runTest('should handle mixed sentiment resulting in neutral', () => {
  const result = analyzeSentiment('Good progress, but also some issues.'); // +1 (good, progress) -1 (issues) = 0
  assert.strictEqual(result.mood, 'yellow');
});

runTest('should be case-insensitive', () => {
  const result = analyzeSentiment('WoNdErFuL dAy');
  assert.strictEqual(result.mood, 'blue');
});

console.log('\nAll sentiment analysis tests passed!');
