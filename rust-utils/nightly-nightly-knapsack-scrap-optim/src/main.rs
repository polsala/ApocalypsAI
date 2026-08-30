use std::env;
use std::fs;
use knapsack_scrap_optimizer::{Item, knapsack};

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
        eprintln!("Usage: {} <items.json> <max_weight>", args[0]);
        std::process::exit(1);
    }
    let items_path = &args[1];
    let max_weight: usize = args[2].parse().expect("Invalid max_weight");
    let data = fs::read_to_string(items_path).expect("Failed to read items file");
    let items: Vec<Item> = serde_json::from_str(&data).expect("Invalid JSON format");
    let (total_value, selected_indices) = knapsack(&items, max_weight);
    let selected_names: Vec<String> = selected_indices.iter().map(|&i| items[i].name.clone()).collect();
    println!("Selected items: {:?}", selected_names);
    println!("Total value: {}", total_value);
}
