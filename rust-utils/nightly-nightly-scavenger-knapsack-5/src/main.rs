use std::env;
use std::fs;
use serde_json;
mod lib;
use lib::{Item, solve_knapsack};

fn print_usage() {
    eprintln!("Usage: <program> <items.json> <max_weight>");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
        print_usage();
        std::process::exit(1);
    }
    let items_path = &args[1];
    let max_weight: usize = args[2].parse().expect("Invalid max_weight");
    let data = fs::read_to_string(items_path).expect("Failed to read items file");
    let items: Vec<Item> = serde_json::from_str(&data).expect("Invalid JSON format");
    let selected = solve_knapsack(&items, max_weight);
    let names: Vec<String> = selected.iter().map(|i| i.name.clone()).collect();
    println!("{}", serde_json::to_string_pretty(&names).unwrap());
}
