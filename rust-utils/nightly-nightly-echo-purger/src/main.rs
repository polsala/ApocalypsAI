use clap::Parser;
use walkdir::WalkDir;
use sha2::{Sha256, Digest};
use std::collections::HashMap;
use std::fs;
use std::io::{self, Read};
use std::path::{Path, PathBuf};

#[derive(Parser, Debug)]
#[command(author, version, about = "Purge data echoes from your digital wasteland!", long_about = None)]
struct Args {
    /// One or more paths to directories to scan for duplicate files.
    #[arg(required = true)]
    paths: Vec<PathBuf>,

    /// DANGER! Delete duplicate files, keeping only the first encountered instance. Use with caution.
    #[arg(short, long)]
    delete: bool,

    /// Enable verbose output, showing more details during scanning.
    #[arg(short, long)]
    verbose: bool,
}

fn calculate_file_hash(path: &Path) -> io::Result<String> {
    let mut file = fs::File::open(path)?;
    let mut hasher = Sha256::new();
    let mut buffer = [0; 4096]; // Read in 4KB chunks

    loop {
        let bytes_read = file.read(&mut buffer)?;
        if bytes_read == 0 {
            break;
        }
        hasher.update(&buffer[..bytes_read]);
    }

    Ok(hex::encode(hasher.finalize()))
}

fn main() -> io::Result<()> {
    let args = Args::parse();

    if args.verbose {
        println!("Scanning for data echoes in: {:?}", args.paths);
        if args.delete {
            println!("WARNING: Purge mode activated! Duplicate files will be deleted.");
        } else {
            println!("Dry run mode: No files will be deleted.");
        }
    }

    let mut file_hashes: HashMap<String, Vec<PathBuf>> = HashMap::new();
    let mut total_files_scanned = 0;
    let mut total_bytes_scanned = 0;

    for path_arg in &args.paths {
        if !path_arg.is_dir() {
            eprintln!("Error: Path '{}' is not a directory. Skipping.", path_arg.display());
            continue;
        }

        for entry in WalkDir::new(path_arg)
            .into_iter()
            .filter_map(|e| e.ok())
        {
            let path = entry.path();
            if path.is_file() {
                total_files_scanned += 1;
                if args.verbose {
                    println!("  Scanning file: {}", path.display());
                }

                match calculate_file_hash(path) {
                    Ok(hash) => {
                        if let Ok(metadata) = fs::metadata(path) {
                            total_bytes_scanned += metadata.len();
                        }
                        file_hashes.entry(hash).or_default().push(path.to_path_buf());
                    }
                    Err(e) => {
                        eprintln!("Error hashing file {}: {}", path.display(), e);
                    }
                }
            }
        }
    }

    println!("\n--- Echo Purge Report ---");
    println!("Scanned {} files, {} bytes.", total_files_scanned, total_bytes_scanned);

    let mut duplicates_found = 0;
    let mut bytes_to_recover = 0;

    for (hash, paths) in file_hashes {
        if paths.len() > 1 {
            duplicates_found += 1;
            println!("\nFound {} data echoes for hash {}:", paths.len() - 1, hash);
            println!("  Original (kept): {}", paths[0].display());

            for i in 1..paths.len() {
                let duplicate_path = &paths[i];
                if let Ok(metadata) = fs::metadata(duplicate_path) {
                    bytes_to_recover += metadata.len();
                }
                println!("  Duplicate: {}", duplicate_path.display());

                if args.delete {
                    match fs::remove_file(duplicate_path) {
                        Ok(_) => println!("    PURGED: {}", duplicate_path.display()),
                        Err(e) => eprintln!("    ERROR purging {}: {}", duplicate_path.display(), e),
                    }
                }
            }
        }
    }

    if duplicates_found == 0 {
        println!("\nNo data echoes detected. Your digital wasteland is pristine!");
    } else {
        println!("\n--- Purge Summary ---");
        println!("Detected {} groups of data echoes.", duplicates_found);
        println!("Potential bytes to recover: {} bytes.", bytes_to_recover);
        if !args.delete {
            println!("Run with --delete to purge these echoes (use with caution!).");
        } else {
            println!("Echoes purged! Your digital realm is a bit lighter.");
        }
    }

    Ok(())
}
