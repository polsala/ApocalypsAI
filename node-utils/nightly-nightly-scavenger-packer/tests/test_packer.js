const assert = require('assert');
const { packItems } = require('../src/packer');

// Mock rationale: deterministic small dataset
const items = [
  { name: 'Canned Beans', weight: 2, value: 3 },
  { name: 'Water Bottle', weight: 3, value: 4 },
  { name: 'First Aid Kit', weight: 5, value: 8 },
];

const result = packItems(items, 5);
// Expected optimal value is 7 (Canned Beans + Water Bottle)
assert.deepStrictEqual(result, ['Canned Beans', 'Water Bottle']);

console.log('All tests passed.');
