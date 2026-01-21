use serde::{Deserialize, Serialize};

#[derive(Debug, Deserialize)]
pub struct Item {
    pub name: String,
    pub weight: usize,
    pub value: usize,
}

#[derive(Debug, Deserialize)]
pub struct Payload {
    pub capacity: usize,
    pub items: Vec<Item>,
}

/// Returns the list of item names that maximize total value without exceeding capacity.
pub fn compute_knapsack(payload: &Payload) -> Vec<String> {
    let n = payload.items.len();
    let cap = payload.capacity;
    // DP table: dp[i][w] = max value using first i items with weight <= w
    let mut dp = vec![vec![0usize; cap + 1]; n + 1];
    for i in 1..=n {
        let item = &payload.items[i - 1];
        for w in 0..=cap {
            if item.weight > w {
                dp[i][w] = dp[i - 1][w];
            } else {
                let without = dp[i - 1][w];
                let with = dp[i - 1][w - item.weight] + item.value;
                dp[i][w] = if with > without { with } else { without };
            }
        }
    }
    // Reconstruct selected items
    let mut w = cap;
    let mut selected = Vec::new();
    for i in (1..=n).rev() {
        if dp[i][w] != dp[i - 1][w] {
            let item = &payload.items[i - 1];
            selected.push(item.name.clone());
            w -= item.weight;
        }
    }
    selected.reverse();
    selected
}
