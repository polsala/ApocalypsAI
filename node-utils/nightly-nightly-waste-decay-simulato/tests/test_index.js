const { calculateRemaining } = require('../src/index');
const assert = require('assert');

// Mock rationale: deterministic values based on pure math, no external dependencies.

function approxEqual(a, b, epsilon = 1e-2) {
  return Math.abs(a - b) < epsilon;
}

// Test 1: zero days -> same amount
assert.strictEqual(calculateRemaining(100, 30, 0), 100);

// Test 2: one half‑life
assert.ok(approxEqual(calculateRemaining(200, 10, 10), 100));

// Test 3: two half‑lives
assert.ok(approxEqual(calculateRemaining(500, 5, 10), 125));

// Test 4: non‑integer days
assert.ok(approxEqual(calculateRemaining(1000, 20, 30), 353.55));

// Test error handling
assert.throws(() => calculateRemaining(100, 0, 10), /Half‑life must be positive/);
assert.throws(() => calculateRemaining(-50, 10, 5), /Initial amount cannot be negative/);

console.log('All tests passed.');
