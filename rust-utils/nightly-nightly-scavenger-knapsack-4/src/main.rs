use std::io::{self, BufRead};

mod lib;
use lib::{Item, knapsack};

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() != 2 {
        eprintln!("Usage: {} <max-weight>", args[0]);
        std::process::exit(1);
    }
    let capacity: u32 = args[1].parse().expect("Invalid weight");

    let stdin = io::stdin();
    let mut items = Vec::new();
    for line in stdin.lock().lines() {
        let line = line.unwrap();
        if line.trim().is_empty() {
            continue;
        }
        let parts: Vec<&str> = line.split_whitespace().collect();
        if parts.len() != 3 {
            eprintln!("Invalid line: {}", line);
            std::process::exit(1);
        }
        let name = parts[0].to_string();
        let weight: u32 = parts[1].parse().expect("Invalid weight");
        let utility: u32 = parts[2].parse().expect("Invalid utility");
        items.push(Item { name, weight, utility });
    }

    let selected = knapsack(&items, capacity);
    for idx in selected {
        println!("{}", items[idx].name);
    }
}
