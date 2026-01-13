import { strict as assert } from 'assert';
import { knapsack, Item } from '../src/main';

const items: Item[] = [
  { name: 'Canned Beans', weight: 2, value: 3 },
  { name: 'Water Bottle', weight: 3, value: 4 },
  { name: 'First Aid Kit', weight: 5, value: 10 },
];

const capacity = 5;
const result = knapsack(items, capacity);

// Expected optimal subset is the First Aid Kit (value 10) vs Beans+Water (value 7)
assert.deepEqual(result, [{ name: 'First Aid Kit', weight: 5, value: 10 }]);

console.log('All tests passed.');
