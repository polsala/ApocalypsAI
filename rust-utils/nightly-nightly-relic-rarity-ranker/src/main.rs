use clap::Parser;
use serde::{Deserialize, Serialize};
use std::fs;
use std::io::{self, Write};

/// A scavenged item with various attributes.
#[derive(Debug, Deserialize, Serialize, Clone, PartialEq)]
pub struct Relic {
    pub name: String,
    pub category: String,
    pub condition: u8, // 0-100
    pub scarcity_factor: u8, // 0-10
}

impl Relic {
    /// Calculates the rarity score for the relic.
    /// Rarity Score: scarcity_factor * (1.0 + condition / 100.0)
    pub fn rarity_score(&self) -> f64 {
        self.scarcity_factor as f64 * (1.0 + self.condition as f64 / 100.0)
    }

    /// Calculates the utility score for the relic.
    /// Utility Score: base_utility_value_by_category * (condition / 100.0)
    pub fn utility_score(&self) -> f64 {
        let base_utility = match self.category.to_lowercase().as_str() {
            "weapon" => 10.0,
            "tool" => 9.0,
            "food" => 7.0,
            "data" => 6.0,
            "decoration" => 1.0,
            _ => 3.0, // Default for unknown categories
        };
        base_utility * (self.condition as f64 / 100.0)
    }
}

#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
struct Args {
    /// Path to the JSON file containing relics.
    #[clap(short, long)]
    input: String,

    /// Sort the output by 'rarity' or 'utility'.
    #[clap(short, long, default_value = "rarity")]
    sort_by: String,

    /// Output format: 'json' or 'text'.
    #[clap(short, long, default_value = "text")]
    output_format: String,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();

    let file_content = fs::read_to_string(&args.input)
        .map_err(|e| format!("Failed to read input file {}: {}", args.input, e))?;

    let mut relics: Vec<Relic> = serde_json::from_str(&file_content)
        .map_err(|e| format!("Failed to parse JSON from {}: {}", args.input, e))?;

    match args.sort_by.to_lowercase().as_str() {
        "rarity" => relics.sort_by(|a, b| b.rarity_score().partial_cmp(&a.rarity_score()).unwrap_or(std::cmp::Ordering::Equal)),
        "utility" => relics.sort_by(|a, b| b.utility_score().partial_cmp(&a.utility_score()).unwrap_or(std::cmp::Ordering::Equal)),
        _ => return Err(format!("Invalid sort_by option: {}. Use 'rarity' or 'utility'.", args.sort_by).into()),
    }

    match args.output_format.to_lowercase().as_str() {
        "json" => {
            let json_output = serde_json::to_string_pretty(&relics)?;
            io::stdout().write_all(json_output.as_bytes())?;
            io::stdout().write_all(b"\n")?;
        },
        "text" => {
            for relic in relics {
                println!(
                    "Name: {}, Category: {}, Condition: {}, Scarcity: {}, Rarity Score: {:.2}, Utility Score: {:.2}",
                    relic.name,
                    relic.category,
                    relic.condition,
                    relic.scarcity_factor,
                    relic.rarity_score(),
                    relic.utility_score()
                );
            }
        },
        _ => return Err(format!("Invalid output_format option: {}. Use 'json' or 'text'.", args.output_format).into()),
    }

    Ok(())
}
