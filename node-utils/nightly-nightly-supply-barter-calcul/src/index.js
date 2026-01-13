#!/usr/bin/env node
// Nightly Supply Barter Calculator
// Computes trade values between items based on rarity and utility.

const items = {
  water: { rarity: 1, utility: 5 },
  cannedFood: { rarity: 2, utility: 4 },
  medicine: { rarity: 5, utility: 10 },
  ammo: { rarity: 3, utility: 6 },
  fuel: { rarity: 4, utility: 8 }
};

function getItemValue(name) {
  const item = items[name];
  if (!item) {
    throw new Error(`Unknown item: ${name}`);
  }
  return item.rarity * item.utility;
}

function totalValue(name, qty) {
  return getItemValue(name) * Number(qty);
}

/**
 * Calculates trade totals for two items.
 * Returns an object { totalA, totalB, ratioAtoB } where ratioAtoB = totalA / totalB.
 */
function tradeWorth(itemA, qtyA, itemB, qtyB) {
  const totalA = totalValue(itemA, qtyA);
  const totalB = totalValue(itemB, qtyB);
  const ratioAtoB = totalA / totalB;
  return { totalA, totalB, ratioAtoB };
}

// CLI handling
if (require.main === module) {
  const [,, itemA, qtyA, itemB, qtyB] = process.argv;
  if (!itemA || !qtyA || !itemB || !qtyB) {
    console.error('Usage: node src/index.js <itemA> <qtyA> <itemB> <qtyB>');
    process.exit(1);
  }
  try {
    const { totalA, totalB, ratioAtoB } = tradeWorth(itemA, qtyA, itemB, qtyB);
    console.log(`Trade ratio: ${totalA} (${itemA}) vs ${totalB} (${itemB})`);
    console.log(`1 ${itemA} â ${(1/ratioAtoB).toFixed(2)} ${itemB}`);
  } catch (e) {
    console.error(e.message);
    process.exit(1);
  }
}

// Export for tests
module.exports = { getItemValue, totalValue, tradeWorth };
