const assert = require('assert');
const {calculateBarterValues} = require('../src/barter');

// Mock rationale: deterministic inputs for reproducible testing
const items = [
  {name: 'canned beans', baseValue: 10, scarcity: 0.8},
  {name: 'water bottle', baseValue: 5, scarcity: 0.3},
  {name: 'medkit', baseValue: 20, scarcity: 0.0}
];

const expected = [
  {name: 'canned beans', adjustedValue: 11},
  {name: 'water bottle', adjustedValue: 6.75},
  {name: 'medkit', adjustedValue: 30}
];

const result = calculateBarterValues(items);
assert.deepStrictEqual(result, expected);
console.log('All tests passed');
