use std::env;
use std::fs::File;
use std::io::{self, Read};

fn main() {
    // Determine input source: file argument or STDIN
    let args: Vec<String> = env::args().collect();
    let data = if args.len() > 1 {
        // Read from the provided file path
        let path = &args[1];
        match read_file(path) {
            Ok(bytes) => bytes,
            Err(e) => {
                eprintln!("Error reading file '{}': {}", path, e);
                std::process::exit(1);
            }
        }
    } else {
        // Read from STDIN
        match read_stdin() {
            Ok(bytes) => bytes,
            Err(e) => {
                eprintln!("Error reading STDIN: {}", e);
                std::process::exit(1);
            }
        }
    };

    if data.is_empty() {
        eprintln!("No data provided to analyze.");
        std::process::exit(1);
    }

    let entropy = compute_shannon_entropy(&data);
    println!("Entropy: {:.4} bits/byte", entropy);
}

fn read_file(path: &str) -> io::Result<Vec<u8>> {
    let mut file = File::open(path)?;
    let mut buffer = Vec::new();
    file.read_to_end(&mut buffer)?;
    Ok(buffer)
}

fn read_stdin() -> io::Result<Vec<u8>> {
    let mut buffer = Vec::new();
    let stdin = io::stdin();
    let mut handle = stdin.lock();
    handle.read_to_end(&mut buffer)?;
    Ok(buffer)
}

/// Compute Shannon entropy (bits per byte) for a slice of bytes.
fn compute_shannon_entropy(data: &[u8]) -> f64 {
    use std::collections::HashMap;
    let mut freq: HashMap<u8, usize> = HashMap::new();
    for &b in data {
        *freq.entry(b).or_insert(0) += 1;
    }
    let len = data.len() as f64;
    let mut entropy = 0.0_f64;
    for &count in freq.values() {
        let p = (count as f64) / len;
        entropy -= p * p.log2();
    }
    entropy
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_entropy_known_string() {
        // "aaaaabbbbcc" -> a:5, b:4, c:2 (total 11)
        let input = b"aaaaabbbbcc";
        let entropy = compute_shannon_entropy(input);
        // Expected entropy ≈ 1.493 bits/byte (calculated manually)
        let expected = 1.4930_f64;
        let diff = (entropy - expected).abs();
        assert!(diff < 0.001, "entropy {} differs from expected {}", entropy, expected);
    }

    #[test]
    fn test_entropy_all_same() {
        let input = b"aaaaaaaaaa"; // uniform data -> entropy 0
        let entropy = compute_shannon_entropy(input);
        assert!((entropy).abs() < 1e-10);
    }

    #[test]
    fn test_entropy_two_symbols_equal() {
        let input = b"01010101"; // 4 zeros, 4 ones
        let entropy = compute_shannon_entropy(input);
        // For two equally likely symbols, entropy = 1 bit/byte
        let diff = (entropy - 1.0).abs();
        assert!(diff < 1e-10);
    }
}
