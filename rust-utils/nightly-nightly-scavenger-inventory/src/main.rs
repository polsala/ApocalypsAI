use clap::{Parser, Subcommand};
use std::path::PathBuf;

mod lib;
use lib::{add_item, load_inventory, save_inventory, suggest_next, sorted_by_expiration, Item};

/// Default inventory file name in the current directory.
const DEFAULT_INVENTORY: &str = "inventory.json";

#[derive(Parser)]
#[command(name = "nightly-scavenger-inventory")]
#[command(author = "ApocalypsAI")]
#[command(version = "0.1.0")]
#[command(about = "Track scavenged supplies and suggest what to consume next", long_about = None)]
struct Cli {
    /// Optional path to inventory file
    #[arg(short, long, value_name = "FILE", default_value = DEFAULT_INVENTORY)]
    inventory: PathBuf,

    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Add a new item to the inventory
    Add {
        #[arg(short, long)]
        name: String,
        #[arg(short, long)]
        quantity: u32,
        #[arg(short, long, help = "Days until expiration")]
        expires: u32,
    },
    /// List all items sorted by expiration (soonest first)
    List,
    /// Suggest the next item to consume (earliest expiration)
    Suggest,
}

fn main() {
    let cli = Cli::parse();
    // Load existing inventory (or start empty)
    let mut items = match load_inventory(&cli.inventory) {
        Ok(v) => v,
        Err(e) => {
            eprintln!("Error loading inventory: {}", e);
            std::process::exit(1);
        }
    };

    match cli.command {
        Commands::Add { name, quantity, expires } => {
            let new_item = Item { name, quantity, expires_in_days: expires };
            items = add_item(items, new_item);
            if let Err(e) = save_inventory(&cli.inventory, &items) {
                eprintln!("Failed to save inventory: {}", e);
                std::process::exit(1);
            }
            println!("Item added successfully.");
        }
        Commands::List => {
            let sorted = sorted_by_expiration(items);
            if sorted.is_empty() {
                println!("Inventory is empty.");
            } else {
                for item in sorted {
                    println!("{name}: {qty} (expires in {days} days)",
                        name = item.name,
                        qty = item.quantity,
                        days = item.expires_in_days);
                }
            }
        }
        Commands::Suggest => {
            if let Some(item) = suggest_next(&items) {
                println!("You should consume: {name} (expires in {days} days, qty: {qty})",
                    name = item.name,
                    days = item.expires_in_days,
                    qty = item.quantity);
            } else {
                println!("Inventory is empty – nothing to suggest.");
            }
        }
    }
}
