const assert = require('assert');
const { intToRoman, romanToInt } = require('../src/roman.js');

// intToRoman tests
assert.strictEqual(intToRoman(1), 'I');
assert.strictEqual(intToRoman(4), 'IV');
assert.strictEqual(intToRoman(9), 'IX');
assert.strictEqual(intToRoman(58), 'LVIII');
assert.strictEqual(intToRoman(1994), 'MCMXCIV');

// romanToInt tests
assert.strictEqual(romanToInt('I'), 1);
assert.strictEqual(romanToInt('IV'), 4);
assert.strictEqual(romanToInt('IX'), 9);
assert.strictEqual(romanToInt('LVIII'), 58);
assert.strictEqual(romanToInt('MCMXCIV'), 1994);

// Round‑trip verification for the full range (1‑3999)
for (let i = 1; i <= 3999; i++) {
  const roman = intToRoman(i);
  const back = romanToInt(roman);
  assert.strictEqual(back, i);
}

console.log('All tests passed');
