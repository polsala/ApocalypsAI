use clap::Parser;
use std::fs;

/// Simple CLI that reads a file containing a whimsical QR string and prints the decoded message.
#[derive(Parser)]
#[command(name = "qr-reverse-decoder")]
#[command(about = "Decode whimsical QR strings encoded as reversed text with a QR: prefix")]
struct Args {
    /// Path to the file containing the QR string
    input: String,
}

fn main() {
    let args = Args::parse();
    match fs::read_to_string(&args.input) {
        Ok(content) => {
            // Trim to remove trailing newlines/spaces that might be present in the file
            match qr_reverse_decoder::decode_qr(content.trim()) {
                Some(decoded) => println!("{}", decoded),
                None => eprintln!("Failed to decode: invalid QR format"),
            }
        }
        Err(e) => eprintln!("Error reading file: {}", e),
    }
}
