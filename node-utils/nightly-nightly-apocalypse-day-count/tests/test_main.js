// Simple test runner using Node's built‑in assert module.
// No external dependencies; runs synchronously.

const assert = require('assert');
const { daysSinceApocalypse } = require('../src/main');

function runTests() {
  // Test: same day as apocalypse start
  assert.strictEqual(daysSinceApocalypse('2023-01-01'), 0, 'Start day should be 0');

  // Test: one day after start
  assert.strictEqual(daysSinceApocalypse('2023-01-02'), 1, 'One day after start should be 1');

  // Test: 31 days after start (end of January)
  assert.strictEqual(daysSinceApocalypse('2023-01-31'), 30, 'January 31 should be 30 days after start');

  // Test: leap year handling (2024-02-29)
  // Days from 2023‑01‑01 to 2024‑02‑29 = 424 days (including leap day)
  assert.strictEqual(daysSinceApocalypse('2024-02-29'), 424, 'Leap year calculation');

  // Test: date before apocalypse (should be negative)
  assert.strictEqual(daysSinceApocalypse('2022-12-31'), -1, 'Day before start should be -1');

  console.log('All tests passed.');
}

if (require.main === module) {
  // Mock rationale: tests are deterministic and run offline.
  runTests();
}
