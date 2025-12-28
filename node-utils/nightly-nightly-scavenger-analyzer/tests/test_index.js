const assert = require('assert');
const { analyzeInventory } = require('../src/index');

// Mock rationale: deterministic sample data
const sampleItems = [
  { name: 'Rusty Spoon', weight: 0.2, rarity: 'common' },
  { name: 'Old Book', weight: 0.5, rarity: 'uncommon' },
  { name: 'Ancient Relic', weight: 2.5, rarity: 'epic' },
  { name: 'Scrap Metal', weight: 1.0, rarity: 'common' }
];

const expected = {
  totalItems: 4,
  totalWeight: 4.2,
  rarityCounts: { common: 2, uncommon: 1, epic: 1 }
};

const result = analyzeInventory(sampleItems);
assert.deepStrictEqual(result, expected);
console.log('All tests passed.');
