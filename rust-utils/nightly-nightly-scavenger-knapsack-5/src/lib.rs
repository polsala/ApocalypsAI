use serde::{Deserialize, Serialize};

#[derive(Debug, Deserialize)]
pub struct Item {
    pub name: String,
    pub weight: usize,
    pub value: usize,
}

#[derive(Debug, Deserialize)]
pub struct Input {
    pub capacity: usize,
    pub items: Vec<Item>,
}

/// Returns a vector of item names that constitute the optimal (maximum value) selection
/// without exceeding the given capacity.
pub fn solve_knapsack(input: &Input) -> Vec<String> {
    let n = input.items.len();
    let cap = input.capacity;
    // DP table: dp[i][w] = max value using first i items with weight limit w
    let mut dp = vec![vec![0usize; cap + 1]; n + 1];
    for i in 0..n {
        let item = &input.items[i];
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
            let item = &input.items[i];
            selected.push(item.name.clone());
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
    use assert_json_diff::assert_json_eq;
    use serde_json::json;

    #[test]
    fn test_basic_scenario() {
        let input = Input {
            capacity: 10,
            items: vec![
                Item { name: "canned beans".into(), weight: 3, value: 5 },
                Item { name: "bottled water".into(), weight: 2, value: 4 },
                Item { name: "first‑aid kit".into(), weight: 5, value: 7 },
                Item { name: "flashlight".into(), weight: 1, value: 2 },
            ],
        };
        let result = solve_knapsack(&input);
        // Expected optimal set: beans, water, flashlight (total weight 6, value 11)
        let expected = vec!["canned beans", "bottled water", "flashlight"];
        assert_eq!(result, expected);
        // Also verify JSON serialization matches expectation
        let json_res = serde_json::to_value(&result).unwrap();
        let json_exp = json!(expected);
        assert_json_eq!(json_res, json_exp);
    }

    #[test]
    fn test_no_items_fit() {
        let input = Input {
            capacity: 1,
            items: vec![
                Item { name: "heavy armor".into(), weight: 5, value: 10 },
            ],
        };
        let result = solve_knapsack(&input);
        let expected: Vec<String> = vec![];
        assert_eq!(result, expected);
    }
}
