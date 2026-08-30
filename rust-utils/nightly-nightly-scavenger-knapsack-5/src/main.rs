use std::env;
use std::fs::File;
use std::io::{self, BufRead, BufReader};

#[derive(Debug, Clone)]
struct Item {
    name: String,
    weight: usize,
    value: usize,
}

fn parse_csv(path: &str) -> io::Result<Vec<Item>> {
    let file = File::open(path)?;
    let reader = BufReader::new(file);
    let mut items = Vec::new();
    for (idx, line) in reader.lines().enumerate() {
        let line = line?;
        if line.trim().is_empty() {
            continue;
        }
        let parts: Vec<&str> = line.split(',').map(|s| s.trim()).collect();
        if parts.len() != 3 {
            return Err(io::Error::new(
                io::ErrorKind::InvalidData,
                format!("Invalid CSV format on line {}", idx + 1),
            ));
        }
        let name = parts[0].to_string();
        let weight = parts[1]
            .parse::<usize>()
            .map_err(|_| io::Error::new(io::ErrorKind::InvalidData, "Weight must be a positive integer"))?;
        let value = parts[2]
            .parse::<usize>()
            .map_err(|_| io::Error::new(io::ErrorKind::InvalidData, "Value must be a positive integer"))?;
        items.push(Item { name, weight, value });
    }
    Ok(items)
}

/// Returns the list of item names that maximize total value without exceeding `capacity`.
fn knapsack(items: &[Item], capacity: usize) -> Vec<String> {
    let n = items.len();
    // DP table: dp[i][w] = max value using first i items with weight limit w
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
            selected.push(items[i].name.clone());
            w -= items[i].weight;
        }
        if w == 0 {
            break;
        }
    }
    selected.reverse();
    selected
}

fn main() -> io::Result<()> {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
        eprintln!("Usage: {} <capacity> <items.csv>", args[0]);
        std::process::exit(1);
    }
    let capacity: usize = args[1].parse().map_err(|_| {
        io::Error::new(io::ErrorKind::InvalidInput, "Capacity must be a positive integer")
    })?;
    let items = parse_csv(&args[2])?;
    let selected = knapsack(&items, capacity);
    let total_weight: usize = selected
        .iter()
        .map(|name| items.iter().find(|it| &it.name == name).unwrap().weight)
        .sum();
    let total_value: usize = selected
        .iter()
        .map(|name| items.iter().find(|it| &it.name == name).unwrap().value)
        .sum();
    println!("Selected items (total weight: {}, total value: {}):", total_weight, total_value);
    for name in selected {
        println!("- {}", name);
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    fn sample_items() -> Vec<Item> {
        vec![
            Item { name: "Water Bottle".into(), weight: 2, value: 3 },
            Item { name: "Canned Food".into(), weight: 3, value: 4 },
            Item { name: "First Aid Kit".into(), weight: 5, value: 10 },
            Item { name: "Radio".into(), weight: 1, value: 2 },
        ]
    }

    #[test]
    fn test_knapsack_basic() {
        let items = sample_items();
        let selected = knapsack(&items, 7);
        // Expected optimal selection: Canned Food (3,4) + First Aid Kit (5,10) exceeds weight.
        // Best within 7 weight is First Aid Kit (5,10) + Radio (1,2) = weight 6, value 12.
        // However, Canned Food + First Aid Kit = weight 8 (too heavy).
        // Canned Food + Radio + Water Bottle = weight 6, value 9.
        // So optimal is First Aid Kit + Radio.
        let mut expected = vec!["First Aid Kit", "Radio"];
        expected.sort();
        let mut got = selected.clone();
        got.sort();
        assert_eq!(got, expected);
    }

    #[test]
    fn test_knapsack_zero_capacity() {
        let items = sample_items();
        let selected = knapsack(&items, 0);
        assert!(selected.is_empty());
    }
}
