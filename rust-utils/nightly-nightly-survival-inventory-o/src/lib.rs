use std::collections::HashMap;

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct Item {
    pub name: String,
    pub weight: usize,
    pub utility: usize,
}

/// Solve the 0/1 knapsack problem.
/// Returns the set of items that yields maximal utility without exceeding `capacity`.
pub fn optimal_items(items: &[Item], capacity: usize) -> Vec<Item> {
    let n = items.len();
    // dp[i][w] = max utility using first i items with weight limit w
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
    // Reconstruct chosen items
    let mut w = capacity;
    let mut chosen = Vec::new();
    for i in (0..n).rev() {
        if dp[i + 1][w] != dp[i][w] {
            let item = items[i].clone();
            chosen.push(item.clone());
            w -= item.weight;
        }
        if w == 0 { break; }
    }
    chosen.reverse();
    chosen
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_optimal_items_basic() {
        let items = vec![
            Item { name: "water".into(), weight: 3, utility: 10 },
            Item { name: "food".into(), weight: 5, utility: 8 },
            Item { name: "first-aid".into(), weight: 2, utility: 7 },
            Item { name: "radio".into(), weight: 1, utility: 4 },
            Item { name: "knife".into(), weight: 2, utility: 5 },
        ];
        let capacity = 10;
        let result = optimal_items(&items, capacity);
        let names: Vec<_> = result.iter().map(|i| i.name.as_str()).collect();
        // Expected optimal set: water, first-aid, radio, knife (total weight 8, utility 26)
        // food (weight 5, utility 8) would reduce total utility if taken.
        assert_eq!(names, vec!["water", "first-aid", "radio", "knife"]);
    }
}
