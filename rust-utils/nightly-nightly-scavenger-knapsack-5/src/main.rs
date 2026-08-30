use std::io::{self, Read};

fn main() {
    // Expect exactly one argument: the capacity
    let args: Vec<String> = std::env::args().collect();
    if args.len() != 2 {
        eprintln!("Usage: {} <capacity>", args[0]);
        std::process::exit(1);
    }
    let capacity: u32 = match args[1].parse() {
        Ok(v) => v,
        Err(_) => {
            eprintln!("Capacity must be a positive integer");
            std::process::exit(1);
        }
    };

    // Read all lines from stdin. Each line: "name weight value"
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).expect("Failed to read stdin");
    let mut weights = Vec::new();
    let mut values = Vec::new();
    for line in input.lines() {
        let parts: Vec<&str> = line.split_whitespace().collect();
        if parts.len() != 3 {
            // ignore malformed lines
            continue;
        }
        // parts[0] is the name – we don't need it for the algorithm
        let w: u32 = parts[1].parse().unwrap_or(0);
        let v: u32 = parts[2].parse().unwrap_or(0);
        weights.push(w);
        values.push(v);
    }

    let max_value = scavenger_knapsack::knapsack(&weights, &values, capacity);
    println!("Maximum value: {}", max_value);
}
