use std::error::Error;
use std::fs::File;
use std::io::{self, BufReader, Read};
use std::path::PathBuf;

use clap::Parser;
use serde::Deserialize;

#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
struct Args {
    /// Path to the input CSV file containing items, gloom factor, and sparkle potential.
    #[clap(value_parser)]
    input_file: PathBuf,
}

#[derive(Debug, Deserialize, PartialEq, Eq, PartialOrd, Ord, Clone)]
struct Item {
    item_name: String,
    gloom_factor: u8,
    sparkle_potential: u8,
    #[serde(skip)] // Don't deserialize this field from CSV
    survival_score: i32,
}

impl Item {
    /// Calculates the survival score for an item.
    /// Score = Sparkle Potential - Gloom Factor + 10 (to ensure positive scores for sorting).
    fn calculate_survival_score(&mut self) {
        self.survival_score = (self.sparkle_potential as i32) - (self.gloom_factor as i32) + 10;
    }

    /// Validates the gloom and sparkle factors are within the 1-10 range.
    fn validate_factors(&self) -> Result<(), String> {
        if !(1..=10).contains(&self.gloom_factor) {
            return Err(format!(
                "Gloom factor for '{}' is out of range (1-10): {}",
                self.item_name, self.gloom_factor
            ));
        }
        if !(1..=10).contains(&self.sparkle_potential) {
            return Err(format!(
                "Sparkle potential for '{}' is out of range (1-10): {}",
                self.item_name, self.sparkle_potential
            ));
        }
        Ok(())
    }
}

fn run(input_reader: impl Read) -> Result<(), Box<dyn Error>> {
    let mut rdr = csv::ReaderBuilder::new()
        .has_headers(false) // Assuming no header row for simplicity
        .from_reader(input_reader);

    let mut items: Vec<Item> = Vec::new();

    for result in rdr.deserialize() {
        let mut item: Item = result?;
        item.validate_factors()?;
        item.calculate_survival_score();
        items.push(item);
    }

    // Sort items by survival score in descending order
    items.sort_by(|a, b| b.survival_score.cmp(&a.survival_score));

    println!("Prioritized Scavenged Items:");
    println!("----------------------------");
    for (i, item) in items.iter().enumerate() {
        println!(
            "{}. {} (Survival Score: {}, Gloom: {}, Sparkle: {})",
            i + 1,
            item.item_name,
            item.survival_score,
            item.gloom_factor,
            item.sparkle_potential
        );
    }

    Ok(())
}

fn main() -> Result<(), Box<dyn Error>> {
    let args = Args::parse();

    let file = File::open(&args.input_file)?;
    let reader = BufReader::new(file);

    run(reader)
}
