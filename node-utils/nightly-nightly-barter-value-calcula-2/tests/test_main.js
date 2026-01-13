// Nightly Barter Value Calculator Tests
// Mock rationale: using Node's builtâin assert for deterministic offline testing.

const assert = require('assert');
const { calculateValue } = require('../src/main');

// Test known items
assert.strictEqual(calculateValue('water', 3), 30, 'water x3 should be 30');
assert.strictEqual(calculateValue('Food', 2), 16, 'Food caseâinsensitive');

// Test invalid item
let threw = false;
try {
  calculateValue('gold', 1);
} catch (e) {
  threw = true;
  assert.strictEqual(e.message, 'Unknown item: gold');
}
assert.ok(threw, 'should throw on unknown item');

// Test invalid quantity
threw = false;
try {
  calculateValue('ammo', 0);
} catch (e) {
  threw = true;
  assert.strictEqual(e.message, 'Quantity must be a positive integer');
}
assert.ok(threw, 'should throw on nonâpositive quantity');

console.log('All tests passed.');
