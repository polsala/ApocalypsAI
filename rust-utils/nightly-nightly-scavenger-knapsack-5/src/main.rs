use serde_json::{self, Value};
use std::io::{self, Read};

mod lib;
use lib::{compute_knapsack, Problem};

fn main() {
    // Read entire stdin
    let mut buffer = String::new();
    io::stdin().read_to_string(&mut buffer).expect("Failed to read stdin");
    // Parse JSON into Problem struct
    let problem: Problem = serde_json::from_str(&buffer).expect("Invalid JSON input");
    let selected = compute_knapsack(&problem);
    // Output as JSON array of strings
    let output = serde_json::to_string(&selected).expect("Failed to serialize output");
    println!("{}", output);
}
