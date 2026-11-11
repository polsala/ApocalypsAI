use std::env;
use std::process;

mod lib;
use lib::{Item, solve_knapsack};

fn parse_item(s: &str) -> Result<Item, String> {
    // Expected format: name:weight:value
    let parts: Vec<&str> = s.split(':').collect();
    if parts.len() != 3 {
        return Err(format!("Invalid item format '{}', expected name:weight:value", s));
    }
    let name = parts[0].to_string();
    let weight = parts[1]
        .parse::<usize>()
        .map_err(|_| format!("Invalid weight in item '{}'", s))?;
    let value = parts[2]
        .parse::<usize>()
        .map_err(|_| format!("Invalid value in item '{}'", s))?;
    Ok(Item { name, weight, value })
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
        eprintln!("Usage: {} <capacity> <item1,item2,...>", args[0]);
        eprintln!("Each item format: name:weight:value");
        process::exit(1);
    }
    let capacity: usize = match args[1].parse() {
        Ok(c) => c,
        Err(_) => {
            eprintln!("Capacity must be a positive integer");
            process::exit(1);
        }
    };
    let raw_items = &args[2];
    let mut items = Vec::new();
    for token in raw_items.split(',') {
        match parse_item(token) {
            Ok(item) => items.push(item),
            Err(e) => {
                eprintln!("Error parsing item: {}", e);
                process::exit(1);
            }
        }
    }
    let selected = solve_knapsack(&items, capacity);
    if selected.is_empty() {
        println!("No items can be selected within the given capacity.");
        return;
    }
    let total_value: usize = selected.iter().map(|i| i.value).sum();
    println!("Selected items:");
    for i in &selected {
        println!(" - {} (weight: {}, value: {})", i.name, i.weight, i.value);
    }
    println!("Total value: {}", total_value);
}
