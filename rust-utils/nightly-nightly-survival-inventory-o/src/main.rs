use clap::Parser;
use nightly_survival_inventory_optimizer::Item;
use nightly_survival_inventory_optimizer::optimal_items;

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Comma‑separated list of items in the form name:weight:utility
    #[arg(short, long)]
    items: String,

    /// Maximum total weight you can carry
    #[arg(short, long)]
    capacity: usize,
}

fn parse_items(s: &str) -> Vec<Item> {
    s.split(',')
        .filter_map(|part| {
            let mut parts = part.split(':');
            let name = parts.next()?.trim().to_string();
            let weight = parts.next()?.trim().parse::<usize>().ok()?;
            let utility = parts.next()?.trim().parse::<usize>().ok()?;
            Some(Item { name, weight, utility })
        })
        .collect()
}

fn main() {
    let args = Args::parse();
    let items = parse_items(&args.items);
    let optimal = optimal_items(&items, args.capacity);
    let total_weight: usize = optimal.iter().map(|i| i.weight).sum();
    let total_utility: usize = optimal.iter().map(|i| i.utility).sum();
    println!("Optimal items (total weight: {}kg, total utility: {}):", total_weight, total_utility);
    for item in optimal {
        println!("- {} ({}kg, utility {})", item.name, item.weight, item.utility);
    }
}
