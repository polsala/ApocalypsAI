use std::io::{self, Read};
use scavenger_knapsack::compute_knapsack;
use scavenger_knapsack::{Item, Payload};

fn main() {
    // Read entire stdin
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).expect("Failed to read stdin");
    // Parse JSON
    let payload: Payload = serde_json::from_str(&input).expect("Invalid JSON payload");
    // Compute optimal set
    let result = compute_knapsack(&payload);
    // Output JSON array of names
    let output = serde_json::to_string(&result).expect("Failed to serialize result");
    println!("{}", output);
}
