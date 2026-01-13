import * as fs from 'fs';
import * as path from 'path';

/**
 * Represents a single supply item.
 */
export interface Item {
  name: string;
  weight: number;
  value: number;
}

/**
 * Result of the knapsack solver.
 */
export interface KnapsackResult {
  selected: Item[];
  totalWeight: number;
  totalValue: number;
}

/**
 * Solves the 0/1 knapsack problem using dynamic programming.
 *
 * @param items   Array of candidate items.
 * @param capacity Maximum total weight allowed.
 * @returns       The optimal selection of items.
 */
export function solveKnapsack(items: Item[], capacity: number): KnapsackResult {
  const n = items.length;
  // dp[i][w] = max value using first i items with weight limit w
  const dp: number[][] = Array.from({ length: n + 1 }, () => Array(capacity + 1).fill(0));

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

  selected.reverse(); // preserve original order
  const totalWeight = selected.reduce((sum, it) => sum + it.weight, 0);
  const totalValue = selected.reduce((sum, it) => sum + it.value, 0);

  return { selected, totalWeight, totalValue };
}

/**
 * Reads JSON input either from a file (if -i/--input is provided) or from STDIN.
 */
function readInput(): { capacity: number; items: Item[] } {
  const args = process.argv.slice(2);
  const inputFlagIndex = args.findIndex(arg => arg === '-i' || arg === '--input');
  let raw: string;
  if (inputFlagIndex !== -1 && args[inputFlagIndex + 1]) {
    const filePath = path.resolve(process.cwd(), args[inputFlagIndex + 1]);
    raw = fs.readFileSync(filePath, 'utf-8');
  } else {
    // Read from STDIN
    raw = fs.readFileSync(0, 'utf-8'); // 0 = STDIN
  }
  const parsed = JSON.parse(raw);
  if (typeof parsed.capacity !== 'number' || !Array.isArray(parsed.items)) {
    throw new Error('Invalid input format. Expected { capacity: number, items: [...] }');
  }
  return { capacity: parsed.capacity, items: parsed.items };
}

/**
 * Pretty‑prints the result to the console.
 */
function printResult(result: KnapsackResult): void {
  console.log('Selected items:');
  for (const it of result.selected) {
    console.log(`- ${it.name} (weight: ${it.weight}, value: ${it.value})`);
  }
  console.log('');
  console.log(`Total weight: ${result.totalWeight}`);
  console.log(`Total value: ${result.totalValue}`);
}

// Main execution block
if (require.main === module) {
  try {
    const { capacity, items } = readInput();
    const result = solveKnapsack(items, capacity);
    printResult(result);
  } catch (err) {
    console.error('Error:', (err as Error).message);
    process.exit(1);
  }
}

