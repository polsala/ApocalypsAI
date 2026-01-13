/// Represents a piece of gear.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Item {
    pub name: String,
    pub weight: usize,
    pub utility: usize,
}

/// Solve the 0/1 knapsack problem.
/// Returns the names of the selected items in the order they appear in the input.
pub fn solve_knapsack(items: &[Item], capacity: usize) -> Vec<String> {
    let n = items.len();
    let mut dp = vec![vec![0usize; capacity + 1]; n + 1];
    for i in 0..n {
        let item = &items[i];
        for w in 0..=capacity {
            if item.weight > w {
                dp[i + 1][w] = dp[i][w];
            } else {
                let without = dp[i][w];
                let with = dp[i][w - item.weight] + item.utility;
                dp[i + 1][w] = if with > without { with } else { without };
            }
        }
    }
    // Backtrack to find selected items
    let mut w = capacity;
    let mut selected = Vec::new();
    for i in (0..n).rev() {
        if dp[i + 1][w] != dp[i][w] {
            let item = &items[i];
            selected.push(item.name.clone());
            w -= item.weight;
        }
    }
    selected.reverse();
    selected
}

