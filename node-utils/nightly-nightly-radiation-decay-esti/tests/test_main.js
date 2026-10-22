// Nightly Radiation Decay Estimator – Tests
// No external dependencies; uses Node's built‑in assert module.

const assert = require('assert');
const { estimateDecay } = require('../src/main');

// Mock rationale: These tests cover known half‑life scenarios using exact math.

function approxEqual(actual, expected, epsilon = 1e-10) {
  assert.ok(Math.abs(actual - expected) < epsilon, `Expected ${expected}, got ${actual}`);
}

// Test 1: Zero years should return 1 (no decay)
approxEqual(estimateDecay('U-235', 0), 1);

// Test 2: One half‑life elapsed → 0.5 remaining
approxEqual(estimateDecay('C-14', 5730), 0.5);

// Test 3: Two half‑lives → 0.25 remaining
approxEqual(estimateDecay('C-14', 11460), 0.25);

// Test 4: Fractional years (half of a half‑life)
approxEqual(estimateDecay('C-14', 2865), Math.sqrt(0.5));

// Test 5: Unknown isotope should throw
let threw = false;
try {
  estimateDecay('X-999', 100);
} catch (e) {
  threw = true;
  assert.strictEqual(e.message, 'Unknown isotope: X-999');
}
assert.ok(threw, 'Expected error for unknown isotope');

// Test 6: Negative years should throw
threw = false;
try {
  estimateDecay('U-235', -5);
} catch (e) {
  threw = true;
  assert.strictEqual(e.message, 'Years must be a non‑negative number');
}
assert.ok(threw, 'Expected error for negative years');

console.log('All tests passed.');
