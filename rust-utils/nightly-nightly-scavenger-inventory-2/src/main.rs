use clap::{Parser, Subcommand};
use chrono::NaiveDate;
use serde::{Deserialize, Serialize};
use std::fs;
use std::process;

#[derive(Serialize, Deserialize, Debug, Clone, PartialEq, Eq)]
pub struct Item {
    pub name: String,
    pub quantity: u32,
    pub expires: NaiveDate,
}

#[derive(Parser)]
#[command(name = "nightly-scavenger-inventory")]
#[command(about = "Manage scavenger inventory", long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// List items sorted by expiration, warn about expired
    List {
        /// Path to inventory JSON file
        file: String,
    },
    /// Add a new item to inventory
    Add {
        /// Path to inventory JSON file
        file: String,
        /// Item name
        name: String,
        /// Quantity
        quantity: u32,
        /// Expiration date (YYYY-MM-DD)
        expires: String,
    },
}

fn load_items(path: &str) -> Vec<Item> {
    let data = fs::read_to_string(path).unwrap_or_else(|e| {
        eprintln!("Failed to read file {}: {}", path, e);
        process::exit(1);
    });
    serde_json::from_str(&data).unwrap_or_else(|e| {
        eprintln!("Failed to parse JSON: {}", e);
        process::exit(1);
    })
}

fn save_items(path: &str, items: &[Item]) {
    let json = serde_json::to_string_pretty(items).expect("Serialization failed");
    fs::write(path, json).unwrap_or_else(|e| {
        eprintln!("Failed to write file {}: {}", path, e);
        process::exit(1);
    });
}

pub fn prioritize(items: &[Item]) -> Vec<Item> {
    let mut sorted = items.to_vec();
    sorted.sort_by_key(|i| i.expires);
    sorted
}

fn list_items(path: &str) {
    let items = load_items(path);
    let sorted = prioritize(&items);
    let today = chrono::Local::today().naive_local();
    for item in sorted {
        let status = if item.expires < today { "EXPIRED" } else { "OK" };
        println!(
            "{} (x{}) - expires {} [{}]",
            item.name, item.quantity, item.expires, status
        );
    }
}

fn add_item(path: &str, name: String, quantity: u32, expires_str: String) {
    let mut items = load_items(path);
    let expires = NaiveDate::parse_from_str(&expires_str, "%Y-%m-%d").unwrap_or_else(|e| {
        eprintln!("Invalid date format: {}", e);
        process::exit(1);
    });
    items.push(Item { name, quantity, expires });
    save_items(path, &items);
    println!("Item added.");
}

fn main() {
    let cli = Cli::parse();

    match cli.command {
        Commands::List { file } => list_items(&file),
        Commands::Add { file, name, quantity, expires } => {
            add_item(&file, name, quantity, expires);
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use chrono::NaiveDate;

    #[test]
    fn test_prioritize() {
        let items = vec![
            Item {
                name: "Water".to_string(),
                quantity: 5,
                expires: NaiveDate::from_ymd_opt(2024, 5, 1).unwrap(),
            },
            Item {
                name: "Energy Bar".to_string(),
                quantity: 10,
                expires: NaiveDate::from_ymd_opt(2023, 11, 15).unwrap(),
            },
        ];
        let sorted = prioritize(&items);
        assert_eq!(sorted[0].name, "Energy Bar");
        assert_eq!(sorted[1].name, "Water");
    }

    #[test]
    fn test_add_item_logic() {
        // Simulate adding an item to an empty inventory vector
        let mut items: Vec<Item> = Vec::new();
        let new_item = Item {
            name: "Canned Beans".to_string(),
            quantity: 12,
            expires: NaiveDate::from_ymd_opt(2025, 12, 31).unwrap(),
        };
        items.push(new_item.clone());
        assert_eq!(items.len(), 1);
        assert_eq!(items[0], new_item);
    }
}
