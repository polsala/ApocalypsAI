use std::io::{self, Read};

fn main() {
    // Collect command‑line arguments (excluding the binary name)
    let args: Vec<String> = std::env::args().skip(1).collect();
    let input = if !args.is_empty() {
        // If arguments are provided, join them with spaces (mirrors typical CLI behaviour)
        args.join(" ")
    } else {
        // No arguments – read the entire STDIN
        let mut buffer = String::new();
        io::stdin().read_to_string(&mut buffer).expect("Failed to read STDIN");
        // Trim trailing newlines for cleaner output
        buffer.trim_end().to_string()
    };

    // Use the library function for the actual transformation
    let output = nightly_rot13_cli::rot13(&input);
    println!("{}", output);
}
