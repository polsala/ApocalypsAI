use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Deserialize, Serialize, PartialEq, Eq)]
pub struct Item {
    pub name: String,
    pub weight: usize,
    pub value: usize,
}

#[derive(Debug, Deserialize)]
pub struct Problem {
    pub capacity: usize,
    pub items: Vec<Item>,
}

/// Returns the list of item names that maximize total value without exceeding `capacity`.
/// Implements the classic dynamic‑programming solution for the 0/1 knapsack problem.
pub fn compute_knapsack(problem: &Problem) -> Vec<String> {
    let n = problem.items.len();
    let cap = problem.capacity;
    // dp[i][w] = max value using first i items with weight limit w
    let mut dp = vec![vec![0usize; cap + 1]; n + 1];
    for i in 0..n {
        let item = &problem.items[i];
        for w in 0..=cap {
            if item.weight > w {
                dp[i + 1][w] = dp[i][w];
            } else {
                let without = dp[i][w];
                let with = dp[i][w - item.weight] + item.value;
                dp[i + 1][w] = if with > without { with } else { without };
            }
        }
    }
    // Reconstruct selected items
    let mut selected = Vec::new();
    let mut w = cap;
    for i in (0..n).rev() {
        if dp[i + 1][w] != dp[i][w] {
            let item = &problem.items[i];
            selected.push(item.name.clone());
            w -= item.weight;
        }
        if w == 0 { break; }
    }
    selected.reverse();
    selected
}
