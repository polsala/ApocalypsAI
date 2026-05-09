use std::collections::HashMap;
use std::env;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn main() -> io::Result<()> {
    let args: Vec<String> = env::args().collect();

    if args.len() != 3 {
        eprintln!("Usage: {} <manifest_file> <scavenged_file>", args[0]);
        std::process::exit(1);
    }

    let manifest_path = &args[1];
    let scavenged_path = &args[2];

    let manifest_items = read_items_from_file(manifest_path)?;
    let scavenged_items = read_items_from_file(scavenged_path)?;

    let mut manifest_counts: HashMap<String, usize> = HashMap::new();
    for item in manifest_items {
        *manifest_counts.entry(item).or_insert(0) += 1;
    }

    let mut scavenged_counts: HashMap<String, usize> = HashMap::new();
    for item in scavenged_items {
        *scavenged_counts.entry(item).or_insert(0) += 1;
    }

    println!("--- Scavenger's Manifest Audit Report ---");

    let mut missing_items = Vec::new();
    for (item, &manifest_count) in &manifest_counts {
        let scavenged_count = *scavenged_counts.get(item).unwrap_or(&0);
        if scavenged_count < manifest_count {
            missing_items.push(format!("{} ({} missing)", item, manifest_count - scavenged_count));
        }
    }

    if !missing_items.is_empty() {
        println!("\nMissing Items (in manifest, not enough scavenged):");
        for item in missing_items {
            println!("  - {}", item);
        }
    } else {
        println!("\nAll manifest items accounted for!");
    }

    let mut surplus_items = Vec::new();
    for (item, &scavenged_count) in &scavenged_counts {
        let manifest_count = *manifest_counts.get(item).unwrap_or(&0);
        if scavenged_count > manifest_count {
            surplus_items.push(format!("{} ({} surplus)", item, scavenged_count - manifest_count));
        }
    }

    if !surplus_items.is_empty() {
        println!("\nSurplus Items (scavenged, not in manifest or too many):");
        for item in surplus_items {
            println!("  - {}", item);
        }
    } else {
        println!("\nNo surplus items found!");
    }

    if missing_items.is_empty() && surplus_items.is_empty() {
        println!("\nManifest perfectly matched!");
    }

    Ok(())
}

fn read_items_from_file<P: AsRef<Path>>(filename: P) -> io::Result<Vec<String>> {
    let file = File::open(filename)?;
    let reader = io::BufReader::new(file);
    let mut items = Vec::new();
    for line in reader.lines() {
        let line = line?;
        let trimmed_line = line.trim();
        if !trimmed_line.is_empty() {
            items.push(trimmed_line.to_string());
        }
    }
    Ok(items)
}
