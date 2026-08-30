use std::collections::HashMap;
use std::fs::File;
use std::io::{self, Read};
use std::path::PathBuf;
use clap::Parser;

#[derive(Parser, Debug)]
#[clap(author, version, about = "Extracts 'void whispers' from binary files by identifying repeating byte patterns.", long_about = None)]
struct Args {
    /// Path to the binary file to scan
    #[clap(short, long, value_parser)]
    file: PathBuf,

    /// Length of byte patterns to search for (e.g., 2, 4, 8)
    #[clap(short, long, value_parser, default_value_t = 4)]
    pattern_length: usize,

    /// Number of top patterns to report
    #[clap(short, long, value_parser, default_value_t = 10)]
    top_n: usize,
}

fn main() -> io::Result<()> {
    let args = Args::parse();

    if !args.file.exists() {
        eprintln!("Error: File not found at {:?}", args.file);
        std::process::exit(1);
    }

    let mut file = File::open(&args.file)?;
    let mut buffer = Vec::new();
    file.read_to_end(&mut buffer)?;

    if buffer.len() < args.pattern_length {
        println!("File is too small to find patterns of length {}.", args.pattern_length);
        return Ok(());
    }

    let mut pattern_counts: HashMap<Vec<u8>, usize> = HashMap::new();

    for i in 0..=buffer.len() - args.pattern_length {
        let pattern = buffer[i..i + args.pattern_length].to_vec();
        *pattern_counts.entry(pattern).or_insert(0) += 1;
    }

    let mut sorted_patterns: Vec<(&Vec<u8>, &usize)> = pattern_counts.iter().collect();
    sorted_patterns.sort_by(|a, b| b.1.cmp(a.1)); // Sort descending by count

    println!("Scanning '{:?}' for void whispers (pattern length: {} bytes)...", args.file, args.pattern_length);
    println!("------------------------------------------------------------------");

    if sorted_patterns.is_empty() {
        println!("No repeating patterns found. The void is silent.");
    } else {
        for (pattern, count) in sorted_patterns.iter().take(args.top_n) {
            let hex_pattern: Vec<String> = pattern.iter().map(|b| format!("{:02X}", b)).collect();
            let interpretation = interpret_pattern(pattern);
            println!("  Pattern: {} (Count: {}) -> {}", hex_pattern.join(" "), count, interpretation);
        }
    }

    Ok(())
}

fn interpret_pattern(pattern: &[u8]) -> String {
    match pattern {
        // Common patterns
        _ if pattern.iter().all(|&b| b == 0x00) => "Silence of the Void: A deep, unsettling calm.".to_string(),
        _ if pattern.iter().all(|&b| b == 0xFF) => "Echoes of the Old World: Remnants of forgotten data.".to_string(),
        // ASCII-like patterns
        _ if pattern.iter().all(|&b| b.is_ascii_alphanumeric() || b.is_ascii_whitespace() || b.is_ascii_punctuation()) => {
            let s = String::from_utf8_lossy(pattern);
            format!("Faint Human Traces: A garbled message from the past: \"{}\"", s.trim())
        },
        // Repetitive patterns (e.g., 01 01 01 01)
        _ if pattern.len() > 1 && pattern.iter().skip(1).all(|&b| b == pattern[0]) => {
            format!("Rhythmic Pulsation: A repeating beat from the data stream (byte: {:02X}).", pattern[0])
        },
        // Mixed patterns
        _ => "Cryptic Resonance: An unknown signal from the data depths.".to_string(),
    }
}
