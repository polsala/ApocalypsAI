use clap::Parser;
use std::fs;
use std::path::PathBuf;

mod lib;
use lib::{Item, knapsack};

/// Simple CLI for the Scavenger Packer utility.
#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Path to CSV file containing items (name,weight,value)
    #[arg(short, long, value_name = "FILE")]
    items: PathBuf,

    /// Maximum carry weight
    #[arg(short, long, value_name = "CAPACITY")]
    capacity: u32,
}

fn parse_csv(content: &str) -> Vec<Item> {
    let mut items = Vec::new();
    for line in content.lines() {
        let parts: Vec<&str> = line.split(',').map(|s| s.trim()).collect();
        if parts.len() != 3 {
            continue; // Skip malformed lines
        }
        let name = parts[0].to_string();
        let weight = parts[1].parse::<u32>().unwrap_or(0);
        let value = parts[2].parse::<u32>().unwrap_or(0);
        items.push(Item { name, weight, value });
    }
    items
}

fn main() {
    let args = Args::parse();
    let csv_content = fs::read_to_string(&args.items)
        .expect("Failed to read items CSV file");
    let items = parse_csv(&csv_content);
    let selected = knapsack(&items, args.capacity);

    let total_weight: u32 = selected.iter().map(|i| i.weight).sum();
    let total_value: u32 = selected.iter().map(|i| i.value).sum();

    println!("Selected items:");
    for itm in &selected {
        println!("- {} (weight: {}, value: {})", itm.name, itm.weight, itm.value);
    }
    println!("Total weight: {}", total_weight);
    println!("Total value: {}", total_value);
}
