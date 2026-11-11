/// Represents a scavenged item.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Item {
    pub name: String,
    pub weight: usize,
    pub value: usize,
}

/// Solves the 0/1 knapsack problem.
///
/// Returns a vector of items that maximizes total value without exceeding `capacity`.
pub fn solve_knapsack(items: &[Item], capacity: usize) -> Vec<Item> {
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
    // Backtrack to find selected items
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
    fn test_simple_knapsack() {
        let items = vec![
            Item { name: "water".into(), weight: 3, value: 10 },
            Item { name: "food".into(), weight: 2, value: 7 },
            Item { name: "medkit".into(), weight: 5, value: 12 },
        ];
        let capacity = 5;
        let result = solve_knapsack(&items, capacity);
        let names: Vec<&str> = result.iter().map(|i| i.name.as_str()).collect();
        assert!(names.contains(&"water"));
        assert!(names.contains(&"food"));
        assert_eq!(result.iter().map(|i| i.value).sum::<usize>(), 17);
    }

    #[test]
    fn test_no_fit() {
        let items = vec![
            Item { name: "rock".into(), weight: 10, value: 1 },
        ];
        let capacity = 5;
        let result = solve_knapsack(&items, capacity);
        assert!(result.is_empty());
    }
}
