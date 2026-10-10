use clap::{Parser, Subcommand};
use std::fs;
use std::path::Path;

mod lib;
use lib::{add_item, deserialize_inventory, serialize_inventory, Item, prioritize};

#[derive(Parser)]
#[command(name = "scavenger_inventory")]
#[command(about = "Track scavenged supplies", long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Add a new item to the inventory
    Add {
        name: String,
        category: String,
        quantity: u32,
        expires_in_days: u32,
    },
    /// List all items in the inventory
    List,
    /// Show the most urgent item (expires soonest)
    Prioritize,
}

const INVENTORY_FILE: &str = "inventory.json";

fn load_inventory() -> Vec<Item> {
    if Path::new(INVENTORY_FILE).exists() {
        let data = fs::read_to_string(INVENTORY_FILE).expect("Failed to read inventory file");
        deserialize_inventory(&data)
    } else {
        Vec::new()
    }
}

fn save_inventory(inventory: &[Item]) {
    let json = serialize_inventory(inventory);
    fs::write(INVENTORY_FILE, json).expect("Failed to write inventory file");
}

fn main() {
    let cli = Cli::parse();
    match cli.command {
        Commands::Add { name, category, quantity, expires_in_days } => {
            let mut inv = load_inventory();
            let item = Item { name, category, quantity, expires_in_days };
            inv = add_item(inv, item);
            save_inventory(&inv);
            println!("Item added.");
        }
        Commands::List => {
            let inv = load_inventory();
            if inv.is_empty() {
                println!("Inventory is empty.");
            } else {
                for (i, item) in inv.iter().enumerate() {
                    println!("{}: {} ({}), qty: {}, expires in {} days", i+1, item.name, item.category, item.quantity, item.expires_in_days);
                }
            }
        }
        Commands::Prioritize => {
            let inv = load_inventory();
            match prioritize(&inv) {
                Some(item) => println!("Most urgent: {} ({}), qty: {}, expires in {} days", item.name, item.category, item.quantity, item.expires_in_days),
                None => println!("Inventory is empty.")
            }
        }
    }
}
