const assert = require('assert');
const { computeDecay } = require('../src/main');

// Helper for floating‑point comparison
function approxEqual(a, b, epsilon = 1e-12) {
  return Math.abs(a - b) < epsilon;
}

// Mock rationale: using known half‑life values to verify the formula.
// Test 1: Carbon‑14 after exactly one half‑life (5730 years) should be 0.5.
const resultC14 = computeDecay('C-14', 5730);
assert(approxEqual(resultC14, 0.5), 'C-14 after one half‑life should be 0.5');

// Test 2: Zero years elapsed → full activity (1.0).
assert.strictEqual(computeDecay('C-14', 0), 1, 'Zero years should yield full activity');

// Test 3: Unknown isotope should throw an error.
let threw = false;
try {
  computeDecay('X-99', 10);
} catch (e) {
  threw = true;
}
assert.strictEqual(threw, true, 'Unknown isotope should cause an exception');

console.log('All tests passed');
