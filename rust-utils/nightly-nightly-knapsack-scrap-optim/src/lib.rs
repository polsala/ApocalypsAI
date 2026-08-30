use serde::Deserialize;

#[derive(Debug, Deserialize, Clone)]
pub struct Item {
    pub name: String,
    pub weight: usize,
    pub value: usize,
}

/// Returns the maximum total value achievable and the indices of the selected items.
pub fn knapsack(items: &[Item], max_weight: usize) -> (usize, Vec<usize>) {
    let n = items.len();
    let mut dp = vec![vec![0usize; max_weight + 1]; n + 1];
    for i in 0..n {
        let w = items[i].weight;
        let v = items[i].value;
        for cap in 0..=max_weight {
            if w > cap {
                dp[i + 1][cap] = dp[i][cap];
            } else {
                let without = dp[i][cap];
                let with = dp[i][cap - w] + v;
                dp[i + 1][cap] = if with > without { with } else { without };
            }
        }
    }
    // Backtrack to find selected item indices
    let mut selected = Vec::new();
    let mut cap = max_weight;
    for i in (0..n).rev() {
        if dp[i + 1][cap] != dp[i][cap] {
            selected.push(i);
            cap -= items[i].weight;
        }
    }
    selected.reverse();
    (dp[n][max_weight], selected)
}
