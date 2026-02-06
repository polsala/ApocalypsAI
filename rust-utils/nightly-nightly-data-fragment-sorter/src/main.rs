use clap::Parser;
use walkdir::WalkDir;
use std::path::{Path, PathBuf};
use std::fs;
use std::collections::HashMap;
use sha2::{Sha256, Digest};
use hex;

#[derive(Parser, Debug)]
#[command(author, version, about = "Scans directories for data fragments, categorizes them, and identifies duplicates.", long_about = None)]
struct Args {
    /// The directory to scan for data fragments.
    #[arg(short, long, value_name = "PATH")]
    source_dir: PathBuf,

    /// The directory where categorized fragments will be moved/copied.
    #[arg(short, long, value_name = "PATH")]
    output_dir: PathBuf,

    /// Minimum file size (bytes) to be considered 'large'.
    #[arg(long, default_value_t = 1024 * 1024)] // 1MB
    min_large_size: u64,

    /// Number of days for a file to be considered 'recent'.
    #[arg(long, default_value_t = 7)]
    recent_days: u64,

    /// If true, files will be moved; otherwise, they will be copied.
    #[arg(short, long)]
    mv: bool,
}

#[derive(Debug, PartialEq)]
enum FragmentCategory {
    Large,
    Recent,
    Empty,
    Duplicate(String), // Stores hash of the original file
    Other,
    Error(String),
}

fn calculate_hash(path: &Path) -> Result<String, String> {
    let mut file = fs::File::open(path).map_err(|e| format!("Failed to open file: {}", e))?;
    let mut hasher = Sha256::new();
    std::io::copy(&mut file, &mut hasher).map_err(|e| format!("Failed to read file for hashing: {}", e))?;
    Ok(hex::encode(hasher.finalize()))
}

fn categorize_file(
    path: &Path,
    min_large_size: u64,
    recent_days: u64,
    file_hashes: &mut HashMap<String, PathBuf>,
) -> FragmentCategory {
    let metadata = match fs::metadata(path) {
        Ok(meta) => meta,
        Err(e) => return FragmentCategory::Error(format!("Failed to get metadata: {}", e)),
    };

    if metadata.is_dir() {
        return FragmentCategory::Other; // Skip directories
    }

    if metadata.len() == 0 {
        return FragmentCategory::Empty;
    }

    if metadata.len() >= min_large_size {
        return FragmentCategory::Large;
    }

    if let Ok(modified_time) = metadata.modified() {
        let now = std::time::SystemTime::now();
        if let Ok(duration) = now.duration_since(modified_time) {
            if duration.as_secs() < recent_days * 24 * 60 * 60 {
                return FragmentCategory::Recent;
            }
        }
    }

    // Check for duplicates
    match calculate_hash(path) {
        Ok(hash) => {
            if let Some(original_path) = file_hashes.get(&hash) {
                FragmentCategory::Duplicate(original_path.to_string_lossy().into_owned())
            } else {
                file_hashes.insert(hash, path.to_path_buf());
                FragmentCategory::Other
            }
        }
        Err(e) => FragmentCategory::Error(format!("Hashing error: {}", e)),
    }
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();

    if !args.source_dir.exists() {
        eprintln!("Error: Source directory does not exist: {:?}", args.source_dir);
        std::process::exit(1);
    }
    if !args.source_dir.is_dir() {
        eprintln!("Error: Source path is not a directory: {:?}", args.source_dir);
        std::process::exit(1);
    }

    fs::create_dir_all(&args.output_dir)?;

    let mut file_hashes: HashMap<String, PathBuf> = HashMap::new();
    let mut categorized_count = HashMap::new();

    println!("Scanning for data fragments in {:?}...", args.source_dir);

    for entry in WalkDir::new(&args.source_dir) {
        let entry = entry?;
        let path = entry.path();

        if path.is_file() {
            let category = categorize_file(
                path,
                args.min_large_size,
                args.recent_days,
                &mut file_hashes,
            );

            let category_str = match &category {
                FragmentCategory::Large => "large_files",
                FragmentCategory::Recent => "recent_files",
                FragmentCategory::Empty => "empty_files",
                FragmentCategory::Duplicate(_) => "duplicate_files",
                FragmentCategory::Other => "other_fragments",
                FragmentCategory::Error(_) => "error_fragments",
            };

            *categorized_count.entry(category_str.to_string()).or_insert(0) += 1;

            let target_dir = args.output_dir.join(category_str);
            fs::create_dir_all(&target_dir)?;

            let target_path = target_dir.join(path.file_name().ok_or("Invalid file name")?);

            match category {
                FragmentCategory::Duplicate(original_path_str) => {
                    println!("  [DUPLICATE] {:?} (original: {})", path, original_path_str);
                    // Duplicates are logged but not moved/copied to avoid redundant storage.
                    // If a copy/move is desired, a naming strategy for duplicates would be needed.
                }
                FragmentCategory::Error(e) => {
                    eprintln!("  [ERROR] {:?}: {}", path, e);
                    // Move/copy to error_fragments for manual inspection
                    if args.mv {
                        fs::rename(path, &target_path)?;
                    } else {
                        fs::copy(path, &target_path)?;
                    }
                }
                _ => {
                    println!("  [{}] {:?} -> {:?}", category_str, path, target_path);
                    if args.mv {
                        fs::rename(path, &target_path)?;
                    } else {
                        fs::copy(path, &target_path)?;
                    }
                }
            }
        }
    }

    println!("\n--- Scan Complete ---");
    println!("Categorized fragments:");
    for (category, count) in categorized_count {
        println!("  {}: {}", category, count);
    }

    Ok(())
}
