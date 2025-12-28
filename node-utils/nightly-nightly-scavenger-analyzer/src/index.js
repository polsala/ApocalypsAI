#!/usr/bin/env node
const fs = require('fs');

function analyzeInventory(items) {
  const summary = {
    totalItems: items.length,
    totalWeight: 0,
    rarityCounts: {}
  };
  for (const item of items) {
    const w = Number(item.weight) || 0;
    summary.totalWeight += w;
    const rarity = item.rarity || 'unknown';
    summary.rarityCounts[rarity] = (summary.rarityCounts[rarity] || 0) + 1;
  }
  // round weight to 2 decimals
  summary.totalWeight = Math.round(summary.totalWeight * 100) / 100;
  return summary;
}

// CLI handling
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length !== 1) {
    console.error('Usage: node src/index.js <path-to-json>');
    process.exit(1);
  }
  const filePath = args[0];
  try {
    const data = fs.readFileSync(filePath, 'utf8');
    const items = JSON.parse(data);
    const result = analyzeInventory(items);
    console.log(JSON.stringify(result, null, 2));
  } catch (err) {
    console.error('Error:', err.message);
    process.exit(1);
  }
}

module.exports = { analyzeInventory };
