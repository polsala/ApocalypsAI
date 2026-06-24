#!/usr/bin/env node
/**
 * nightly-backpack-optimizer
 * 0/1 knapsack implementation for survival gear.
 */

function solveKnapsack(items, capacity) {
  const n = items.length;
  // DP table
  const dp = Array.from({ length: n + 1 }, () => Array(capacity + 1).fill(0));
  for (let i = 1; i <= n; i++) {
    const { weight, value } = items[i - 1];
    for (let w = 0; w <= capacity; w++) {
      if (weight > w) {
        dp[i][w] = dp[i - 1][w];
      } else {
        dp[i][w] = Math.max(dp[i - 1][w], dp[i - 1][w - weight] + value);
      }
    }
  }
  // backtrack to find selected items
  const selected = [];
  let w = capacity;
  for (let i = n; i > 0; i--) {
    if (dp[i][w] !== dp[i - 1][w]) {
      const item = items[i - 1];
      selected.push(item);
      w -= item.weight;
    }
  }
  return selected.reverse(); // preserve original order
}

// CLI handling
if (require.main === module) {
  const args = process.argv.slice(2);
  const getArg = (flag) => {
    const idx = args.indexOf(flag);
    if (idx !== -1 && idx + 1 < args.length) {
      return args[idx + 1];
    }
    return null;
  };
  const limitStr = getArg('--limit');
  const itemsStr = getArg('--items');
  if (!limitStr || !itemsStr) {
    console.error('Usage: node src/index.js --limit <number> --items <json-array>');
    process.exit(1);
  }
  const limit = parseInt(limitStr, 10);
  let items;
  try {
    items = JSON.parse(itemsStr);
  } catch (e) {
    console.error('Failed to parse items JSON:', e.message);
    process.exit(1);
  }
  const result = solveKnapsack(items, limit);
  console.log(JSON.stringify(result, null, 2));
}

// Export for tests
module.exports = { solveKnapsack };
