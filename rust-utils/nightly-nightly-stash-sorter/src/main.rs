use clap::Parser;
use std::collections::{BTreeMap, HashMap};
use std::fs;
use std::io::{self, BufRead};
use serde::Deserialize;

#[derive(Parser, Debug)]
#[clap(author, version, about = "A high-performance CLI tool to categorize and sort scavenged items.", long_about = None)]
struct Args {
    /// Path to a file containing items (one per line). If not provided, reads from stdin.
    #[clap(short, long)]
    file: Option<String>,

    /// Path to a TOML file defining custom categories and keywords.
    #[clap(short, long)]
    rules: Option<String>,
}

#[derive(Debug, Deserialize, Clone)]
struct CategoryConfig {
    keywords: Vec<String>,
}

#[derive(Debug, Deserialize)]
struct RulesConfig {
    categories: HashMap<String, CategoryConfig>,
}

// Default categories and their keywords
pub fn default_categories() -> BTreeMap<String, Vec<String>> {
    let mut map = BTreeMap::new();
    map.insert("Sustenance".to_string(), vec!["food", "water", "ration", "can", "bottle", "berry", "fruit", "vegetable", "drink", "meal", "snack"].into_iter().map(String::from).collect());
    map.insert("Tools & Tech".to_string(), vec!["wrench", "hammer", "radio", "battery", "wire", "circuit", "tool", "device", "gear", "kit", "parts"].into_iter().map(String::from).collect());
    map.insert("Barter & Bling".to_string(), vec!["coin", "jewelry", "gem", "shiny", "bottlecap", "gold", "silver", "trinket", "currency", "valuable"].into_iter().map(String::from).collect());
    map.insert("Mysterious Artifacts".to_string(), vec!["orb", "rune", "scroll", "unknown", "glowing", "ancient", "relic", "artifact", "curio"].into_iter().map(String::from).collect());
    map
}

// Function to load custom rules from a TOML file
pub fn load_custom_rules(path: &str) -> Result<BTreeMap<String, Vec<String>>, String> {
    let contents = fs::read_to_string(path)
        .map_err(|e| format!("Failed to read rules file {}: {}", path, e))?;
    let config: RulesConfig = toml::from_str(&contents)
        .map_err(|e| format!("Failed to parse rules file {}: {}", path, e))?;

    let mut custom_map = BTreeMap::new();
    for (category_name, category_config) in config.categories {
        custom_map.insert(category_name, category_config.keywords);
    }
    Ok(custom_map)
}

// Function to categorize an item
pub fn categorize_item(item: &str, rules: &BTreeMap<String, Vec<String>>) -> String {
    let lower_item = item.to_lowercase();
    for (category, keywords) in rules.iter() {
        for keyword in keywords {
            if lower_item.contains(&keyword.to_lowercase()) {
                return category.clone();
            }
        }
    }
    "Miscellaneous".to_string()
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();

    let mut rules = default_categories();

    if let Some(rules_file) = args.rules {
        match load_custom_rules(&rules_file) {
            Ok(custom_rules) => {
                // Merge custom rules, overriding defaults if category names clash
                for (category_name, keywords) in custom_rules {
                    rules.insert(category_name, keywords);
                }
            },
            Err(e) => {
                eprintln!("Error loading custom rules: {}", e);
                std::process::exit(1);
            }
        }
    }

    let reader: Box<dyn BufRead> = match args.file {
        Some(file_path) => {
            let file = fs::File::open(&file_path)?;
            Box::new(io::BufReader::new(file))
        }
        None => Box::new(io::BufReader::new(io::stdin())),
    };

    let mut categorized_items: BTreeMap<String, Vec<String>> = BTreeMap::new();
    for category in rules.keys() {
        categorized_items.insert(category.clone(), Vec::new());
    }
    categorized_items.insert("Miscellaneous".to_string(), Vec::new()); // Ensure Miscellaneous is always present

    for line_result in reader.lines() {
        let item = line_result?;
        if item.trim().is_empty() {
            continue;
        }
        let category = categorize_item(&item, &rules);
        categorized_items.entry(category).or_default().push(item);
    }

    println!("--- Stash Report ---");
    for (category, items) in categorized_items.iter_mut() {
        items.sort(); // Sort items alphabetically within each category
        println!("\n[{}]", category);
        if items.is_empty() {
            println!("  - (No items)");
        } else {
            for item in items {
                println!("  - {}", item);
            }
        }
    }

    Ok(())
}
