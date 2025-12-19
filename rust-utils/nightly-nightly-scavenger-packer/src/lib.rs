use std::cmp;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Item {
    pub name: String,
    pub weight: u32,
    pub value: u32,
}

/// Solve the 0/1 knapsack problem.
/// Returns a vector of selected `Item`s that maximizes total value without exceeding `capacity`.
pub fn knapsack(items: &[Item], capacity: u32) -> Vec<Item> {
    let n = items.len();
    // DP table: dp[i][w] = max value using first i items with weight limit w
    let mut dp = vec![vec![0u32; (capacity + 1) as usize]; n + 1];

    for i in 0..n {
        let itm = &items[i];
        for w in 0..=capacity {
            if itm.weight > w {
                dp[i + 1][w as usize] = dp[i][w as usize];
            } else {
                let without = dp[i][w as usize];
                let with = dp[i][(w - itm.weight) as usize] + itm.value;
                dp[i + 1][w as usize] = cmp::max(without, with);
            }
        }
    }

    // Reconstruct selected items
    let mut selected = Vec::new();
    let mut w = capacity;
    for i in (0..n).rev() {
        if dp[i + 1][w as usize] != dp[i][w as usize] {
            let itm = &items[i];
            selected.push(itm.clone());
            w -= itm.weight;
        }
        if w == 0 {
            break;
        }
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
        let result = knapsack(&items, 7);
        // Expected optimal set: A + B (value 9)
        assert_eq!(result.len(), 2);
        assert!(result.iter().any(|i| i.name == "A"));
        assert!(result.iter().any(|i| i.name == "B"));
    }
}
