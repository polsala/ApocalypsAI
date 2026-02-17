use clap::Parser;
use std::collections::HashMap;
use std::fs;
use std::path::{Path, PathBuf};
use std::time::{Duration, SystemTime};
use walkdir::WalkDir;
use sha2::{Sha256, Digest};

#[derive(Parser, Debug)]
#[command(author, version, about = "A high-performance CLI tool to identify and report digital debris like duplicate, empty, or ancient files across specified directories.", long_about = None)]
struct Args {
    /// Paths to scan for digital debris
    #[arg(required = true)]
    paths: Vec<PathBuf>,

    /// Detect duplicate files by content hash
    #[arg(long)]
    duplicates: bool,

    /// Detect empty files
    #[arg(long)]
    empty: bool,

    /// Detect files older than N days
    #[arg(long, value_name = "DAYS")]
    ancient: Option<u64>,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();

    let mut duplicate_hashes: HashMap<String, Vec<PathBuf>> = HashMap::new();
    let mut empty_files: Vec<PathBuf> = Vec::new();
    let mut ancient_files: Vec<PathBuf> = Vec::new();

    let now = SystemTime::now();
    let ancient_threshold = args.ancient.map(|days| now - Duration::from_secs(days * 24 * 60 * 60));

    let mut found_any_debris = false;

    for path in &args.paths {
        if !path.exists() {
            eprintln!("Warning: Path not found: {}", path.display());
            continue;
        }

        for entry in WalkDir::new(path).into_iter().filter_map(|e| e.ok()) {
            let entry_path = entry.path().to_path_buf();
            if entry_path.is_file() {
                let metadata = match fs::metadata(&entry_path) {
                    Ok(m) => m,
                    Err(e) => {
                        eprintln!("Error reading metadata for {}: {}", entry_path.display(), e);
                        continue;
                    }
                };

                // Check for empty files
                if args.empty && metadata.len() == 0 {
                    empty_files.push(entry_path.clone());
                    found_any_debris = true;
                }

                // Check for duplicates
                if args.duplicates {
                    match fs::read(&entry_path) {
                        Ok(bytes) => {
                            let mut hasher = Sha256::new();
                            hasher.update(&bytes);
                            let hash = format!("{:x}", hasher.finalize());
                            duplicate_hashes.entry(hash).or_default().push(entry_path.clone());
                        }
                        Err(e) => {
                            eprintln!("Error reading file for hashing {}: {}", entry_path.display(), e);
                        }
                    }
                }

                // Check for ancient files
                if let Some(threshold) = ancient_threshold {
                    if let Ok(modified_time) = metadata.modified() {
                        if modified_time < threshold {
                            ancient_files.push(entry_path.clone());
                            found_any_debris = true;
                        }
                    } else {
                        eprintln!("Warning: Could not get modification time for {}", entry_path.display());
                    }
                }
            }
        }
    }

    // Report findings
    if !empty_files.is_empty() {
        println!("\n--- Empty Files (Digital Voids) ---");
        for file in empty_files {
            println!("  {}", file.display());
        }
    }

    if args.duplicates {
        let mut has_actual_duplicates = false;
        for (hash, paths) in &duplicate_hashes {
            if paths.len() > 1 {
                if !has_actual_duplicates {
                    println!("\n--- Duplicate Fragments (Echoes in the Data Stream) ---");
                    has_actual_duplicates = true;
                    found_any_debris = true;
                }
                println!("  Hash: {}", hash);
                for path in paths {
                    println!("    {}", path.display());
                }
            }
        }
    }

    if !ancient_files.is_empty() {
        println!("\n--- Ancient Relics (Forgotten Data) ---");
        for file in ancient_files {
            println!("  {}", file.display());
        }
    }

    if !found_any_debris && (args.empty || args.duplicates || args.ancient.is_some()) {
        println!("\nNo significant digital debris found. Your data stream is clear!");
    } else if !found_any_debris && !(args.empty || args.duplicates || args.ancient.is_some()) {
        println!("\nNo checks were specified. Use --empty, --duplicates, or --ancient <DAYS>.");
    }

    Ok(())
}
