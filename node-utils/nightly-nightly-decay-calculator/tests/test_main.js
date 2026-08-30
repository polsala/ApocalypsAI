const assert = require('assert');
const { computeDecay } = require('../src/index.js');

/** Helper for approximate equality */
function approxEqual(a, b, epsilon = 1e-6) {
  return Math.abs(a - b) < epsilon;
}

// No decay (elapsed time = 0)
assert.strictEqual(computeDecay(1000, 30, 0), 1000);

// One half‑life
assert.ok(approxEqual(computeDecay(1000, 30, 30), 500));

// Three half‑lives
assert.ok(approxEqual(computeDecay(1000, 30, 90), 125));

// Fractional time (half of a half‑life)
assert.ok(approxEqual(computeDecay(200, 10, 5), 200 * Math.pow(0.5, 0.5)));

console.log('All tests passed.');
