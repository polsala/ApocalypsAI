/// Represents an item that can be taken by the scavenger.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Item {
    pub name: String,
    pub weight: usize,
    pub value: usize,
}

/// Parse a slice of strings like "name,weight,value" into a vector of `Item`.
/// Invalid entries are ignored.
pub fn parse_items(args: &[String]) -> Vec<Item> {
    let mut items = Vec::new();
    for arg in args {
        let parts: Vec<&str> = arg.split(',').collect();
        if parts.len() != 3 {
            eprintln!("Invalid item format: {}", arg);
            continue;
        }
        let name = parts[0].to_string();
        let weight = parts[1].parse::<usize>().unwrap_or(0);
        let value = parts[2].parse::<usize>().unwrap_or(0);
        items.push(Item { name, weight, value });
    }
    items
}

/// Solve the 0/1 knapsack problem.
/// Returns a tuple of the selected item names (in the order they appear) and the total value.
pub fn knapsack(items: &[Item], capacity: usize) -> (Vec<String>, usize) {
    let n = items.len();
    let mut dp = vec![vec![0usize; capacity + 1]; n + 1];
    for i in 0..n {
        let item = &items[i];
        for w in 0..=capacity {
            if item.weight > w {
                dp[i + 1][w] = dp[i][w];
            } else {
                let without = dp[i][w];
                let with = dp[i][w - item.weight] + item.value;
                dp[i + 1][w] = if with > without { with } else { without };
            }
        }
    }
    // Backtrack to find which items were taken.
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
    (selected, dp[n][capacity])
}
