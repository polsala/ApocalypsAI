#!/usr/bin/env node

const fs = require('fs');

// Base barter values for known supplies
const baseValues = {
  "canned-beans": 2,
  "water": 3,
  "medicine": 10,
  "ammo": 5,
  "fuel": 8,
  "scrap-metal": 1,
  "electronics": 7
};

// Rarity multipliers
const rarityMultipliers = {
  "common": 1,
  "uncommon": 1.5,
  "rare": 2,
  "legendary": 5
};

// Simple mapping of item -> rarity
const rarityMap = {
  "canned-beans": "common",
  "water": "common",
  "medicine": "uncommon",
  "ammo": "uncommon",
  "fuel": "rare",
  "scrap-metal": "common",
  "electronics": "rare"
};

function getItemValue(name, qty) {
  const base = baseValues[name] !== undefined ? baseValues[name] : 1;
  const rarity = rarityMap[name] || "common";
  const multiplier = rarityMultipliers[rarity] || 1;
  return base * multiplier * qty;
}

function computeBarterValue(items) {
  if (!Array.isArray(items)) {
    throw new Error("Items must be an array");
  }
  return items.reduce((sum, item) => {
    const name = item.name;
    const qty = Number(item.qty);
    if (!name || isNaN(qty)) {
      throw new Error("Invalid item format");
    }
    return sum + getItemValue(name, qty);
  }, 0);
}

// CLI handling
function main() {
  let input = '';
  if (process.argv.length > 2) {
    // JSON string supplied as first argument after script name
    input = process.argv[2];
  } else {
    // Read from STDIN (file descriptor 0)
    input = fs.readFileSync(0, 'utf-8');
  }
  try {
    const items = JSON.parse(input);
    const total = computeBarterValue(items);
    console.log(`Total barter value: ${total}`);
  } catch (e) {
    console.error('Error:', e.message);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { computeBarterValue };
