const assert = require('assert');
const { nextWaterDate } = require('../src/index');

// Mock rationale: deterministic dates, no external calls
// Test 1: simple addition
assert.strictEqual(nextWaterDate('2023-09-01', 3), '2023-09-04');

// Test 2: month rollover
assert.strictEqual(nextWaterDate('2023-01-30', 5), '2023-02-04');

// Test 3: zero interval
assert.strictEqual(nextWaterDate('2023-12-31', 0), '2023-12-31');

// Test 4: invalid date throws
let threw = false;
try {
  nextWaterDate('invalid-date', 2);
} catch (e) {
  threw = true;
}
assert.strictEqual(threw, true);

// Test 5: negative interval throws
threw = false;
try {
  nextWaterDate('2023-01-01', -1);
} catch (e) {
  threw = true;
}
assert.strictEqual(threw, true);

console.log('All tests passed');
