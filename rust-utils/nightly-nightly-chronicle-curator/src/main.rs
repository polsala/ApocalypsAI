use clap::Parser;
use chrono::{DateTime, Local, Utc};
use walkdir::WalkDir;
use std::fs;
use std::path::{Path, PathBuf};

#[derive(Parser, Debug)]
#[command(author, version, about = "Curate your digital history by organizing files into chronological directories.", long_about = None)]
struct Args {
    /// The source directory to scan for files.
    #[arg(short, long, default_value = ".")]
    source: PathBuf,

    /// The destination directory where organized files will be placed.
    #[arg(short, long, default_value = "./chronicle")]
    destination: PathBuf,

    /// Use modification time instead of creation time for organizing files.
    #[arg(short, long)]
    modified: bool,

    /// Only show what would be done, without actually moving files.
    #[arg(short, long)]
    dry_run: bool,

    /// Include hidden files and directories.
    #[arg(short, long)]
    all: bool,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();

    if !args.source.exists() {
        eprintln!("Error: Source directory '{}' does not exist.", args.source.display());
        std::process::exit(1);
    }

    if !args.destination.exists() {
        if args.dry_run {
            println!("Dry Run: Would create destination directory: {}", args.destination.display());
        } else {
            println!("Creating destination directory: {}", args.destination.display());
            fs::create_dir_all(&args.destination)?;
        }
    } else if !args.destination.is_dir() {
        eprintln!("Error: Destination path '{}' exists but is not a directory.", args.destination.display());
        std::process::exit(1);
    }

    println!("Nightly Chronicle Curator is sifting through the sands of time...");

    let mut processed_count = 0;
    let mut skipped_count = 0;
    let mut error_count = 0;

    for entry in WalkDir::new(&args.source)
        .into_iter()
        .filter_entry(|e| {
            if args.all {
                true
            } else {
                !e.file_name().to_string_lossy().starts_with('.')
            }
        })
        .filter_map(|e| e.ok())
    {
        let path = entry.path();
        if path.is_file() {
            let metadata = match fs::metadata(path) {
                Ok(m) => m,
                Err(e) => {
                    eprintln!("Warning: Could not get metadata for {}: {}", path.display(), e);
                    error_count += 1;
                    continue;
                }
            };

            let timestamp = if args.modified {
                metadata.modified()? 
            } else {
                metadata.created().unwrap_or_else(|_| {
                    // Fallback to modified time if creation time is not available (e.g., some Linux filesystems)
                    eprintln!("Warning: Creation time not available for {}. Using modification time.", path.display());
                    metadata.modified().unwrap_or_else(|_| {
                        // Fallback to current time if neither is available
                        eprintln!("Warning: Neither creation nor modification time available for {}. Using current time.", path.display());
                        std::time::SystemTime::now()
                    })
                })
            };

            let datetime: DateTime<Local> = timestamp.into();
            let year = datetime.format("%Y").to_string();
            let month = datetime.format("%m").to_string();
            let day = datetime.format("%d").to_string();

            let target_dir = args.destination.join(&year).join(&month).join(&day);
            let target_path = target_dir.join(path.file_name().unwrap());

            if args.dry_run {
                println!("Dry Run: Would move '{}' to '{}'", path.display(), target_path.display());
                processed_count += 1;
            } else {
                if !target_dir.exists() {
                    fs::create_dir_all(&target_dir)?;
                }

                match fs::rename(path, &target_path) {
                    Ok(_) => {
                        println!("Curated: '{}' -> '{}'", path.display(), target_path.display());
                        processed_count += 1;
                    }
                    Err(e) => {
                        eprintln!("Error moving '{}' to '{}': {}", path.display(), target_path.display(), e);
                        error_count += 1;
                    }
                }
            }
        } else if path.is_dir() && path != args.source {
            // Optionally handle empty directories or directories that become empty
            // For now, we just skip directories themselves, focusing on files.
            skipped_count += 1;
        }
    }

    println!("\nChronicle curation complete!");
    println!("  Files processed: {}", processed_count);
    println!("  Directories/files skipped: {}", skipped_count);
    println!("  Errors encountered: {}", error_count);

    Ok(())
}
