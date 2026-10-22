use std::fs;
use std::io::{self, BufRead};
use std::path::PathBuf;
use clap::Parser;

mod item;
use item::{Item, Rarity, Condition};

#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
struct Args {
    /// Path to the input file containing scavenged items
    #[clap(short, long, value_parser)]
    input: PathBuf,

    /// Sort order: 'asc' (ascending score) or 'desc' (descending score)
    #[clap(short, long, value_parser, default_value = "desc")]
    order: String,
}

fn main() -> io::Result<()> {
    let args = Args::parse();

    let file_content = fs::read_to_string(&args.input)?;
    let mut items = Vec::new();

    for line in file_content.lines() {
        if line.trim().is_empty() {
            continue;
        }
        match Item::from_str(line) {
            Ok(item) => items.push(item),
            Err(e) => eprintln!("Warning: Could not parse line '{}': {}", line, e),
        }
    }

    if args.order == "asc" {
        items.sort_by(|a, b| a.survival_score().partial_cmp(&b.survival_score()).unwrap_or(std::cmp::Ordering::Equal));
    } else {
        items.sort_by(|a, b| b.survival_score().partial_cmp(&a.survival_score()).unwrap_or(std::cmp::Ordering::Equal));
    }

    println!("--- Scavenged Item Prioritization ---");
    for item in items {
        println!("{}", item);
    }

    Ok(())
}
