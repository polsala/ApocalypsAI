use std::env;
use std::io::{self, Read};

fn generate_qr_ascii(data: &str) -> String {
    // Create QR code using the `qrcode` crate.
    let code = qrcode::QrCode::new(data.as_bytes()).expect("Failed to create QR code");
    let matrix = code.render::<bool>().build();

    // Render the matrix as ASCII. Dark modules are "██" by default.
    // Every 7th dark module is rendered as "▓▓" to give a subtle glitch effect.
    let mut output = String::new();
    let mut dark_counter = 0usize;
    for row in matrix.iter() {
        for &module in row.iter() {
            if module {
                dark_counter += 1;
                let block = if dark_counter % 7 == 0 { "▓▓" } else { "██" };
                output.push_str(block);
            } else {
                output.push_str("  ");
            }
        }
        output.push('\n');
    }
    output
}

fn main() {
    // Collect command‑line arguments (skip the binary name).
    let args: Vec<String> = env::args().skip(1).collect();
    let input = if !args.is_empty() {
        args.join(" ")
    } else {
        // Read from stdin if no arguments were supplied.
        let mut buffer = String::new();
        io::stdin().read_to_string(&mut buffer).expect("Failed to read stdin");
        buffer
    };
    let trimmed = input.trim();
    if trimmed.is_empty() {
        eprintln!("Error: No input provided.");
        std::process::exit(1);
    }
    let ascii_qr = generate_qr_ascii(trimmed);
    println!("{}", ascii_qr);
}
