const assert = require('assert');
const { calculateDrift } = require('../src/chronoDrift');

// Mock rationale: We need a fixed point in time to ensure deterministic drift calculations.
// The Date object is mocked to return a consistent "now" for all test cases.
const mockDate = new Date('2023-10-27T10:00:00.000Z'); // A fixed UTC date for testing

/**
 * Helper function to run a test and report its status.
 * @param {string} name - The name of the test.
 * @param {Function} fn - The test function to execute.
 */
function runTest(name, fn) {
  try {
    fn();
    console.log(`✅ ${name}`);
  } catch (error) {
    console.error(`❌ ${name}`);
    console.error(error);
    process.exit(1); // Exit with error code on failure
  }
}

runTest('should calculate drift correctly for an even seed (positive adjustment)', () => {
  const seed = 10; // Even seed: (10 % 13) - 6 = 4; direction = 1. Adjustment: +4 seconds.
  const result = calculateDrift(seed, mockDate);
  assert.strictEqual(result.adjustmentSeconds, 4, 'Expected adjustment of +4 seconds');
  assert.strictEqual(result.adjustedTime.getTime(), mockDate.getTime() + 4 * 1000, 'Adjusted time should be +4 seconds');
  assert.ok(result.stabilityMessage.includes('Minor temporal ripples'), 'Expected minor ripples message');
});

runTest('should calculate drift correctly for an odd seed (negative adjustment)', () => {
  const seed = 11; // Odd seed: (11 % 13) - 6 = 5; direction = -1. Adjustment: -5 seconds.
  const result = calculateDrift(seed, mockDate);
  assert.strictEqual(result.adjustmentSeconds, -5, 'Expected adjustment of -5 seconds');
  assert.strictEqual(result.adjustedTime.getTime(), mockDate.getTime() - 5 * 1000, 'Adjusted time should be -5 seconds');
  assert.ok(result.stabilityMessage.includes('Significant chrono-distortion'), 'Expected significant distortion message');
});

runTest('should calculate drift correctly for a seed resulting in zero adjustment', () => {
  const seed = 6; // Even seed: (6 % 13) - 6 = 0; direction = 1. Adjustment: 0 seconds.
  const result = calculateDrift(seed, mockDate);
  assert.strictEqual(result.adjustmentSeconds, 0, 'Expected adjustment of 0 seconds');
  assert.strictEqual(result.adjustedTime.getTime(), mockDate.getTime(), 'Adjusted time should be unchanged');
  assert.ok(result.stabilityMessage.includes('remarkably stable'), 'Expected stable message');
});

runTest('should calculate drift correctly for a seed resulting in minimal adjustment (+1)', () => {
  const seed = 5; // Odd seed: (5 % 13) - 6 = -1; direction = -1. Adjustment: +1 second.
  const result = calculateDrift(seed, mockDate);
  assert.strictEqual(result.adjustmentSeconds, 1, 'Expected adjustment of +1 seconds');
  assert.ok(result.stabilityMessage.includes('remarkably stable'), 'Expected stable message for +1s');
});

runTest('should calculate drift correctly for a seed resulting in minimal adjustment (-1)', () => {
  const seed = 7; // Odd seed: (7 % 13) - 6 = 1; direction = -1. Adjustment: -1 second.
  const result = calculateDrift(seed, mockDate);
  assert.strictEqual(result.adjustmentSeconds, -1, 'Expected adjustment of -1 seconds');
  assert.ok(result.stabilityMessage.includes('remarkably stable'), 'Expected stable message for -1s');
});

console.log('\nAll tests for chronoDrift.js completed.\n');
