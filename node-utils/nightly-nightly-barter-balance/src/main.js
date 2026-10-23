#!/usr/bin/env node

/**
 * nightly-barter-balance
 * ----------------------
 * A whimsical yet practical CLI that evaluates the fairness of a trade
 * between two post‑apocalypse supplies.
 *
 * Each item has a *rarity* (1‑5) and a *utility* (1‑5). The product of the two
 * yields the item’s intrinsic value. The tool compares the total value of the
 * two sides and, if they differ, suggests the minimal number of additional
 * items required to achieve balance.
 */

const items = {
  water: { rarity: 1, utility: 5 },
  canned_food: { rarity: 2, utility: 4 },
  ammo: { rarity: 3, utility: 3 },
  medicine: { rarity: 4, utility: 5 },
  fuel: { rarity: 5, utility: 2 }
};

/** Compute the intrinsic value of a single unit of an item */
function unitValue(item) {
  const data = items[item];
  if (!data) {
    throw new Error(`Unknown item: ${item}`);
  }
  return data.rarity * data.utility;
}

/** Compute total value for a given quantity */
function totalValue(item, qty) {
  return unitValue(item) * qty;
}

/**
 * Suggest a trade adjustment.
 * @param {string} itemA - Name of first item
 * @param {number} qtyA - Quantity offered of first item
 * @param {string} itemB - Name of second item
 * @param {number} qtyB - Quantity offered of second item
 * @returns {object} { balanced: boolean, diff: number, suggestion: string }
 */
function suggest(itemA, qtyA, itemB, qtyB) {
  const valA = totalValue(itemA, qtyA);
  const valB = totalValue(itemB, qtyB);
  const diff = Math.abs(valA - valB);
  const balanced = diff === 0;
  let suggestion = '';
  if (!balanced) {
    // Determine which side is weaker and how many of that item are needed
    if (valA < valB) {
      const needed = Math.ceil(diff / unitValue(itemA));
      suggestion = `Add ${needed} more ${itemA}(s) to side A.`;
    } else {
      const needed = Math.ceil(diff / unitValue(itemB));
      suggestion = `Add ${needed} more ${itemB}(s) to side B.`;
    }
  } else {
    suggestion = 'The trade is already balanced.';
  }
  return { balanced, diff, suggestion };
}

/** CLI entry point */
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length !== 4) {
    console.error('Usage: node src/main.js <item1> <qty1> <item2> <qty2>');
    process.exit(1);
  }
  const [itemA, qtyAStr, itemB, qtyBStr] = args;
  const qtyA = parseInt(qtyAStr, 10);
  const qtyB = parseInt(qtyBStr, 10);
  try {
    const result = suggest(itemA, qtyA, itemB, qtyB);
    console.log('--- Trade Evaluation ---');
    console.log(`Side A: ${qtyA} ${itemA} (value ${totalValue(itemA, qtyA)})`);
    console.log(`Side B: ${qtyB} ${itemB} (value ${totalValue(itemB, qtyB)})`);
    console.log(result.balanced ? '✅ Balanced trade!' : '⚖️ Imbalance detected');
    console.log('Suggestion:', result.suggestion);
  } catch (e) {
    console.error('Error:', e.message);
    process.exit(1);
  }
}

module.exports = { suggest, items };
