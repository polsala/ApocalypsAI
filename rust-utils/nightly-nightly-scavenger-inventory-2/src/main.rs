use clap::Parser;
use scavenger_inventory::{parse_items, suggest_drops, Item};

/// Simple scavenger inventory tracker.
#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Maximum weight the scavenger can carry.
    max_weight: f64,
    /// Items in the form name:weight (e.g. water:2.5)
    #[arg(required = true)]
    items: Vec<String>,
}

fn main() {
    let args = Args::parse();
    let items = parse_items(&args.items);
    let total: f64 = items.iter().map(|i| i.weight).sum();
    println!("Total weight: {}", total);
    if total <= args.max_weight {
        return;
    }
    let excess = total - args.max_weight;
    println!("Limit exceeded by {}", excess);
    let drops = suggest_drops(&items, excess);
    if drops.is_empty() {
        println!("No single item can reduce the excess enough.");
    } else {
        let drop_list: Vec<String> = drops.iter().map(|i| format!("{} ({})", i.name, i.weight)).collect();
        println!("Suggested items to drop: {}", drop_list.join(", "));
    }
}
