use std::env;
use std::io::{self, Read, Write};

// Import the library function
use nightly_cryptic_clipboard_keeper::xor;

fn print_usage() {
    eprintln!("Usage: {} <encrypt|decrypt> <passphrase>", env::args().next().unwrap_or_else(|| \"cli\".to_string()));
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
        print_usage();
        std::process::exit(1);
    }
    let _mode = &args[1]; // mode is kept for a friendly interface; XOR is symmetric
    let passphrase = args[2].as_bytes();

    // Read all of stdin
    let mut input = Vec::new();
    io::stdin().read_to_end(&mut input).expect("Failed to read stdin");

    // Apply XOR cipher
    let output = xor(&input, passphrase);

    // Write result to stdout
    io::stdout().write_all(&output).expect("Failed to write stdout");
}
