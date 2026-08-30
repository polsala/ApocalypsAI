use std::env;
use std::fs;
use std::process;

mod lib;
use lib::{solve_knapsack, Input};

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        eprintln!("Usage: {} <input-json-file>", args[0]);
        process::exit(1);
    }
    let input_path = &args[1];
    let data = fs::read_to_string(input_path).unwrap_or_else(|err| {
        eprintln!("Failed to read {}: {}", input_path, err);
        process::exit(1);
    });
    let input: Input = serde_json::from_str(&data).unwrap_or_else(|err| {
        eprintln!("Invalid JSON in {}: {}", input_path, err);
        process::exit(1);
    });
    let selected = solve_knapsack(&input);
    let output = serde_json::to_string(&selected).expect("Serialization failed");
    println!("{}", output);
}
