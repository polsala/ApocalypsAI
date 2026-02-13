use std::env;
use std::io::{self, Read};

use nightly_entropy_analyzer::compute_entropy;

fn main() {
    // Gather input either from command‑line arguments or stdin
    let args: Vec<String> = env::args().collect();
    let input = if args.len() > 1 {
        args[1..].join(" ")
    } else {
        let mut buffer = String::new();
        io::stdin()
            .read_to_string(&mut buffer)
            .expect("Failed to read stdin");
        buffer.trim_end().to_string()
    };
    let entropy = compute_entropy(&input);
    println!("{:.4}", entropy);
}
