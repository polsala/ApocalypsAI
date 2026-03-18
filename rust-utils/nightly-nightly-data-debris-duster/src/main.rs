use clap::Parser;
use std::collections::HashMap;
use std::fs;
use std::path::{Path, PathBuf};
use sha2::{Sha256, Digest};
use walkdir::WalkDir;

#[derive(Parser, Debug)]
#[clap(author, version, about = "Nightly Data Debris Duster: Find and report duplicate files.", long_about = None)]
struct Args {
    /// The root directory to scan for duplicate files.
    #[clap(short, long, value_parser)]
    path: PathBuf,
}

/// Calculates the SHA256 hash of a file.
fn calculate_hash(path: &Path) -> Result<String, std::io::Error> {
    let mut file = fs::File::open(path)?;
    let mut hasher = Sha256::new();
    std::io::copy(&mut file, &mut hasher)?;
    Ok(format!("{:x}", hasher.finalize()))
}

/// Finds duplicate files in the given root directory.
/// Returns a HashMap where keys are file hashes and values are vectors of paths to files with that hash.
fn find_duplicates(root_path: &Path) -> HashMap<String, Vec<PathBuf>> {
    let mut file_hashes: HashMap<String, Vec<PathBuf>> = HashMap::new();

    for entry in WalkDir::new(root_path).into_iter().filter_map(|e| e.ok()) {
        let path = entry.path();
        if path.is_file() {
            match calculate_hash(path) {
                Ok(hash) => {
                    file_hashes.entry(hash).or_default().push(path.to_path_buf());
                }
                Err(e) => {
                    eprintln!("Warning: Could not hash file {:?}: {}", path, e);
                }
            }
        }
    }
    file_hashes
}

fn main() {
    let args = Args::parse();

    if !args.path.exists() {
        eprintln!("Error: Path does not exist: {:?}", args.path);
        std::process::exit(1);
    }
    if !args.path.is_dir() {
        eprintln!("Error: Path is not a directory: {:?}", args.path);
        std::process::exit(1);
    }

    println!("Scanning for digital debris in {:?}...", args.path);
    let duplicates = find_duplicates(&args.path);

    let mut found_duplicates = false;
    for (hash, paths) in duplicates {
        if paths.len() > 1 {
            found_duplicates = true;
            println!("\n--- Duplicate Debris (Hash: {}) ---", hash);
            for path in paths {
                println!("  - {}", path.display());
            }
        }
    }

    if !found_duplicates {
        println!("\nNo significant digital debris (duplicates) found. Your data is sparkling clean!");
    } else {
        println!("\nDigital debris report complete. Time to clear the clutter!");
    }
}
