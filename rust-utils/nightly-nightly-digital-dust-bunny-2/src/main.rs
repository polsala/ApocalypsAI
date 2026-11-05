use clap::Parser;
use std::{
    collections::HashMap,
    fs,
    path::{Path, PathBuf},
    time::{Duration, SystemTime},
};
use walkdir::WalkDir;
use sha2::{Digest, Sha256};

#[derive(Parser, Debug)]
#[clap(author, version, about = "Identify and report on old or duplicate files.", long_about = None)]
pub struct Args {
    /// Path to scan
    #[clap(value_parser)]
    pub path: PathBuf,

    /// Report files not accessed or modified in the last N days. Use 0 to report all files as 'old'.
    #[clap(short, long, value_parser, default_value_t = 0)]
    pub age: u64,

    /// Report duplicate files based on content hash
    #[clap(short, long)]
    pub duplicates: bool,
}

pub fn run_app(args: Args) -> Result<(), Box<dyn std::error::Error>> {
    if !args.path.exists() {
        eprintln!("Error: Path '{}' does not exist.", args.path.display());
        return Err(format!("Path '{}' does not exist.", args.path.display()).into());
    }

    let mut file_hashes: HashMap<Vec<u8>, Vec<PathBuf>> = HashMap::new();
    let now = SystemTime::now();
    let age_threshold = if args.age > 0 {
        Some(now - Duration::from_days(args.age))
    } else {
        None
    };

    println!("Scanning '{}' for digital dust bunnies...", args.path.display());
    println!("--------------------------------------------------");

    for entry in WalkDir::new(&args.path).into_iter().filter_map(|e| e.ok()) {
        if entry.file_type().is_file() {
            let path = entry.path().to_path_buf();
            let metadata = fs::metadata(&path)?;

            // Check for age
            if args.age == 0 { // Special case: if age is 0, report all files as 'old'
                let modified_time = metadata.modified().unwrap_or(SystemTime::UNIX_EPOCH);
                let accessed_time = metadata.accessed().unwrap_or(SystemTime::UNIX_EPOCH);
                println!(
                    "[OLD]   {} (Modified: {:?}, Accessed: {:?})",
                    path.display(),
                    modified_time,
                    accessed_time
                );
            } else if let Some(threshold) = age_threshold {
                let modified_time = metadata.modified().unwrap_or(SystemTime::UNIX_EPOCH);
                let accessed_time = metadata.accessed().unwrap_or(SystemTime::UNIX_EPOCH);

                if modified_time < threshold || accessed_time < threshold {
                    println!(
                        "[OLD]   {} (Modified: {:?}, Accessed: {:?})",
                        path.display(),
                        modified_time,
                        accessed_time
                    );
                }
            }

            // Check for duplicates
            if args.duplicates {
                let mut file = fs::File::open(&path)?;
                let mut hasher = Sha256::new();
                std::io::copy(&mut file, &mut hasher)?;
                let hash = hasher.finalize().to_vec();

                file_hashes.entry(hash).or_default().push(path);
            }
        }
    }

    if args.duplicates {
        println!("\n--------------------------------------------------");
        println!("Duplicate Files Found:");
        let mut found_duplicates = false;
        for (hash, paths) in file_hashes {
            if paths.len() > 1 {
                found_duplicates = true;
                println!("  Hash: {}", hex::encode(hash));
                for p in paths {
                    println!("    - {}", p.display());
                }
            }
        }
        if !found_duplicates {
            println!("  No duplicate files found.");
        }
    }

    println!("\nScan complete. Remember, no files were modified.");
    Ok(())
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();
    run_app(args)
}
