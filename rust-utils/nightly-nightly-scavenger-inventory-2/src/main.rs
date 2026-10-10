use std::env;
use std::fs::File;
use std::io::{self, BufRead, BufReader};
use std::collections::HashMap;
use chrono::{NaiveDate, Utc, Duration};
use rand::seq::SliceRandom;

#[derive(Debug, Clone)]
struct Item {
    name: String,
    category: String,
    quantity: i32,
    expiration: NaiveDate,
}

fn parse_csv<R: BufRead>(reader: R) -> io::Result<Vec<Item>> {
    let mut lines = reader.lines();
    // Skip header
    let header = match lines.next() {
        Some(l) => l?,
        None => return Ok(vec![]),
    };
    if header.trim() != "name,category,quantity,expiration_date" {
        return Err(io::Error::new(io::ErrorKind::InvalidData, "Invalid CSV header"));
    }
    let mut items = Vec::new();
    for line_res in lines {
        let line = line_res?;
        if line.trim().is_empty() { continue; }
        let parts: Vec<&str> = line.split(',').collect();
        if parts.len() != 4 {
            return Err(io::Error::new(io::ErrorKind::InvalidData, "Malformed CSV line"));
        }
        let name = parts[0].trim().to_string();
        let category = parts[1].trim().to_string();
        let quantity: i32 = parts[2].trim().parse().map_err(|_| io::Error::new(io::ErrorKind::InvalidData, "Invalid quantity"))?;
        let expiration = NaiveDate::parse_from_str(parts[3].trim(), "%Y-%m-%d")
            .map_err(|_| io::Error::new(io::ErrorKind::InvalidData, "Invalid date"))?;
        items.push(Item { name, category, quantity, expiration });
    }
    Ok(items)
}

fn category_totals(items: &[Item]) -> HashMap<String, i32> {
    let mut map = HashMap::new();
    for item in items {
        *map.entry(item.category.clone()).or_insert(0) += item.quantity;
    }
    map
}

fn expiring_soon(items: &[Item], days: i64) -> Vec<&Item> {
    let today = Utc::today().naive_utc();
    items.iter()
        .filter(|it| {
            let diff = it.expiration - today;
            diff.num_days() >= 0 && diff.num_days() <= days
        })
        .collect()
}

fn random_tip() -> &'static str {
    const TIPS: &[&str] = &[
        "Never trust a silent wind.",
        "A full belly makes a quiet night.",
        "Keep your blade sharp and your mind sharper.",
        "Water is worth more than gold.",
        "When in doubt, hide in the shadows.",
    ];
    let mut rng = rand::thread_rng();
    TIPS.choose(&mut rng).unwrap_or(&"Stay safe.")
}

fn print_report(items: &[Item]) {
    println!("=== Scavenger Inventory Report ===\n");
    // Category totals
    println!("-- Totals by Category --");
    for (cat, qty) in category_totals(items) {
        println!("{:<12}: {}", cat, qty);
    }
    // Expiring soon
    println!("\n-- Items Expiring Within 7 Days --");
    let soon = expiring_soon(items, 7);
    if soon.is_empty() {
        println!("(none)");
    } else {
        for it in soon {
            let days_left = (it.expiration - Utc::today().naive_utc()).num_days();
            println!("{:<20} ({} days left)", it.name, days_left);
        }
    }
    // Random tip
    println!("\nSurvival Tip: {}", random_tip());
}

fn usage() {
    eprintln!("Usage: nightly-scavenger-inventory <path-to-csv>");
}

fn main() -> io::Result<()> {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        usage();
        std::process::exit(1);
    }
    let path = &args[1];
    let file = File::open(path)?;
    let reader = BufReader::new(file);
    let items = parse_csv(reader)?;
    if items.is_empty() {
        println!("No items found in inventory.");
        return Ok(());
    }
    print_report(&items);
    Ok(())
}
