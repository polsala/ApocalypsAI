use std::{collections::HashMap, fs, io::{self, Read}};
use clap::Parser;

#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
struct Args {
    /// Path to the manifest file. If not provided, reads from stdin.
    #[clap(short, long)]
    file: Option<String>,
}

#[derive(Debug, PartialEq, Eq, Hash, Clone, Copy)]
enum Category {
    Food,
    Water,
    Tools,
    Components,
    Medical,
    Junk,
    Unknown,
}

impl Category {
    fn classify(item_name: &str) -> Category {
        let lower_name = item_name.to_lowercase();
        if lower_name.contains("canned") || lower_name.contains("ration") || lower_name.contains("berry") || lower_name.contains("meat") || lower_name.contains("veg") || lower_name.contains("dried") {
            Category::Food
        } else if lower_name.contains("water") || lower_name.contains("bottle") || lower_name.contains("purifier") {
            Category::Water
        } else if lower_name.contains("wrench") || lower_name.contains("hammer") || lower_name.contains("knife") || lower_name.contains("saw") || lower_name.contains("tool") || lower_name.contains("pipe") {
            Category::Tools
        } else if lower_name.contains("scrap") || lower_name.contains("wire") || lower_name.contains("gear") || lower_name.contains("circuit") || lower_name.contains("bolt") || lower_name.contains("nut") {
            Category::Components
        } else if lower_name.contains("bandage") || lower_name.contains("medkit") || lower_name.contains("antiseptic") || lower_name.contains("medicine") || lower_name.contains("aid") {
            Category::Medical
        } else if lower_name.contains("rock") || lower_name.contains("dirt") || lower_name.contains("broken") || lower_name.contains("old") || lower_name.contains("rusty") {
            Category::Junk
        }
        else {
            Category::Unknown
        }
    }
}

fn parse_manifest(input: &str) -> HashMap<Category, HashMap<String, u32>> {
    let mut categorized_items: HashMap<Category, HashMap<String, u32>> = HashMap::new();

    for line in input.lines() {
        let trimmed_line = line.trim();
        if trimmed_line.is_empty() {
            continue;
        }

        let mut quantity = 1;
        let mut item_name = trimmed_line.to_string();

        if let Some((qty_str, name_part)) = trimmed_line.split_once('x') {
            if let Ok(q) = qty_str.trim().parse::<u32>() {
                quantity = q;
                item_name = name_part.trim().to_string();
            }
        }

        let category = Category::classify(&item_name);
        let entry = categorized_items.entry(category).or_default();
        *entry.entry(item_name).or_insert(0) += quantity;
    }
    categorized_items
}

fn main() -> io::Result<()> {
    let args = Args::parse();

    let input_content = if let Some(file_path) = args.file {
        fs::read_to_string(file_path)?
    } else {
        let mut buffer = String::new();
        io::stdin().read_to_string(&mut buffer)?;
        buffer
    };

    let categorized_items = parse_manifest(&input_content);

    println!("--- Scavenger's Manifest Analysis ---");
    if categorized_items.is_empty() {
        println!("No items found in manifest. Time to scavenge!");
    } else {
        let mut sorted_categories: Vec<_> = categorized_items.keys().collect();
        sorted_categories.sort_by_key(|c| format!("{:?}", c)); // Sort categories alphabetically for consistent output

        for category in sorted_categories {
            println!("\n[{:?}]", category);
            let items = categorized_items.get(category).unwrap();
            let mut sorted_items: Vec<_> = items.iter().collect();
            sorted_items.sort_by_key(|(name, _)| *name); // Sort items alphabetically

            for (item_name, count) in sorted_items {
                println!("  - {}: {}", item_name, count);
            }
        }
    }

    Ok(())
}
