use serde::Deserialize;

#[derive(Debug, Clone, Deserialize, PartialEq, Eq)]
pub struct Item {
    pub name: String,
    pub weight: usize,
    pub value: usize,
}

/// Solve the 0/1 knapsack problem.
/// Returns a vector of selected items that maximizes total value without exceeding `capacity`.
pub fn knapsack(items: &[Item], capacity: usize) -> Vec<Item> {
    let n = items.len();
    // dp[i][w] = max value using first i items with weight limit w
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
    // Reconstruct selected items
    let mut selected = Vec::new();
    let mut w = capacity;
    for i in (0..n).rev() {
        if dp[i + 1][w] != dp[i][w] {
            let item = &items[i];
            selected.push(item.clone());
            w -= item.weight;
        }
        if w == 0 { break; }
    }
    selected.reverse();
    selected
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_knapsack_basic() {
        let items = vec![
            Item { name: "A".into(), weight: 3, value: 4 },
            Item { name: "B".into(), weight: 4, value: 5 },
            Item { name: "C".into(), weight: 2, value: 3 },
        ];
        let result = knapsack(&items, 6);
        // Optimal is items A (3,4) + C (2,3) = weight 5, value 7
        assert_eq!(result.len(), 2);
        assert!(result.iter().any(|i| i.name == "A"));
        assert!(result.iter().any(|i| i.name == "C"));
        let total_weight: usize = result.iter().map(|i| i.weight).sum();
        let total_value: usize = result.iter().map(|i| i.value).sum();
        assert_eq!(total_weight, 5);
        assert_eq!(total_value, 7);
    }
}
