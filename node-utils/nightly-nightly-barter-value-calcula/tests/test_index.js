// Nightly Barter Value Calculator â Tests
// No external dependencies; uses Node's builtâin assert.

const assert = require('assert');
const { calculateValue } = require('../src/index.js');

// Mock rationale: All test data are hardâcoded; no network or file I/O.

function runTests() {
  // Basic known values
  assert.strictEqual(calculateValue('water', 'good'), 10, 'water + good should be 10');
  assert.strictEqual(calculateValue('water', 'pristine'), 15, 'water + pristine should be 15');
  assert.strictEqual(calculateValue('water', 'worn'), 7, 'water + worn should be 7');
  assert.strictEqual(calculateValue('water', 'broken'), 3, 'water + broken should be 3');

  // Different item
  assert.strictEqual(calculateValue('ammo', 'worn'), 8, 'ammo + worn should be 8');
  assert.strictEqual(calculateValue('"first-aid kit"', 'pristine'), 45, 'firstâaid kit + pristine should be 45');

  // Caseâinsensitivity and whitespace handling
  assert.strictEqual(calculateValue('  WaTeR  ', '  GOOD  '), 10, 'whitespace & case should be ignored');

  // Unknown item / condition handling
  let threw = false;
  try {
    calculateValue('unknown-item', 'good');
  } catch (e) {
    threw = true;
    assert.strictEqual(e.message, 'Unknown item: unknown-item');
  }
  assert.ok(threw, 'Should throw on unknown item');

  threw = false;
  try {
    calculateValue('water', 'superb');
  } catch (e) {
    threw = true;
    assert.strictEqual(e.message, 'Unknown condition: superb');
  }
  assert.ok(threw, 'Should throw on unknown condition');

  console.log('All tests passed.');
}

runTests();
