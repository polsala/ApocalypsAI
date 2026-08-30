use clap::Parser;
use walkdir::WalkDir;
use sha2::{Sha256, Digest};
use std::collections::{HashMap, HashSet};
use std::path::{Path, PathBuf};
use std::fs;
use std::io::{self, Read};

#[derive(Parser, Debug)]
#[clap(author, version, about = "A high-performance CLI tool to catalog unique files ('relics') in a directory, identifying duplicates ('common junk') and reporting on file types.", long_about = None)]
struct Args {
    /// The path to the directory to scan for relics.
    #[clap(name = "DIRECTORY")]
    directory: PathBuf,
}

/// Calculates the SHA256 hash of a file.
fn calculate_hash(path: &Path) -> Result<String, io::Error> {
    let mut file = fs::File::open(path)?;
    let mut hasher = Sha256::new();
    let mut buffer = [0; 1024];

    loop {
        let bytes_read = file.read(&mut buffer)?;
        if bytes_read == 0 {
            break;
        }
        hasher.update(&buffer[..bytes_read]);
    }

    Ok(format!("{:x}", hasher.finalize()))
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();

    if !args.directory.is_dir() {
        eprintln!("Error: Provided path is not a directory: {}", args.directory.display());
        std::process::exit(1);
    }

    println!("Scanning for relics in: {}\n", args.directory.display());

    let mut hash_to_paths: HashMap<String, Vec<PathBuf>> = HashMap::new();
    let mut file_type_counts: HashMap<String, usize> = HashMap::new();
    let mut total_files_scanned = 0;

    for entry in WalkDir::new(&args.directory)
        .into_iter()
        .filter_map(|e| e.ok()) {
        
        if entry.file_type().is_file() {
            total_files_scanned += 1;
            let path = entry.path().to_path_buf();

            // Calculate hash
            match calculate_hash(&path) {
                Ok(hash) => {
                    hash_to_paths.entry(hash).or_default().push(path.clone());
                },
                Err(e) => {
                    eprintln!("Warning: Could not hash file {}: {}", path.display(), e);
                }
            }

            // Count file types
            let extension = path.extension()
                .and_then(|os_str| os_str.to_str())
                .map_or("(No Extension)".to_string(), |s| format!(".{}", s));
            *file_type_counts.entry(extension).or_insert(0) += 1;
        }
    }

    let mut unique_relics: Vec<(String, PathBuf)> = Vec::new();
    let mut common_junk_groups: HashMap<String, Vec<PathBuf>> = HashMap::new();

    for (hash, paths) in hash_to_paths {
        if paths.len() == 1 {
            unique_relics.push((hash, paths[0].clone()));
        } else {
            common_junk_groups.insert(hash, paths);
        }
    }

    println!("--- Rummaging Report ---");
    println!("\nTotal files scanned: {}", total_files_scanned);
    println!("Total unique relics found: {}", unique_relics.len());
    println!("Total common junk (duplicates): {}", total_files_scanned - unique_relics.len());

    if !unique_relics.is_empty() {
        println!("\n--- Precious Artifacts (Unique Relics) ---");
        for (hash, path) in unique_relics {
            println!("[SHA256: {}] {}", &hash[..8], path.display());
        }
    }

    if !common_junk_groups.is_empty() {
        println!("\n--- Common Junk (Duplicate Groups) ---");
        for (hash, paths) in common_junk_groups {
            println!("Hash: {}...", &hash[..8]);
            for path in paths {
                println!("  - {}", path.display());
            }
            println!();
        }
    }

    if !file_type_counts.is_empty() {
        println!("\n--- File Type Manifest ---");
        let mut sorted_types: Vec<(&String, &usize)> = file_type_counts.iter().collect();
        sorted_types.sort_by(|a, b| b.1.cmp(a.1)); // Sort by count, descending
        for (ext, count) in sorted_types {
            println!("{}: {} files", ext, count);
        }
    }

    println!("\n--- End of Rummaging ---");
    println!("May your unique finds be plentiful!");

    Ok(())
}
