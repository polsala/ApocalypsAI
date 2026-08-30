use clap::Parser;
use std::collections::{HashMap, HashSet};
use std::fs;
use std::path::{Path, PathBuf};
use sha2::{Sha256, Digest};
use walkdir::WalkDir;

#[derive(Parser, Debug)]
#[clap(author, version, about = "Detects 'reality ripples' by comparing file contents across multiple directories.", long_about = None)]
struct Args {
    /// List of directories to compare
    #[clap(min_values = 2)]
    directories: Vec<PathBuf>,
}

fn calculate_file_hash(path: &Path) -> Result<String, std::io::Error> {
    let mut file = fs::File::open(path)?;
    let mut hasher = Sha256::new();
    std::io::copy(&mut file, &mut hasher)?;
    Ok(format!("{:x}", hasher.finalize()))
}

// Core logic function for testing and main execution
pub fn find_ripples(
    base_dirs: &[PathBuf],
) -> Result<HashMap<PathBuf, HashMap<PathBuf, String>>, Box<dyn std::error::Error>> {
    let mut all_file_data: HashMap<PathBuf, HashMap<PathBuf, String>> = HashMap::new(); // relative_path -> { canonical_base_dir -> hash }

    for base_dir in base_dirs {
        if !base_dir.is_dir() {
            return Err(format!("Error: Directory not found: {}", base_dir.display()).into());
        }
        let canonical_base_dir = base_dir.canonicalize()?;

        for entry in WalkDir::new(&base_dir) {
            let entry = entry?;
            let path = entry.path();

            if path.is_file() {
                let relative_path = path.strip_prefix(&base_dir)?.to_path_buf();
                let hash = calculate_file_hash(path)?;

                all_file_data
                    .entry(relative_path)
                    .or_default()
                    .insert(canonical_base_dir.clone(), hash);
            }
        }
    }
    Ok(all_file_data)
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();
    let base_dirs = args.directories;

    if base_dirs.len() < 2 {
        eprintln!("Error: Please provide at least two directories to compare.");
        std::process::exit(1);
    }

    let all_file_data = find_ripples(&base_dirs)?;

    let mut found_ripples = false;

    // Get canonical paths for all input base directories once for consistent comparison
    let canonical_input_base_dirs: Vec<PathBuf> = base_dirs.iter()
        .map(|p| p.canonicalize().map_err(|e| e.into()))
        .collect::<Result<_, Box<dyn std::error::Error>>>()?;

    for (relative_path, dir_hashes) in all_file_data {
        let mut unique_hashes: HashSet<&String> = HashSet::new();
        for hash in dir_hashes.values() {
            unique_hashes.insert(hash);
        }

        let mut present_in_canonical_dirs: HashSet<PathBuf> = HashSet::new();
        for dir_path in dir_hashes.keys() {
            present_in_canonical_dirs.insert(dir_path.clone());
        }

        // Check for missing files in some directories
        let mut missing_in_some = false;
        let mut missing_dirs_display = Vec::new();
        for input_base_dir in &canonical_input_base_dirs {
            if !present_in_canonical_dirs.contains(input_base_dir) {
                missing_in_some = true;
                // Find the original path from args for display
                if let Some(original_path) = base_dirs.iter().find(|p| p.canonicalize().unwrap_or_default() == *input_base_dir) {
                    missing_dirs_display.push(original_path.display().to_string());
                } else {
                    missing_dirs_display.push(input_base_dir.display().to_string());
                }
            }
        }

        if missing_in_some {
            found_ripples = true;
            println!(
                "🌀 RIPPLE DETECTED: File '{}' is missing in: {}",
                relative_path.display(),
                missing_dirs_display.join(", ")
            );
        }

        // Check for content discrepancies
        if unique_hashes.len() > 1 {
            found_ripples = true;
            println!(
                "💥 RIPPLE DETECTED: File '{}' has different content across directories:",
                relative_path.display()
            );
            // Sort for consistent output
            let mut sorted_dir_hashes: Vec<(&PathBuf, &String)> = dir_hashes.iter().collect();
            sorted_dir_hashes.sort_by_key(|(dir_path, _)| *dir_path);

            for (canonical_dir, hash) in sorted_dir_hashes {
                // Find the original path from args for display
                if let Some(original_path) = base_dirs.iter().find(|p| p.canonicalize().unwrap_or_default() == *canonical_dir) {
                    println!("  - {}: {}", original_path.display(), hash);
                } else {
                    println!("  - {}: {}", canonical_dir.display(), hash);
                }
            }
        }
    }

    if !found_ripples {
        println!("✨ All realities are in harmony! No ripples detected.");
    }

    Ok(())
}
