use clap::Parser;
use std::error::Error;
use std::fs::File;
use csv::ReaderBuilder;
mod lib;
use lib::{Item, solve_knapsack};

/// Simple scavenger packer
#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Maximum carry weight
    #[arg(short, long)]
    weight: u32,

    /// CSV file with items (name,weight,value)
    #[arg(value_name = "FILE")]
    file: String,
}

fn read_items(path: &str) -> Result<Vec<Item>, Box<dyn Error>> {
    let file = File::open(path)?;
    let mut rdr = ReaderBuilder::new().has_headers(true).from_reader(file);
    let mut items = Vec::new();
    for result in rdr.deserialize() {
        let record: Item = result?;
        items.push(record);
    }
    Ok(items)
}

fn main() -> Result<(), Box<dyn Error>> {
    let args = Args::parse();
    let items = read_items(&args.file)?;
    let selected = solve_knapsack(&items, args.weight);
    let total_value: u32 = selected.iter().map(|i| i.value).sum();
    println!("Selected items (total value {}):", total_value);
    for item in selected {
        println!("- {} (weight {}, value {})", item.name, item.weight, item.value);
    }
    Ok(())
}
