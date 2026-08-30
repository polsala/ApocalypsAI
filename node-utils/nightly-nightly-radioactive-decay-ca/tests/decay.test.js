const assert = require('assert');
const { calculateRemaining } = require('../src/decay');

// Mock rationale: deterministic values, no external dependencies

// Test 1: No time elapsed -> same amount
assert.strictEqual(calculateRemaining(100, 30, 0), 100);

// Test 2: One half‑life elapsed -> half amount
assert.strictEqual(calculateRemaining(200, 10, 10), 100);

// Test 3: Two half‑lives elapsed -> quarter amount
assert.strictEqual(calculateRemaining(80, 5, 10), 20);

// Test 4: Non‑integer result (three half‑lives)
const result = calculateRemaining(100, 30, 90); // 3 * 30 = three half‑lives => 12.5
assert.strictEqual(result, 12.5);

console.log('All tests passed');
