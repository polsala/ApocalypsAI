const assert = require('assert');
const { suggestLabels } = require('../src/main');

// Mock rationale: deterministic keyword mapping ensures repeatable results

function testCase(title, expected) {
  const result = suggestLabels(title);
  assert.deepStrictEqual(result.sort(), expected.sort(), `Failed for "${title}"`);
}

// Test known mappings
testCase('Crash on startup', ['bug']);
testCase('Add dark mode feature', ['enhancement']);
testCase('Update README documentation', ['documentation']);
testCase('Refactor authentication flow', ['refactor']);
testCase('Random unrelated title', ['question']);

console.log('All tests passed.');
