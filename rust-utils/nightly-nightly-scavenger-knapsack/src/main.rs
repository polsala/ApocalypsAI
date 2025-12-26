use std::io::{self, BufRead};

#[derive(Debug, Clone)]
struct Item {
    name: String,
    weight: usize,
    value: usize,
}

fn parse_items() -> Vec<Item> {
    let stdin = io::stdin();
    let lines = stdin.lock().lines();
    let mut items = Vec::new();
    for line in lines {
        if let Ok(l) = line {
            if l.trim().is_empty() { continue; }
            let parts: Vec<&str> = l.split_whitespace().collect();
            if parts.len() != 3 { continue; }
            let name = parts[0].to_string();
            let weight = parts[1].parse::<usize>().unwrap_or(0);
            let value = parts[2].parse::<usize>().unwrap_or(0);
            items.push(Item { name, weight, value });
        }
    }
    items
}

// 0/1 knapsack DP returning total value and selected item names
fn knapsack(items: &[Item], capacity: usize) -> (usize, Vec<String>) {
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
    // backtrack to find selected items
    let mut w = capacity;
    let mut selected = Vec::new();
    for i in (0..n).rev() {
        if dp[i + 1][w] != dp[i][w] {
            selected.push(items[i].name.clone());
            w -= items[i].weight;
        }
    }
    selected.reverse();
    (dp[n][capacity], selected)
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() != 2 {
        eprintln!("Usage: {} <capacity>", args[0]);
        std::process::exit(1);
    }
    let capacity = args[1].parse::<usize>().unwrap_or(0);
    let items = parse_items();
    let (total_value, selected) = knapsack(&items, capacity);
    println!("Total value: {}", total_value);
    println!("Selected items:");
    for name in selected {
        println!("- {}", name);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_knapsack_basic() {
        let items = vec![
            Item { name: "water".into(), weight: 3, value: 10 },
            Item { name: "food".into(), weight: 2, value: 9 },
            Item { name: "medkit".into(), weight: 5, value: 15 },
            Item { name: "radio".into(), weight: 1, value: 4 },
        ];
        let (value, selected) = knapsack(&items, 10);
        assert_eq!(value, 34);
        assert_eq!(selected, vec!["water", "food", "radio"]);
    }

    #[test]
    fn test_knapsack_zero_capacity() {
        let items = vec![
            Item { name: "rock".into(), weight: 5, value: 1 },
        ];
        let (value, selected) = knapsack(&items, 0);
        assert_eq!(value, 0);
        assert!(selected.is_empty());
    }
}
