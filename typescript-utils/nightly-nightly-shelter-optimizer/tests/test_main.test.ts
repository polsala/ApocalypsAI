// Mock rationale: deterministic test data, no external I/O
import { solveKnapsack, Item, KnapsackResult } from '../src/main';

function assert(condition: boolean, message: string): void {
  if (!condition) {
    throw new Error('Assertion failed: ' + message);
  }
}

// Test case: simple known optimal solution
const items: Item[] = [
  { name: 'Canned Beans', weight: 5, value: 10 },
  { name: 'Water Bottle', weight: 10, value: 15 },
  { name: 'First‑Aid Kit', weight: 8, value: 25 },
  { name: 'Radio', weight: 12, value: 20 }
];
const capacity = 20;

const result: KnapsackResult = solveKnapsack(items, capacity);

// Expected optimal selection: First‑Aid Kit (8,25) + Canned Beans (5,10) + Water Bottle (10,15) would exceed 20.
// Best is First‑Aid Kit (8,25) + Radio (12,20) = weight 20, value 45.
assert(result.totalWeight === 20, `Expected totalWeight 20, got ${result.totalWeight}`);
assert(result.totalValue === 45, `Expected totalValue 45, got ${result.totalValue}`);
const selectedNames = result.selected.map(it => it.name).sort();
assert(selectedNames.length === 2, `Expected 2 selected items, got ${selectedNames.length}`);
assert(selectedNames.includes('First‑Aid Kit'), 'First‑Aid Kit should be selected');
assert(selectedNames.includes('Radio'), 'Radio should be selected');

console.log('All tests passed.');

