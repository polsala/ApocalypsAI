/**
 * Solve 0/1 knapsack problem.
 * @param {Array<{name:string, weight:number, value:number}>} items
 * @param {number} capacity
 * @returns {string[]} list of selected item names
 */
function packItems(items, capacity) {
  const n = items.length;
  // DP table (n+1) x (capacity+1)
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
      selected.push(item.name);
      w -= item.weight;
    }
  }
  return selected.reverse(); // preserve original order
}

module.exports = { packItems };
