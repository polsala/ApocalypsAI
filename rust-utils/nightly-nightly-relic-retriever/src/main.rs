use clap::Parser;
use std::collections::HashMap;
use std::fs;
use std::io::{self, Read};
use std::path::{Path, PathBuf};
use walkdir::WalkDir;
use sha2::{Sha256, Digest};
use chrono::Local;

#[derive(Parser, Debug)]
#[command(author, version, about = "Nightly Relic Retriever: Unearthing Temporal Echoes from the Wasteland", long_about = None)]
struct Args {
    /// The directory to scan for relics (duplicate files).
    #[arg(name = "PATH")]
    path: PathBuf,

    /// The directory where temporal echoes will be moved. Defaults to .void_vault within the scanned path.
    #[arg(short = 'a', long, value_name = "ARCHIVE_PATH")]
    archive_path: Option<PathBuf>,

    /// Perform a dry run. No files will be moved, but the tool will report what it *would* do.
    #[arg(short = 'd', long)]
    dry_run: bool,

    /// Enable verbose output.
    #[arg(short = 'v', long)]
    verbose: bool,
}

fn calculate_hash(path: &Path) -> io::Result<String> {
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
    Ok(hex::encode(hasher.finalize()))
}

fn main() -> io::Result<()> {
    let args = Args::parse();

    let scan_path = args.path.canonicalize()?;
    let archive_path = args.archive_path.unwrap_or_else(|| scan_path.join(".void_vault"));

    if args.verbose {
        println!("\nInitiating Relic Retrieval Protocol...");
        println!("Scanning path: {}", scan_path.display());
        println!("Void Vault: {}", archive_path.display());
        if args.dry_run {
            println!("DRY RUN ENABLED: No files will be moved.");
        }
    }

    let mut file_hashes: HashMap<String, Vec<PathBuf>> = HashMap::new();

    for entry in WalkDir::new(&scan_path)
        .into_iter()
        .filter_map(|e| e.ok())
    {
        let path = entry.path();
        if path.is_file() {
            // Skip files within the archive path itself to prevent self-archiving
            if path.starts_with(&archive_path) {
                if args.verbose {
                    println!("Skipping archived relic: {}", path.display());
                }
                continue;
            }

            if args.verbose {
                println!("Analyzing relic: {}", path.display());
            }
            match calculate_hash(path) {
                Ok(hash) => {
                    file_hashes.entry(hash).or_default().push(path.to_path_buf());
                }
                Err(e) => {
                    eprintln!("Warning: Could not hash relic {}: {}", path.display(), e);
                }
            }
        }
    }

    let mut echoes_found = 0;
    let mut echoes_archived = 0;

    for (hash, paths) in file_hashes {
        if paths.len() > 1 {
            echoes_found += paths.len() - 1;
            if args.verbose {
                println!("\nTemporal Echoes Detected for hash {}:", hash);
                for p in &paths {
                    println!("  - {}", p.display());
                }
            }

            let primary_relic = &paths[0]; // Keep the first encountered as the primary relic
            if args.verbose {
                println!("  Keeping primary relic: {}", primary_relic.display());
            }

            for i in 1..paths.len() {
                let echo_path = &paths[i];
                let original_filename = echo_path.file_name().unwrap_or_default().to_string_lossy();
                let timestamp = Local::now().format("%Y%m%d%H%M%S").to_string();
                let new_filename = format!("{}_{}_{}", original_filename, hash.chars().take(8).collect::<String>(), timestamp);
                let destination_path = archive_path.join(&new_filename);

                if args.dry_run {
                    println!("  [DRY RUN] Would move echo {} to {}", echo_path.display(), destination_path.display());
                } else {
                    if !archive_path.exists() {
                        fs::create_dir_all(&archive_path)?;
                        if args.verbose {
                            println!("Created Void Vault at {}", archive_path.display());
                        }
                    }
                    match fs::rename(echo_path, &destination_path) {
                        Ok(_) => {
                            echoes_archived += 1;
                            println!("  Archived temporal echo: {} -> {}", echo_path.display(), destination_path.display());
                        }
                        Err(e) => {
                            eprintln!("Error archiving echo {}: {}", echo_path.display(), e);
                        }
                    }
                }
            }
        }
    }

    println!("\nRelic Retrieval Protocol Complete.");
    if echoes_found > 0 {
        println!("Identified {} temporal echoes.", echoes_found);
        if !args.dry_run {
            println!("Successfully archived {} echoes to the Void Vault.", echoes_archived);
        } else {
            println!("Dry run complete. {} echoes would have been archived.", echoes_found);
        }
    } else {
        println!("No temporal echoes detected. Your data is pristine... for now.");
    }

    Ok(())
}
