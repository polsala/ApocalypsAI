// Tests for Nightly Supply Barter Calculator
const assert = require('assert');
const { getItemValue, totalValue, tradeWorth } = require('../src/index.js');

// Mock rationale: No external resources are accessed; all data is in-memory.

// Test item base values
assert.strictEqual(getItemValue('water'), 5, 'water base value should be 5');
assert.strictEqual(getItemValue('medicine'), 50, 'medicine base value should be 50');

// Test total value calculation
assert.strictEqual(totalValue('cannedFood', 3), 24, '3 cannedFood should equal 24');

// Test trade worth calculation
const trade = tradeWorth('water', 10, 'cannedFood', 5);
assert.strictEqual(trade.totalA, 50, '10 water total should be 50');
assert.strictEqual(trade.totalB, 40, '5 cannedFood total should be 40');
assert.strictEqual(trade.ratioAtoB, 1.25, 'ratio should be 1.25');

// Test unknown item handling
assert.throws(() => getItemValue('unknown'), /Unknown item/);

console.log('All tests passed.');
