use std::env;
use std::fs::File;
use std::io::{self, BufRead, BufReader};

mod lib;
use lib::{Item, knapsack};

fn parse_csv<R: BufRead>(reader: R) -> io::Result<Vec<Item>> {
    let mut items = Vec::new();
    for line_res in reader.lines() {
        let line = line_res?;
        if line.trim().is_empty() {
            continue;
        }
        let parts: Vec<&str> = line.split(',').map(|s| s.trim()).collect();
        if parts.len() != 3 {
            return Err(io::Error::new(io::ErrorKind::InvalidData, "Each line must have three comma‑separated fields"));
        }
        let name = parts[0].to_string();
        let weight: u32 = parts[1].parse().map_err(|_| io::Error::new(io::ErrorKind::InvalidData, "Invalid weight"))?;
        let value: u32 = parts[2].parse().map_err(|_| io::Error::new(io::ErrorKind::InvalidData, "Invalid value"))?;
        items.push(Item { name, weight, value });
    }
    Ok(items)
}

fn print_usage() {
    eprintln!("Usage: nightly-scavenger-knapsack --capacity <MAX_WEIGHT> --items <CSV_FILE>");
}

fn main() -> io::Result<()> {
    let args: Vec<String> = env::args().collect();
    let mut capacity_opt: Option<u32> = None;
    let mut items_path_opt: Option<String> = None;

    let mut i = 1;
    while i < args.len() {
        match args[i].as_str() {
            "--capacity" => {
                if i + 1 >= args.len() {
                    print_usage();
                    return Err(io::Error::new(io::ErrorKind::InvalidInput, "Missing capacity value"));
                }
                capacity_opt = Some(args[i + 1].parse().map_err(|_| io::Error::new(io::ErrorKind::InvalidInput, "Invalid capacity"))?);
                i += 2;
            }
            "--items" => {
                if i + 1 >= args.len() {
                    print_usage();
                    return Err(io::Error::new(io::ErrorKind::InvalidInput, "Missing items file"));
                }
                items_path_opt = Some(args[i + 1].clone());
                i += 2;
            }
            _ => {
                print_usage();
                return Err(io::Error::new(io::ErrorKind::InvalidInput, "Unknown argument"));
            }
        }
    }

    let capacity = match capacity_opt {
        Some(c) => c,
        None => {
            print_usage();
            return Err(io::Error::new(io::ErrorKind::InvalidInput, "Capacity not provided"));
        }
    };

    let items_path = match items_path_opt {
        Some(p) => p,
        None => {
            print_usage();
            return Err(io::Error::new(io::ErrorKind::InvalidInput, "Items file not provided"));
        }
    };

    let file = File::open(items_path)?;
    let reader = BufReader::new(file);
    let items = parse_csv(reader)?;

    let selected = knapsack(&items, capacity);
    println!("{}", selected.join(", "));
    Ok(())
}
