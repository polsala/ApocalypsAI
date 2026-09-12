use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct Item {
    pub name: String,
    pub weight: usize,
    pub value: usize,
}

/// Solve the 0/1 knapsack problem.
/// Returns the list of items that maximizes total value without exceeding `max_weight`.
pub fn solve_knapsack(items: &[Item], max_weight: usize) -> Vec<Item> {
    let n = items.len();
    let mut dp = vec![vec![0usize; max_weight + 1]; n + 1];
    for i in 0..n {
        let item = &items[i];
        for w in 0..=max_weight {
            if item.weight > w {
                dp[i + 1][w] = dp[i][w];
            } else {
                let without = dp[i][w];
                let with = dp[i][w - item.weight] + item.value;
                dp[i + 1][w] = if with > without { with } else { without };
            }
        }
    }
    // Backtrack to find selected items
    let mut w = max_weight;
    let mut selected = Vec::new();
    for i in (0..n).rev() {
        if dp[i + 1][w] != dp[i][w] {
            let item = &items[i];
            selected.push(item.clone());
            w -= item.weight;
        }
    }
    selected.reverse();
    selected
}
