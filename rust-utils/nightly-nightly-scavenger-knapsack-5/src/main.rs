use clap::Parser;
use std::fs;
use std::process;

mod lib;
use lib::{Item, knapsack};

#[derive(Parser, Debug)]
#[command(author, version, about = "Post‑apocalypse scavenger knapsack optimizer", long_about = None)]
struct Args {
    /// Path to JSON file containing an array of items
    input: String,
    /// Maximum total weight you can carry
    capacity: usize,
}

fn main() {
    let args = Args::parse();
    let data = match fs::read_to_string(&args.input) {
        Ok(d) => d,
        Err(e) => {
            eprintln!("Failed to read {}: {}", args.input, e);
            process::exit(1);
        }
    };
    let items: Vec<Item> = match serde_json::from_str(&data) {
        Ok(i) => i,
        Err(e) => {
            eprintln!("Failed to parse JSON: {}", e);
            process::exit(1);
        }
    };
    let selected = knapsack(&items, args.capacity);
    let total_weight: usize = selected.iter().map(|i| i.weight).sum();
    let total_value: usize = selected.iter().map(|i| i.value).sum();
    println!("Selected items:");
    for item in &selected {
        println!("- {} (weight: {}, value: {})", item.name, item.weight, item.value);
    }
    println!("Total weight: {}", total_weight);
    println!("Total value: {}", total_value);
}
