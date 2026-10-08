const assert = require('assert');
const { computeShares } = require('../src/index');

// Helper to compare objects shallowly
function objectsEqual(a, b) {
  const aKeys = Object.keys(a).sort();
  const bKeys = Object.keys(b).sort();
  if (aKeys.length !== bKeys.length) return false;
  for (let i = 0; i < aKeys.length; i++) {
    if (aKeys[i] !== bKeys[i]) return false;
    if (a[aKeys[i]] !== b[bKeys[i]]) return false;
  }
  return true;
}

// Test cases – deterministic because RNG is seeded with total+survivors
const cases = [
  { total: 100, survivors: 4, expected: { survivor1: 27, survivor2: 23, survivor3: 25, survivor4: 25 } },
  { total: 7, survivors: 3, expected: { survivor1: 3, survivor2: 2, survivor3: 2 } },
  { total: 0, survivors: 5, expected: { survivor1: 0, survivor2: 0, survivor3: 0, survivor4: 0, survivor5: 0 } },
];

cases.forEach(({ total, survivors, expected }) => {
  const result = computeShares(total, survivors);
  assert(objectsEqual(result, expected), `Failed for total=${total}, survivors=${survivors}`);
});

console.log('All tests passed.');
