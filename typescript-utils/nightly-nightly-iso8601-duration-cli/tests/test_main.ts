import { parseDuration } from '../src/index';
import * as assert from 'assert';

// Mock rationale: these tests cover typical, edge‑case, and minimal inputs.

function runTests() {
  // Full duration
  assert.strictEqual(
    parseDuration('P1Y2M3DT4H5M6S'),
    '1 year, 2 months, 3 days, 4 hours, 5 minutes, 6 seconds'
  );

  // Time‑only
  assert.strictEqual(parseDuration('PT20M'), '20 minutes');

  // Date‑only (weeks)
  assert.strictEqual(parseDuration('P3W'), '3 weeks');

  // Zero components (just "P")
  assert.strictEqual(parseDuration('P'), '0 seconds');

  // Fractional seconds
  assert.strictEqual(parseDuration('PT0.5S'), '0.5 seconds');

  // Invalid input should throw
  let threw = false;
  try {
    parseDuration('invalid');
  } catch (e) {
    threw = true;
  }
  assert.ok(threw, 'Expected error for malformed input');

  console.log('All tests passed.');
}

if (require.main === module) {
  runTests();
}
