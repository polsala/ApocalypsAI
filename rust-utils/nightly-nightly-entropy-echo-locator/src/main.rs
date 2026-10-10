use std::fs::File;
use std::io::{self, Read};
use std::path::PathBuf;
use clap::Parser;

/// A high-performance CLI tool to calculate the Shannon entropy of files,
/// helping to identify potential 'signals' or anomalies in data streams.
#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
struct Args {
    /// Paths to one or more files to analyze.
    #[clap(value_parser)]
    files: Vec<PathBuf>,
}

fn calculate_entropy(path: &PathBuf) -> io::Result<f64> {
    let mut file = File::open(path)?;
    let mut buffer = [0; 4096];
    let mut byte_counts = [0usize; 256];
    let mut total_bytes = 0usize;

    loop {
        let bytes_read = file.read(&mut buffer)?;
        if bytes_read == 0 {
            break;
        }
        for &byte in &buffer[..bytes_read] {
            byte_counts[byte as usize] += 1;
            total_bytes += 1;
        }
    }

    if total_bytes == 0 {
        return Ok(0.0);
    }

    let mut entropy = 0.0;
    for &count in byte_counts.iter() {
        if count > 0 {
            let p = count as f64 / total_bytes as f64;
            entropy -= p * p.log2();
        }
    }

    Ok(entropy)
}

fn main() -> io::Result<()> {
    let args = Args::parse();

    if args.files.is_empty() {
        eprintln!("Error: No files provided. Use `nightly-entropy-echo-locator --help` for usage.");
        std::process::exit(1);
    }

    for file_path in args.files {
        match calculate_entropy(&file_path) {
            Ok(entropy) => {
                println!("File: {}, Entropy: {:.3} bits/byte", file_path.display(), entropy);
            }
            Err(e) => {
                eprintln!("Error processing file {}: {}", file_path.display(), e);
            }
        }
    }

    Ok(())
}
