// tests/test_main.js
// Simple assertions without external libraries.
const assert = require('assert');
const { computeLabel } = require('../src/index');

// Mock rationale: deterministic inputs, no network calls.
function runTests() {
  const cases = [
    { title: 'Fix critical bug in parser', expected: '🐞 bug' },
    { title: 'Add new feature: user profiles', expected: '✨ feature' },
    { title: 'Update docs for API', expected: '📚 docs' },
    { title: 'Write tests for edge cases', expected: '✅ test' },
    { title: 'Refactor authentication module', expected: '🔧 refactor' },
    { title: 'Chore: clean up lint warnings', expected: '🧹 chore' },
    { title: 'Random improvement', expected: '🤖 unknown' },
    { title: '', expected: '🤖 unknown' },
    { title: null, expected: '🤖 unknown' }
  ];

  for (const { title, expected } of cases) {
    const result = computeLabel(title);
    assert.strictEqual(result, expected, `Title: "${title}" should map to "${expected}"`);
  }
  console.log('All tests passed.');
}

runTests();
