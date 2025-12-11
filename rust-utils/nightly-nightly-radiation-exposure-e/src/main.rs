use std::env;
use std::fs;
use std::io::{self, Read};

fn read_input() -> String {
    let args: Vec<String> = env::args().collect();
    if args.len() > 1 {
        // Read from file path provided as first argument
        fs::read_to_string(&args[1]).unwrap_or_default()
    } else {
        // Read from stdin
        let mut buffer = String::new();
        let _ = io::stdin().read_to_string(&mut buffer).unwrap_or(0);
        buffer
    }
}

fn main() {
    let input = read_input();
    let total = radiation_exposure_estimator::parse_and_sum(&input);
    println!("Total radiation dose: {:.2} mSv", total);
}
