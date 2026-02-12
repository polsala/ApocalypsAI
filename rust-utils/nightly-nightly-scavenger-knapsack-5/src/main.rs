use std::env;
use std::fs;
use nightly_scavenger_knapsack::{Item, greedy_knapsack};

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
        eprintln!("Usage: {} <items.json> <max_weight>", args[0]);
        std::process::exit(1);
    }
    let items_path = &args[1];
    let max_weight: u32 = args[2].parse().expect("Invalid max_weight");
    let data = fs::read_to_string(items_path).expect("Failed to read items file");
    let items: Vec<Item> = serde_json::from_str(&data).expect("Invalid JSON format");
    let selected = greedy_knapsack(&items, max_weight);
    let names: Vec<String> = selected.iter().map(|i| i.name.clone()).collect();
    let total_value: u32 = selected.iter().map(|i| i.value).sum();
    println!("Selected items: {:?}", names);
    println!("Total value: {}", total_value);
}
