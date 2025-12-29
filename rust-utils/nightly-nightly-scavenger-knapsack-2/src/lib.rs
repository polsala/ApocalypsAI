pub struct Item {
    pub name: String,
    pub weight: u32,
    pub value: u32,
}

/// Solve the 0/1 knapsack problem.
///
/// * `items` – slice of available items
/// * `capacity` – maximum total weight allowed
///
/// Returns a vector of items that yields the maximum total value without exceeding `capacity`.
pub fn solve_knapsack(items: &[Item], capacity: u32) -> Vec<Item> {
    let n = items.len();
    let cap = capacity as usize;
    // dp[i][w] = max value using first i items with weight limit w
    let mut dp = vec![vec![0u32; cap + 1]; n + 1];

    for i in 1..=n {
        let item = &items[i - 1];
        for w in 0..=cap {
            if (item.weight as usize) <= w {
                let without = dp[i - 1][w];
                let with = dp[i - 1][w - item.weight as usize] + item.value;
                dp[i][w] = if with > without { with } else { without };
            } else {
                dp[i][w] = dp[i - 1][w];
            }
        }
    }

    // Reconstruct selected items
    let mut w = cap;
    let mut selected = Vec::new();
    for i in (1..=n).rev() {
        if dp[i][w] != dp[i - 1][w] {
            let item = &items[i - 1];
            selected.push(Item {
                name: item.name.clone(),
                weight: item.weight,
                value: item.value,
            });
            w -= item.weight as usize;
        }
    }
    selected.reverse();
    selected
}
