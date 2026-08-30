const assert = require('assert');
const { computeDecay, halfLives } = require('../src/index.js');

// Helper for approximate equality
function approxEqual(a, b, epsilon = 1e-6) {
  return Math.abs(a - b) < epsilon;
}

// Test known half-life: Cs-137 should halve activity after its half‑life
(function testCs137HalfLife() {
  const result = computeDecay('Cs-137', 1000, halfLives['Cs-137']);
  assert(approxEqual(result, 500), `Cs-137 half‑life test failed: ${result}`);
})();

// Test I-131 with its ~0.0219‑year half‑life
(function testI131() {
  const result = computeDecay('I-131', 200, 0.0219);
  // After one half‑life, activity should be ~100 Bq
  assert(approxEqual(result, 100, 0.1), `I-131 test failed: ${result}`);
})();

// Test that an unknown isotope throws an error
(function testUnknownIsotope() {
  let threw = false;
  try {
    computeDecay('X-999', 100, 1);
  } catch (e) {
    threw = true;
  }
  assert(threw, 'Expected error for unknown isotope');
})();

console.log('All tests passed.');
