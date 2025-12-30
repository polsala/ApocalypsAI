import { generatePassphrase } from '../src/index';
import * as assert from 'assert';

// Mock Math.random to return a deterministic sequence
let mockValues = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9];
let callCount = 0;
const originalRandom = Math.random;
Math.random = () => {
  const val = mockValues[callCount % mockValues.length];
  callCount++;
  return val;
};

function resetMock() {
  callCount = 0;
}

// Test length, delimiter, and word selection
resetMock();
let result = generatePassphrase({ length: 3, delimiter: '-', emoji: false });
assert.strictEqual(result, 'alpha-bravo-charlie');

// Test emoji replacement
resetMock();
result = generatePassphrase({ length: 3, delimiter: '-', emoji: true });
assert.strictEqual(result, '🅰️-🥦-🐱');

// Restore original Math.random (optional, not needed in test runner)
Math.random = originalRandom;

console.log('All tests passed.');
