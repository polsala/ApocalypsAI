/// Represents an item that can be taken by the scavenger.
#[derive(Debug, Clone)]
pub struct Item {
    pub name: String,
    pub weight: usize,
    pub value: usize,
}

/// Solves the 0/1 knapsack problem.
///
/// * `limit` – maximum total weight allowed.
/// * `items` – slice of `Item` structs.
///
/// Returns a vector of item names that constitute the optimal selection.
pub fn solve_knapsack(limit: usize, items: &[Item]) -> Vec<String> {
    let n = items.len();
    // dp[i][w] = max value using first i items with weight limit w
    let mut dp = vec![vec![0usize; limit + 1]; n + 1];

    for i in 0..n {
        let itm = &items[i];
        for w in 0..=limit {
            if itm.weight > w {
                dp[i + 1][w] = dp[i][w];
            } else {
                let without = dp[i][w];
                let with = dp[i][w - itm.weight] + itm.value;
                dp[i + 1][w] = if with > without { with } else { without };
            }
        }
    }

    // Backtrack to find which items were taken
    let mut w = limit;
    let mut selected = Vec::new();
    for i in (0..n).rev() {
        if dp[i + 1][w] != dp[i][w] {
            let itm = &items[i];
            selected.push(itm.name.clone());
            w -= itm.weight;
        }
        if w == 0 { break; }
    }
    selected.reverse();
    selected
}
