use clap::Parser;
use std::{fs, path::PathBuf, io::{self, Write}};
use sha2::{Sha256, Digest};
use nightly_chrono_hash_stabilizer::calculate_stability; // Import from lib.rs

#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
struct Args {
    /// Path to the file to stabilize
    #[clap(short, long, value_parser)]
    file: PathBuf,

    /// Number of temporal observations (hashes) to perform
    #[clap(short, long, value_parser, default_value_t = 10)]
    iterations: u32,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();

    if !args.file.exists() {
        eprintln!("Error: File not found at {:?}", args.file);
        std::process::exit(1);
    }

    if args.iterations == 0 {
        eprintln!("Error: Iterations must be greater than 0.");
        std::process::exit(1);
    }

    println!("Stabilizing chrono-hash for: {:?}", args.file);
    println!("Performing {} temporal observations...", args.iterations);

    let mut hashes: Vec<String> = Vec::new();
    for _i in 0..args.iterations {
        // In a real "temporal distortion" scenario, we'd expect the file content
        // to *potentially* change between reads. For this utility, we simulate
        // this by simply re-reading and re-hashing. If the file system is stable,
        // all hashes will be identical.
        let content = fs::read(&args.file)?;
        let mut hasher = Sha256::new();
        hasher.update(&content);
        let hash = format!("{:x}", hasher.finalize());
        hashes.push(hash);
        print!("."); // Progress indicator
        io::stdout().flush()?;
    }
    println!(); // Newline after progress dots

    let (stable_hash, stability_score) = calculate_stability(&hashes);

    println!("\n--- Chrono-Hash Stability Report ---");
    println!("File: {:?}", args.file);
    println!("Observations: {}", args.iterations);
    println!("Most Stable Chrono-Hash: {}", stable_hash);
    println!("Temporal Stability Score: {:.2}%", stability_score);

    if stability_score == 100.0 {
        println!("Status: Perfectly stable across all temporal observations. A beacon of consistency!");
    } else if stability_score > 75.0 {
        println!("Status: Mostly stable, but minor temporal ripples detected. Keep an eye out!");
    } else if stability_score > 50.0 {
        println!("Status: Significant temporal drift detected. Reality might be... shifty.");
    } else {
        println!("Status: Highly unstable! Seek immediate temporal stabilization protocols!");
    }

    Ok(())
}
