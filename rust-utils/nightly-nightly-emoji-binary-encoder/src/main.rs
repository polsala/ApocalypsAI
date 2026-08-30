use std::env;

use crate::encode_number;

fn print_usage() {
    eprintln!("Usage: nightly-emoji-binary-encoder <non-negative integer>");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        print_usage();
        std::process::exit(1);
    }
    let input = &args[1];
    match input.parse::<u64>() {
        Ok(num) => {
            let encoded = encode_number(num);
            println!("{}", encoded);
        }
        Err(_) => {
            eprintln!("Error: '{}' is not a valid non-negative integer.", input);
            std::process::exit(1);
        }
    }
}
