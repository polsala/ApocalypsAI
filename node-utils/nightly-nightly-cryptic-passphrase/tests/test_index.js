const assert = require('assert');
const { generatePassphrase } = require('../src/index');

/**
 * Mock Math.random with a predefined sequence.
 * Returns a function that restores the original Math.random.
 */
function mockRandom(sequence) {
  const original = Math.random;
  let i = 0;
  Math.random = () => sequence[i++];
  return () => { Math.random = original; };
}

// Test: specific sequence should yield expected words.
const restore = mockRandom([0.1, 0.5, 0.9]); // indices: 2, 13, 23
const pass = generatePassphrase({ count: 3, delimiter: '_' });
restore();
assert.strictEqual(pass, 'cinder_nexus_xenon');

console.log('All tests passed');
