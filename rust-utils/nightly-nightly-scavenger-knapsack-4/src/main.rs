use std::io::{self, BufRead};

use nightly_scavenger_knapsack::{Item, knapsack};

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() != 2 {
        eprintln!("Usage: {} <capacity>", args[0]);
        std::process::exit(1);
    }
    let capacity: usize = args[1].parse().expect("Capacity must be a positive integer");
    let stdin = io::stdin();
    let mut items = Vec::new();
    for line in stdin.lock().lines() {
        let line = line.expect("Failed to read line");
        if line.trim().is_empty() {
            continue;
        }
        let parts: Vec<&str> = line.split_whitespace().collect();
        if parts.len() != 3 {
            eprintln!("Invalid line format: {}", line);
            std::process::exit(1);
        }
        let name = parts[0].to_string();
        let weight: usize = parts[1].parse().expect("Weight must be integer");
        let value: usize = parts[2].parse().expect("Value must be integer");
        items.push(Item { name, weight, value });
    }
    let result = knapsack(&items, capacity);
    for name in result {
        println!("{}", name);
    }
}
