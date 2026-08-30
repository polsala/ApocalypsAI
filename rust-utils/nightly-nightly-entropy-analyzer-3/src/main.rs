use std::env;
use nightly_entropy_analyzer::compute_entropy;

fn main() {
    let args: Vec<String> = env::args().skip(1).collect();
    if args.is_empty() {
        eprintln!("Usage: {} <string>", env::args().next().unwrap());
        std::process::exit(1);
    }
    let input = args.join(" ");
    let entropy = compute_entropy(&input);
    println!("Entropy: {:.6} bits per character", entropy);
}
