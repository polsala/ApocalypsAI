#!/usr/bin/env node
/**
 * Nightly Barter Value Calculator
 * Calculates barter points for items based on predefined scores.
 */

const ITEMS = {
  water: 10,
  food: 8,
  medicine: 15,
  ammo: 12,
  fuel: 14,
  tools: 9,
  scrap: 5
};

/**
 * Calculate total barter value.
 * @param {string} item - Item name (caseâinsensitive).
 * @param {number} qty - Quantity (positive integer).
 * @returns {number} total value.
 * @throws {Error} if item unknown or qty invalid.
 */
function calculateValue(item, qty) {
  if (!item || typeof item !== 'string') {
    throw new Error('Item must be a nonâempty string');
  }
  const key = item.toLowerCase();
  if (!Object.prototype.hasOwnProperty.call(ITEMS, key)) {
    throw new Error(`Unknown item: ${item}`);
  }
  const quantity = Number(qty);
  if (!Number.isInteger(quantity) || quantity <= 0) {
    throw new Error('Quantity must be a positive integer');
  }
  return ITEMS[key] * quantity;
}

// CLI handling
if (require.main === module) {
  const [,, itemArg, qtyArg] = process.argv;
  try {
    const value = calculateValue(itemArg, qtyArg);
    console.log(`${qtyArg} units of ${itemArg} are worth ${value} barter points.`);
  } catch (e) {
    console.error('Error:', e.message);
    process.exit(1);
  }
}

module.exports = { calculateValue };
