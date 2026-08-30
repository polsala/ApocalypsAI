use clap::Parser;
use std::collections::HashMap;
use std::fs;
use std::path::{Path, PathBuf};
use walkdir::WalkDir;
use sha2::{Sha256, Digest};
use hex;

#[derive(Parser, Debug)]
#[clap(author, version, about = "Detects file system chrono-drift between two directories.", long_about = None)]
struct Args {
    /// The baseline directory to compare against.
    #[clap(short, long)]
    baseline: PathBuf,

    /// The current directory to check for anomalies.
    #[clap(short, long)]
    current: PathBuf,
}

/// Scans a directory and returns a HashMap of relative paths to SHA256 hashes.
fn scan_directory(root_path: &Path) -> Result<HashMap<PathBuf, String>, Box<dyn std::error::Error>> {
    let mut file_hashes = HashMap::new();

    for entry in WalkDir::new(root_path) {
        let entry = entry?;
        let path = entry.path();

        if path.is_file() {
            let relative_path = path.strip_prefix(root_path)?.to_path_buf();
            let mut file = fs::File::open(path)?;
            let mut hasher = Sha256::new();
            std::io::copy(&mut file, &mut hasher)?;
            let hash = hasher.finalize();
            file_hashes.insert(relative_path, hex::encode(hash));
        }
    }
    Ok(file_hashes)
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();

    println!("Scanning for Chrono-Drift...");
    println!("Baseline established from: {}", args.baseline.display());
    println!("Current reality check against: {}", args.current.display());
    println!();

    let baseline_files = scan_directory(&args.baseline)?;
    let current_files = scan_directory(&args.current)?;

    let mut new_files = Vec::new();
    let mut deleted_files = Vec::new();
    let mut modified_files = Vec::new();

    // Check for deleted and modified files
    for (baseline_path, baseline_hash) in &baseline_files {
        match current_files.get(baseline_path) {
            Some(current_hash) => {
                if baseline_hash != current_hash {
                    modified_files.push(baseline_path.clone());
                }
            }
            None => {
                deleted_files.push(baseline_path.clone());
            }
        }
    }

    // Check for new files
    for (current_path, _) in &current_files {
        if !baseline_files.contains_key(current_path) {
            new_files.push(current_path.clone());
        }
    }

    println!("--- Temporal Anomaly Report ---");

    if new_files.is_empty() && deleted_files.is_empty() && modified_files.is_empty() {
        println!("No significant chrono-drift detected. Reality remains stable... for now.");
    } else {
        if !new_files.is_empty() {
            println!("\nEmergent Chrono-Entities (New Files):");
            for path in new_files {
                println!("  - {}", path.display());
            }
        }

        if !deleted_files.is_empty() {
            println!("\nVanished Temporal Echoes (Deleted Files):");
            for path in deleted_files {
                println!("  - {}", path.display());
            }
        }

        if !modified_files.is_empty() {
            println!("\nDistorted Chrono-Signatures (Modified Files):");
            for path in modified_files {
                println!("  - {}", path.display());
            }
        }
    }

    Ok(())
}
