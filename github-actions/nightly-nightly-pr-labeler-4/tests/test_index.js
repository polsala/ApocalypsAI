// Simple test runner â no external test framework required
const assert = require('assert');
const { getLabelsForTitle } = require('../src/index');

function test(description, fn) {
  try {
    fn();
    console.log(`â ${description}`);
  } catch (err) {
    console.error(`â ${description}`);
    console.error(err);
    process.exitCode = 1;
  }
}

// Mock rationale: deterministic, no network calls
const mapping = {
  bug: 'bug',
  feat: 'feature',
  doc: 'documentation'
};

test('Single keyword match', () => {
  const labels = getLabelsForTitle('Fix critical bug in parser', mapping);
  assert.deepStrictEqual(labels, ['bug']);
});

test('Multiple keyword matches (order preserved)', () => {
  const labels = getLabelsForTitle('Add new feat and update docs', mapping);
  assert.deepStrictEqual(labels, ['feature', 'documentation']);
});

test('Caseâinsensitive matching', () => {
  const labels = getLabelsForTitle('DOC: improve readme', mapping);
  assert.deepStrictEqual(labels, ['documentation']);
});

test('No matches yields empty array', () => {
  const labels = getLabelsForTitle('Refactor codebase', mapping);
  assert.deepStrictEqual(labels, []);
});
