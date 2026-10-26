use clap::Parser;
use serde::Deserialize;
use std::error::Error;
use std::fs::File;
use std::io::{self, Read};

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Path to the CSV file containing item data
    #[arg(short, long)]
    file: String,

    /// Maximum weight capacity of the container
    #[arg(short, long)]
    max_weight: f64,

    /// Maximum volume capacity of the container
    #[arg(short, long)]
    max_volume: f64,
}

#[derive(Debug, Deserialize, Clone)]
struct Item {
    name: String,
    value: u32,
    weight: f64,
    volume: f64,
}

impl Item {
    fn efficiency(&self) -> f64 {
        if self.weight == 0.0 {
            // Assign a very high efficiency to zero-weight items to prioritize them,
            // assuming they are highly desirable if they don't consume weight capacity.
            f64::MAX
        } else {
            self.value as f64 / self.weight
        }
    }
}

fn main() -> Result<(), Box<dyn Error>> {
    let args = Args::parse();

    let file_path = &args.file;
    let max_weight = args.max_weight;
    let max_volume = args.max_volume;

    let mut rdr = csv::Reader::from_path(file_path)?;
    let mut items: Vec<Item> = Vec::new();
    for result in rdr.deserialize() {
        let item: Item = result?;
        items.push(item);
    }

    // Sort items by efficiency (value/weight) in descending order
    items.sort_by(|a, b| b.efficiency().partial_cmp(&a.efficiency()).unwrap_or(std::cmp::Ordering::Equal));

    let mut packed_items: Vec<Item> = Vec::new();
    let mut current_weight = 0.0;
    let mut current_volume = 0.0;
    let mut total_value = 0;

    for item in items {
        if current_weight + item.weight <= max_weight && current_volume + item.volume <= max_volume {
            current_weight += item.weight;
            current_volume += item.volume;
            total_value += item.value;
            packed_items.push(item);
        }
    }

    println!("--- Scavenger Manifest Optimization Report ---");
    println!("Container Capacity: Max Weight = {:.2}kg, Max Volume = {:.2}L", max_weight, max_volume);
    println!("Packed Items:");
    if packed_items.is_empty() {
        println!("  No items could be packed within the given constraints.");
    } else {
        for item in &packed_items {
            println!("  - {} (Value: {}, Weight: {:.2}kg, Volume: {:.2}L)", item.name, item.value, item.weight, item.volume);
        }
    }
    println!("---------------------------------------------");
    println!("Total Packed Value: {}", total_value);
    println!("Total Packed Weight: {:.2}kg", current_weight);
    println!("Total Packed Volume: {:.2}L", current_volume);

    Ok(())
}
