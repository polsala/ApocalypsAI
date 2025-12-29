use std::env;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

mod lib;
use lib::{Item, solve_knapsack};

fn read_items<P>(filename: P) -> io::Result<Vec<Item>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    let reader = io::BufReader::new(file);
    let mut items = Vec::new();
    for line_res in reader.lines() {
        let line = line_res?;
        if line.trim().is_empty() {
            continue;
        }
        // Expected format: name weight value (space‑separated)
        let parts: Vec<&str> = line.split_whitespace().collect();
        if parts.len() != 3 {
            eprintln!("Skipping malformed line: {}", line);
            continue;
        }
        let name = parts[0].to_string();
        let weight = parts[1].parse::<u32>().unwrap_or(0);
        let value = parts[2].parse::<u32>().unwrap_or(0);
        items.push(Item { name, weight, value });
    }
    Ok(items)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
        eprintln!("Usage: {} <capacity> <items_file>", args[0]);
        std::process::exit(1);
    }
    let capacity = args[1].parse::<u32>().expect("Invalid capacity");
    let items = read_items(&args[2]).expect("Failed to read items file");
    let selected = solve_knapsack(&items, capacity);
    let total_weight: u32 = selected.iter().map(|i| i.weight).sum();
    let total_value: u32 = selected.iter().map(|i| i.value).sum();
    println!("Selected items (total weight {}, total value {}):", total_weight, total_value);
    for item in selected {
        println!("- {} (w:{}, v:{})", item.name, item.weight, item.value);
    }
}
