use std::env;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

#[derive(Debug, Clone)]
struct Item {
    name: String,
    weight: usize,
    value: usize,
}

// Parse CSV lines into Item structs
fn read_items<P: AsRef<Path>>(filename: P) -> io::Result<Vec<Item>> {
    let file = File::open(filename)?;
    let reader = io::BufReader::new(file);
    let mut items = Vec::new();
    for line in reader.lines() {
        let line = line?;
        if line.trim().is_empty() { continue; }
        let parts: Vec<&str> = line.split(',').map(|s| s.trim()).collect();
        if parts.len() != 3 { continue; }
        let name = parts[0].to_string();
        let weight = parts[1].parse::<usize>().unwrap_or(0);
        let value = parts[2].parse::<usize>().unwrap_or(0);
        items.push(Item { name, weight, value });
    }
    Ok(items)
}

// 0/1 knapsack dynamic programming solution
fn knapsack(items: &[Item], capacity: usize) -> (usize, Vec<Item>) {
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
    // Reconstruct selected items
    let mut w = capacity;
    let mut selected = Vec::new();
    for i in (0..n).rev() {
        if dp[i + 1][w] != dp[i][w] {
            let item = &items[i];
            selected.push(item.clone());
            w -= item.weight;
        }
    }
    selected.reverse();
    (dp[n][capacity], selected)
}

fn print_result(total_value: usize, selected: &[Item]) {
    println!("Total value: {}", total_value);
    println!("Selected items:");
    for item in selected {
        println!("- {} (weight: {}, value: {})", item.name, item.weight, item.value);
    }
}

fn print_usage() {
    eprintln!("Usage: <program> --capacity <max_weight> <items_csv>");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 4 || args[1] != "--capacity" {
        print_usage();
        std::process::exit(1);
    }
    let capacity = args[2].parse::<usize>().expect("Invalid capacity");
    let items_file = &args[3];
    let items = read_items(items_file).expect("Failed to read items file");
    let (total, selected) = knapsack(&items, capacity);
    print_result(total, &selected);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_knapsack_simple() {
        let items = vec![
            Item { name: "A".into(), weight: 3, value: 4 },
            Item { name: "B".into(), weight: 4, value: 5 },
            Item { name: "C".into(), weight: 2, value: 3 },
        ];
        let (value, selected) = knapsack(&items, 6);
        assert_eq!(value, 7);
        let names: Vec<_> = selected.iter().map(|i| i.name.as_str()).collect();
        assert_eq!(names, vec!["C", "A"]);
    }
}
