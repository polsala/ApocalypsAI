// nightly-radiation-calculator tests
// Run with: node tests/test_main.js

const assert = require('assert');
const { calculateSafeDistance } = require('../src/main');

function runTests() {
  // Test 1: typical value 0.5 sieverts => distance 2.00 meters
  const result1 = calculateSafeDistance(0.5);
  assert.strictEqual(result1, 2.00, '0.5 sieverts should yield 2.00 meters');

  // Test 2: smaller radiation 0.2 sieverts => distance ~3.16 meters
  const result2 = calculateSafeDistance(0.2);
  assert.strictEqual(result2, 3.16, '0.2 sieverts should yield 3.16 meters');

  // Test 3: larger radiation 1.0 sieverts => distance ~1.41 meters
  const result3 = calculateSafeDistance(1.0);
  assert.strictEqual(result3, 1.41, '1.0 sieverts should yield 1.41 meters');

  // Test 4: invalid input (zero) should throw
  assert.throws(() => calculateSafeDistance(0), /Sieverts must be a positive number/);

  // Test 5: invalid input (negative) should throw
  assert.throws(() => calculateSafeDistance(-0.3), /Sieverts must be a positive number/);

  console.log('All tests passed.');
}

runTests();
