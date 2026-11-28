use std::env;
use std::fs;
use std::process;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        eprintln!("Usage: {} <path-to-csv>", args[0]);
        process::exit(1);
    }
    let path = &args[1];
    let content = match fs::read_to_string(path) {
        Ok(c) => c,
        Err(e) => {
            eprintln!("Failed to read file {}: {}", path, e);
            process::exit(1);
        }
    };
    match eco_footprint_analyzer::compute_total(&content) {
        Ok(total) => println!("Total CO₂ footprint: {:.2} kg", total),
        Err(e) => {
            eprintln!("Error processing CSV: {}", e);
            process::exit(1);
        }
    }
}
