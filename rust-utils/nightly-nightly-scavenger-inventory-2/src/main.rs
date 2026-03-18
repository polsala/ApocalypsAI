use chrono::NaiveDate;
use std::error::Error;
use std::io::{self, Read};

#[derive(Debug, PartialEq, Eq)]
struct Item {
    name: String,
    qty: u32,
    exp: NaiveDate,
}

fn parse_items(csv: &str) -> Result<Vec<Item>, Box<dyn Error>> {
    let mut items = Vec::new();
    for (i, line) in csv.lines().enumerate() {
        if i == 0 {
            // Skip header
            continue;
        }
        let parts: Vec<&str> = line.split(',').map(|s| s.trim()).collect();
        if parts.len() != 3 {
            return Err(format!("invalid CSV line: {}", line).into());
        }
        let name = parts[0].to_string();
        let qty: u32 = parts[1].parse()?;
        let exp = NaiveDate::parse_from_str(parts[2], "%Y-%m-%d")?;
        items.push(Item { name, qty, exp });
    }
    Ok(items)
}

fn sort_by_expiration(mut items: Vec<Item>) -> Vec<Item> {
    items.sort_by_key(|item| item.exp);
    items
}

fn suggest_use(items: &[Item]) -> Option<&Item> {
    items.first()
}

fn format_item(idx: usize, item: &Item) -> String {
    format!("{}. {} – {} pcs – expires {}", idx + 1, item.name, item.qty, item.exp)
}

fn run() -> Result<(), Box<dyn Error>> {
    // Read entire stdin
    let mut input = String::new();
    io::stdin().read_to_string(&mut input)?;
    let items = parse_items(&input)?;
    let sorted = sort_by_expiration(items);

    println!("Sorted inventory (soonest expiry first):");
    for (i, item) in sorted.iter().enumerate() {
        println!("{}", format_item(i, item));
    }

    if let Some(best) = suggest_use(&sorted) {
        println!("\nSuggestion: Use \"{}\" first!", best.name);
    } else {
        println!("\nNo items found.");
    }
    Ok(())
}

fn main() {
    if let Err(e) = run() {
        eprintln!("Error: {}", e);
        std::process::exit(1);
    }
}
