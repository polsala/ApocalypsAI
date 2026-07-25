const assert = require('assert');
const { getDaysUntilNextFlare } = require('../src/index');

function daysBetween(start, end) {
  const diff = end - start;
  return Math.ceil(diff / (1000 * 60 * 60 * 24));
}

// Test 1: date before first flare
let current = new Date('2024-08-01T00:00:00Z');
let expected = daysBetween(current, new Date('2024-09-15T00:00:00Z'));
assert.strictEqual(
  getDaysUntilNextFlare(current),
  expected,
  'Should calculate days to 2024-09-15'
);

// Test 2: on a flare date (should skip to next flare)
current = new Date('2024-09-15T12:00:00Z'); // same day but after flare start
expected = daysBetween(current, new Date('2025-02-10T00:00:00Z'));
assert.strictEqual(
  getDaysUntilNextFlare(current),
  expected,
  'Should skip current flare and go to next'
);

// Test 3: after the last known flare
current = new Date('2027-01-01T00:00:00Z');
assert.strictEqual(
  getDaysUntilNextFlare(current),
  null,
  'Should return null when no upcoming flares'
);

console.log('All tests passed.');
