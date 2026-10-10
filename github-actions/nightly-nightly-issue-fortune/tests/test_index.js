// Mock rationale: we replace Math.random to make the test deterministic.
const assert = require('assert');
const { getFortune } = require('../src/index.js');

// Preserve original Math.random
const originalRandom = Math.random;

// Mock Math.random to always return 0 (first fortune)
Math.random = () => 0;

const firstFortune = getFortune();
assert.strictEqual(
  firstFortune,
  "You will find a hidden stash of snacks in the breakroom.",
  'Expected the first fortune when Math.random returns 0'
);

// Mock Math.random to return 0.9999 (last fortune)
Math.random = () => 0.9999;
const lastFortune = getFortune();
assert.strictEqual(
  lastFortune,
  "A mysterious log will reveal a hidden truth.",
  'Expected the last fortune when Math.random is near 1'
);

// Restore original Math.random
Math.random = originalRandom;

console.log('All tests passed.');
