const assert = require('assert');
const { computeBarterValue } = require('../src/index.js');

// Mock rationale: deterministic values based on known base values and rarity multipliers

function testSimple() {
  const items = [
    { name: 'canned-beans', qty: 10 },
    { name: 'water', qty: 5 }
  ];
  // canned-beans: 2 * 1 * 10 = 20
  // water: 3 * 1 * 5 = 15
  const result = computeBarterValue(items);
  assert.strictEqual(result, 35, 'Simple items total should be 35');
}

function testMixed() {
  const items = [
    { name: 'medicine', qty: 2 },   // 10 * 1.5 * 2 = 30
    { name: 'fuel', qty: 1 },       // 8 * 2 * 1 = 16
    { name: 'scrap-metal', qty: 4 } // 1 * 1 * 4 = 4
  ];
  const result = computeBarterValue(items);
  // Expected total: 30 + 16 + 4 = 50
  assert.strictEqual(result, 50, 'Mixed items total should be 50');
}

function testUnknownItem() {
  const items = [
    { name: 'unknown-item', qty: 3 } // defaults to base 1, common multiplier 1
  ];
  const result = computeBarterValue(items);
  assert.strictEqual(result, 3, 'Unknown item defaults to base 1 and common rarity');
}

function run() {
  try {
    testSimple();
    testMixed();
    testUnknownItem();
    console.log('All tests passed');
  } catch (e) {
    console.error('Test failed:', e.message);
    process.exit(1);
  }
}

run();
