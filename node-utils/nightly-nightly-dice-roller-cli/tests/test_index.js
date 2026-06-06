const assert = require('assert');
const crypto = require('crypto');
const { parseNotation, rollDice } = require('../src/index');

// Helper to temporarily mock crypto.randomInt
function withMockedRandomInt(mockValues, fn) {
  const original = crypto.randomInt;
  let i = 0;
  crypto.randomInt = (min, max) => {
    // Return predetermined value; ignore min/max for simplicity
    const val = mockValues[i++];
    return val;
  };
  try {
    fn();
  } finally {
    crypto.randomInt = original;
  }
}

// Test parseNotation
assert.deepStrictEqual(parseNotation('d20'), { count: 1, sides: 20, modifier: 0 });
assert.deepStrictEqual(parseNotation('3d8+2'), { count: 3, sides: 8, modifier: 2 });
assert.deepStrictEqual(parseNotation('4d6-1'), { count: 4, sides: 6, modifier: -1 });

// Test rollDice with mocked randomness (2d6 => values 2 and 5)
withMockedRandomInt([2, 5], () => {
  const spec = { count: 2, sides: 6 };
  const total = rollDice(spec);
  assert.strictEqual(total, 7); // 2 + 5
});

console.log('All tests passed.');
