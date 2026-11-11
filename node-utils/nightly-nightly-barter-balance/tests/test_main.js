// Mock rationale: Tests run offline, no external resources are needed.
const assert = require('assert');
const { suggest } = require('../src/main');

function runTests() {
  // Test 1: Imbalanced trade should produce a suggestion
  const result1 = suggest('water', 10, 'ammo', 5);
  assert.strictEqual(result1.balanced, false, 'Expected trade to be imbalanced');
  assert.ok(result1.suggestion.includes('Add'), 'Expected suggestion to advise adding items');

  // Test 2: Balanced trade detection
  const result2 = suggest('water', 5, 'canned_food', 5);
  assert.strictEqual(result2.balanced, true, 'Expected trade to be balanced');
  assert.strictEqual(result2.suggestion, 'The trade is already balanced.', 'Expected balanced suggestion');

  console.log('All barter‑balance tests passed');
}

runTests();
