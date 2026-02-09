import { computeKnapsack, Item } from '../src/index';
import assert from 'assert';

/**
 * Helper to compare two Item arrays for equality (order matters).
 */
function arraysEqual(a: Item[], b: Item[]): boolean {
  if (a.length !== b.length) return false;
  return a.every((item, i) => {
    const other = b[i];
    return item.name === other.name && item.weight === other.weight && item.value === other.value;
  });
}

// Mock rationale: deterministic test data representing a typical scavenger loot list.
const items: Item[] = [
  { name: 'Rusty Pipe', weight: 5, value: 3 },
  { name: 'Canned Beans', weight: 2, value: 4 },
  { name: 'Solar Battery', weight: 7, value: 10 },
  { name: 'Water Bottle', weight: 3, value: 5 }
];
const maxWeight = 10;

const result = computeKnapsack(items, maxWeight);

// Expected optimal selection: Canned Beans + Solar Battery (weight 9, value 14)
const expected: Item[] = [
  { name: 'Canned Beans', weight: 2, value: 4 },
  { name: 'Solar Battery', weight: 7, value: 10 }
];

assert(
  arraysEqual(result, expected),
  `Expected ${JSON.stringify(expected)} but got ${JSON.stringify(result)}`
);

console.log('All tests passed.');
