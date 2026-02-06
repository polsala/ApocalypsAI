use std::env;
use std::fs::File;
use std::io::{self, BufRead, BufReader};

#[derive(Debug, Clone)]
struct Item {
    name: String,
    weight: usize,
    value: usize,
}

fn parse_items<R: BufRead>(reader: R) -> Vec<Item> {
    let mut items = Vec::new();
    for line in reader.lines() {
        if let Ok(l) = line {
            let parts: Vec<&str> = l.split_whitespace().collect();
            if parts.len() != 3 {
                continue;
            }
            let name = parts[0].to_string();
            if let (Ok(w), Ok(v)) = (parts[1].parse::<usize>(), parts[2].parse::<usize>()) {
                items.push(Item { name, weight: w, value: v });
            }
        }
    }
    items
}

fn knapsack(items: &[Item], capacity: usize) -> (usize, Vec<String>) {
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
            selected.push(items[i].name.clone());
            w -= items[i].weight;
        }
    }
    selected.reverse();
    (dp[n][capacity], selected)
}

fn print_usage() {
    eprintln!("Usage: nightly-wasteland-knapsack <capacity> [input_file]");
    eprintln!("If input_file is omitted, reads from stdin.");
    eprintln!("Each line of input: <name> <weight> <value>");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        print_usage();
        std::process::exit(1);
    }
    let capacity = match args[1].parse::<usize>() {
        Ok(c) => c,
        Err(_) => {
            eprintln!("Invalid capacity: {}", args[1]);
            std::process::exit(1);
        }
    };
    let reader: Box<dyn BufRead> = if args.len() >= 3 {
        match File::open(&args[2]) {
            Ok(f) => Box::new(BufReader::new(f)),
            Err(e) => {
                eprintln!("Failed to open file {}: {}", args[2], e);
                std::process::exit(1);
            }
        }
    } else {
        Box::new(BufReader::new(io::stdin()))
    };
    let items = parse_items(reader);
    if items.is_empty() {
        eprintln!("No valid items provided.");
        std::process::exit(1);
    }
    let (total_value, selected) = knapsack(&items, capacity);
    println!("Optimal total value: {}", total_value);
    println!("Selected items:");
    for name in selected {
        println!("- {}", name);
    }
}
