use std::env;
use std::fs::File;
use std::io::{self, Read, Write};

/// Compute Shannon entropy (bits per byte) for a slice of bytes.
fn compute_entropy(data: &[u8]) -> f64 {
    if data.is_empty() {
        return 0.0;
    }
    let mut freq = [0usize; 256];
    for &b in data {
        freq[b as usize] += 1;
    }
    let len = data.len() as f64;
    let mut entropy = 0.0f64;
    for &count in &freq {
        if count == 0 {
            continue;
        }
        let p = count as f64 / len;
        entropy -= p * p.log2();
    }
    entropy
}

fn read_input(path: &str) -> io::Result<Vec<u8>> {
    if path == "-" {
        // Read from stdin
        let mut buffer = Vec::new();
        io::stdin().lock().read_to_end(&mut buffer)?;
        Ok(buffer)
    } else {
        let mut file = File::open(path)?;
        let mut buffer = Vec::new();
        file.read_to_end(&mut buffer)?;
        Ok(buffer)
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        eprintln!("Usage: {} <file-path|->", args[0]);
        std::process::exit(1);
    }
    let path = &args[1];
    match read_input(path) {
        Ok(data) => {
            let entropy = compute_entropy(&data);
            println!("Entropy: {:.4} bits/byte", entropy);
            if entropy >= 4.5 {
                eprintln!("⚠️ High‑entropy data detected! This may be a secret or compressed content.");
            }
        }
        Err(e) => {
            eprintln!("Error reading '{}': {}", path, e);
            std::process::exit(1);
        }
    }
}
