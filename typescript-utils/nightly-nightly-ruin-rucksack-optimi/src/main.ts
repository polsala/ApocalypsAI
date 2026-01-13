import * as fs from 'fs';
import * as path from 'path';

export interface Item {
  name: string;
  weight: number;
  value: number;
}

/**
 * Solves the 0/1 knapsack problem using dynamic programming.
 * Returns the list of items that maximizes total value without exceeding capacity.
 */
export function knapsack(items: Item[], capacity: number): Item[] {
  const n = items.length;
  const dp: number[][] = Array.from({ length: n + 1 }, () => Array(capacity + 1).fill(0));

  // Build DP table
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

  // Backtrack to find selected items
  const selected: Item[] = [];
  let w = capacity;
  for (let i = n; i > 0; i--) {
    if (dp[i][w] !== dp[i - 1][w]) {
      const item = items[i - 1];
      selected.push(item);
      w -= item.weight;
    }
  }
  return selected.reverse(); // Preserve original order
}

// CLI handling
if (require.main === module) {
  const args = process.argv.slice(2);
  const getArg = (flag: string): string | undefined => {
    const idx = args.indexOf(flag);
    return idx !== -1 && idx + 1 < args.length ? args[idx + 1] : undefined;
  };

  const itemsPath = getArg('--items');
  const capacityStr = getArg('--capacity');

  if (!itemsPath || !capacityStr) {
    console.error('Usage: node dist/main.js --items <path> --capacity <number>');
    process.exit(1);
  }

  const capacity = parseInt(capacityStr, 10);
  if (isNaN(capacity) || capacity < 0) {
    console.error('Capacity must be a nonânegative integer.');
    process.exit(1);
  }

  const raw = fs.readFileSync(path.resolve(itemsPath), 'utf-8');
  const items: Item[] = JSON.parse(raw);
  const result = knapsack(items, capacity);
  console.log(JSON.stringify(result, null, 2));
}
