use std::env;
use std::io::{self, BufRead};

mod lib;
use lib::{Item, solve_knapsack};

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        eprintln!("Usage: {} <weight_limit>", args[0]);
        std::process::exit(1);
    }
    let capacity: usize = args[1]
        .parse()
        .expect("Weight limit must be a positive integer");

    let stdin = io::stdin();
    let mut items = Vec::new();
    for line in stdin.lock().lines() {
        let line = line.expect("Failed to read line");
        if line.trim().is_empty() {
            continue;
        }
        // Expected format: name,weight,utility
        let parts: Vec<&str> = line.split(',').map(|s| s.trim()).collect();
        if parts.len() != 3 {
            eprintln!("Invalid line format: {}", line);
            std::process::exit(1);
        }
        let name = parts[0].to_string();
        let weight: usize = parts[1]
            .parse()
            .expect("Weight must be an integer");
        let utility: usize = parts[2]
            .parse()
            .expect("Utility must be an integer");
        items.push(Item { name, weight, utility });
    }

    let selected = solve_knapsack(&items, capacity);
    let total_utility: usize = selected
        .iter()
        .map(|name| {
            items
                .iter()
                .find(|it| &it.name == name)
                .unwrap()
                .utility
        })
        .sum();
    println!("Selected items: {}", selected.join(", "));
    println!("Total utility: {}", total_utility);
}

