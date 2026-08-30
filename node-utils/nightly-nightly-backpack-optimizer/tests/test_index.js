const assert = require('assert');
const { solveKnapsack } = require('../src/index');

function deepSort(arr) {
  return arr.map(i => ({...i})).sort((a, b) => a.name.localeCompare(b.name));
}

// Test case from README
const items = [
  {name: 'water', weight: 3, value: 5},
  {name: 'food', weight: 4, value: 6},
  {name: 'radio', weight: 2, value: 2}
];
const capacity = 10;
const expected = [
  {name: 'water', weight: 3, value: 5},
  {name: 'food', weight: 4, value: 6}
];
const result = solveKnapsack(items, capacity);
assert.deepStrictEqual(deepSort(result), deepSort(expected), 'Knapsack should select water and food');

console.log('All tests passed');
