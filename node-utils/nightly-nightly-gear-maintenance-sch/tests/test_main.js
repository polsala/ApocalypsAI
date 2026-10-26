const assert = require('assert');
const { computeSchedule } = require('../src/main');

// Mock rationale: deterministic input representing typical survivor gear
const mockItems = [
  { name: 'Radiation Suit', durability: 85 },
  { name: 'Water Filter', durability: 45 },
  { name: 'Plasma Rifle', durability: 20 }
];

const expected = [
  { name: 'Plasma Rifle', durability: 20, action: 'Repair ASAP' },
  { name: 'Water Filter', durability: 45, action: 'Inspect soon' },
  { name: 'Radiation Suit', durability: 85, action: 'Good' }
];

const result = computeSchedule(mockItems);
assert.deepStrictEqual(result, expected);
console.log('All tests passed');
