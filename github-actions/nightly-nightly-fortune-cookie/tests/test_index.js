const assert = require('assert');
const { getFortune } = require('../src/index');

// Mock rationale: we test a few seed values to ensure deterministic selection.
function testFortune(seed, expected) {
  const result = getFortune(seed);
  assert.strictEqual(result, expected, `Seed ${seed} should yield expected fortune`);
}

// Expected fortunes based on the array order in src/index.js
const expectedFortunes = [
  "You will find a hidden stash of snacks in the pantry.",
  "A sudden burst of inspiration will strike during your next coffee break.",
  "Beware of the mischievous squirrels; they plot in the shadows.",
  "Your code will compile on the first try—today is your lucky day.",
  "An unexpected compliment will brighten your afternoon.",
  "A stray cat will become your new debugging companion.",
  "The next commit you push will be praised by the gods of CI.",
  "A mysterious breeze will carry a hint of fresh ideas.",
  "Your keyboard will type itself for a moment—enjoy the surprise.",
  "A tiny victory today will lead to a grand triumph tomorrow."
];

// Test a range of seeds, including negative and large numbers.
[0, 1, 5, 9, 10, 11, -3, 12345].forEach(seed => {
  const idx = Math.abs(seed) % expectedFortunes.length;
  testFortune(seed, expectedFortunes[idx]);
});

console.log('All tests passed.');
