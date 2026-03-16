use std::env;
use nightly_apocalypse_cipher::cipher;

fn print_usage() {
    eprintln!("Usage: nightly-apocalypse-cipher \"text to cipher\"");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        print_usage();
        std::process::exit(1);
    }
    let input = &args[1];
    let output = cipher(input);
    println!("{}", output);
}
