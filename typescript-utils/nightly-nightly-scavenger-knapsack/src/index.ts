type Item = {
  name: string;
  weight: number;
  value: number;
};

/**
 * Solve the 0/1 knapsack problem.
 * @param items   Array of loot items.
 * @param maxWeight Maximum weight the scavenger can carry.
 * @returns       Subset of items yielding maximal total value without exceeding maxWeight.
 */
function computeKnapsack(items: Item[], maxWeight: number): Item[] {
  const n = items.length;
  // dp[i][w] = max value using first i items with weight limit w
  const dp: number[][] = Array.from({ length: n + 1 }, () => Array(maxWeight + 1).fill(0));

  for (let i = 1; i <= n; i++) {
    const { weight, value } = items[i - 1];
    for (let w = 0; w <= maxWeight; w++) {
      if (weight > w) {
        dp[i][w] = dp[i - 1][w];
      } else {
        dp[i][w] = Math.max(dp[i - 1][w], dp[i - 1][w - weight] + value);
      }
    }
  }

  // Backtrack to find selected items
  let w = maxWeight;
  const selected: Item[] = [];
  for (let i = n; i > 0; i--) {
    if (dp[i][w] !== dp[i - 1][w]) {
      const item = items[i - 1];
      selected.push(item);
      w -= item.weight;
    }
  }
  return selected.reverse();
}

// CLI entry point
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length < 2) {
    console.error('Usage: ts-node src/index.ts <loot.json> <maxWeight>');
    process.exit(1);
  }
  const [filePath, maxWeightStr] = args;
  const maxWeight = parseInt(maxWeightStr, 10);
  const fs = require('fs');
  let raw: string;
  try {
    raw = fs.readFileSync(filePath, 'utf-8');
  } catch (e: any) {
    console.error('Failed to read file:', e.message);
    process.exit(1);
  }
  let items: Item[];
  try {
    items = JSON.parse(raw);
  } catch (e: any) {
    console.error('Invalid JSON:', e.message);
    process.exit(1);
  }
  const selected = computeKnapsack(items, maxWeight);
  const totalWeight = selected.reduce((sum, i) => sum + i.weight, 0);
  const totalValue = selected.reduce((sum, i) => sum + i.value, 0);
  console.log('Selected items:');
  selected.forEach(i => console.log(`- ${i.name} (weight: ${i.weight}, value: ${i.value})`));
  console.log(`Total weight: ${totalWeight}`);
  console.log(`Total value: ${totalValue}`);
}

export { computeKnapsack, Item };
