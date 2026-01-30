pub struct Item {
    pub name: String,
    pub weight: u32,
    pub utility: u32,
}

/// Returns the indices of the items that give the maximum total utility
/// without exceeding `capacity`. Implements the classic 0/1 knapsack DP.
pub fn knapsack(items: &[Item], capacity: u32) -> Vec<usize> {
    let n = items.len();
    let cap = capacity as usize;
    let mut dp = vec![vec![0u32; cap + 1]; n + 1];

    for i in 0..n {
        for w in 0..=cap {
            if items[i].weight as usize > w {
                dp[i + 1][w] = dp[i][w];
            } else {
                let without = dp[i][w];
                let with = dp[i][w - items[i].weight as usize] + items[i].utility;
                dp[i + 1][w] = without.max(with);
            }
        }
    }

    // Backtrack to find selected items
    let mut selected = Vec::new();
    let mut w = cap;
    for i in (0..n).rev() {
        if dp[i + 1][w] != dp[i][w] {
            selected.push(i);
            w -= items[i].weight as usize;
        }
    }
    selected.reverse();
    selected
}
