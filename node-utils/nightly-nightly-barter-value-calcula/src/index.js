// Nightly Barter Value Calculator
// SPDX-License-Identifier: MIT

/**
 * Base barter values for known items (in scrap).
 * Values are intentionally whimsical but balanced for fun.
 */
const BASE_VALUES = {
  water: 10,
  "first-aid kit": 30,
  ammo: 12,
  "canned food": 8,
  "fuel canister": 20,
  "scrap metal": 5,
  "tool kit": 15,
  "radiation suit": 50
};

/**
 * Condition multipliers.
 * pristine > good > worn > broken
 */
const CONDITION_MULTIPLIERS = {
  pristine: 1.5,
  good: 1.0,
  worn: 0.7,
  broken: 0.3
};

/**
 * Normalises a string: trims, lowerâcases, collapses spaces.
 */
function normalise(str) {
  return str.trim().toLowerCase().replace(/\s+/g, ' ');
}

/**
 * Calculates the barter value for a given item and condition.
 * @param {string} item - Name of the item (e.g., "water").
 * @param {string} condition - One of: pristine, good, worn, broken.
 * @returns {number} - Rounded integer value in scrap.
 * @throws {Error} If the item or condition is unknown.
 */
function calculateValue(item, condition) {
  const normItem = normalise(item);
  const normCond = normalise(condition);

  if (!BASE_VALUES.hasOwnProperty(normItem)) {
    throw new Error(`Unknown item: ${item}`);
  }
  if (!CONDITION_MULTIPLIERS.hasOwnProperty(normCond)) {
    throw new Error(`Unknown condition: ${condition}`);
  }

  const base = BASE_VALUES[normItem];
  const multiplier = CONDITION_MULTIPLIERS[normCond];
  const raw = base * multiplier;
  return Math.round(raw);
}

// CLI handling â only when executed directly
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length < 2) {
    console.error('Usage: node src/index.js <item> <condition>');
    process.exit(1);
  }
  const [item, condition] = args;
  try {
    const value = calculateValue(item, condition);
    console.log(`Barter value for "${item}" (${condition}): ${value} scrap`);
  } catch (e) {
    console.error(e.message);
    process.exit(1);
  }
}

module.exports = { calculateValue };
