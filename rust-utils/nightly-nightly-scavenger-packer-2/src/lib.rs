/// Represents an item that can be scavenged.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Item {
    pub name: String,
    pub weight: usize,
    pub value: usize,
}

/// Parse a string of the form "name:weight:value" into an `Item`.
/// Returns `None` if the format is invalid or parsing fails.
pub fn parse_item(s: &str) -> Option<Item> {
    let parts: Vec<&str> = s.split(':').collect();
    if parts.len() != 3 {
        return None;
    }
    let name = parts[0].to_string();
    let weight = parts[1].parse::<usize>().ok()?;
    let value = parts[2].parse::<usize>().ok()?;
    Some(Item { name, weight, value })
}

/// 0/1 knapsack dynamic‑programming implementation.
/// Returns a tuple `(max_value, selected_indices)` where `selected_indices`
/// are the positions of the chosen items in the original slice.
pub fn knapsack(items: &[Item], capacity: usize) -> (usize, Vec<usize>) {
    let n = items.len();
    let mut dp = vec![vec![0usize; capacity + 1]; n + 1];
    for i in 0..n {
        for w in 0..=capacity {
            if items[i].weight > w {
                dp[i + 1][w] = dp[i][w];
            } else {
                let without = dp[i][w];
                let with = dp[i][w - items[i].weight] + items[i].value;
                dp[i + 1][w] = if with > without { with } else { without };
            }
        }
    }
    // Backtrack to find selected items.
    let mut w = capacity;
    let mut selected = Vec::new();
    for i in (0..n).rev() {
        if dp[i + 1][w] != dp[i][w] {
            selected.push(i);
            w -= items[i].weight;
        }
    }
    selected.reverse();
    (dp[n][capacity], selected)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_knapsack_basic() {
        let items = vec![
            Item { name: "a".into(), weight: 3, value: 4 },
            Item { name: "b".into(), weight: 4, value: 5 },
            Item { name: "c".into(), weight: 2, value: 3 },
        ];
        let (max, selected) = knapsack(&items, 6);
        assert_eq!(max, 7);
        // Expected selection: items 0 and 2 (a + c)
        assert_eq!(selected, vec![0, 2]);
    }
}
