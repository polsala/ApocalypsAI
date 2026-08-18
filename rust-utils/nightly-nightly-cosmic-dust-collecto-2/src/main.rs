use clap::Parser;
use walkdir::WalkDir;
use chrono::{Utc, Duration, DateTime};
use std::fs;
use std::path::{Path, PathBuf};
use std::error::Error;

#[derive(Parser, Debug)]
#[command(author, version, about = "Collects 'cosmic dust' (small, old files) from your file system.", long_about = None)]
struct Args {
    /// The root directory to start scanning from.
    #[arg(short, long)]
    path: PathBuf,

    /// Maximum file size in kilobytes (KB). Files larger than this will be ignored.
    #[arg(short = 's', long, default_value_t = 100)]
    max_size: u64,

    /// Minimum age in days. Files modified more recently than this will be ignored.
    #[arg(short = 'a', long, default_value_t = 30)]
    min_age: i64,

    /// Directory to move identified 'cosmic dust' files to. If not specified, files will only be listed.
    #[arg(short = 'o', long)]
    archive_to: Option<PathBuf>,

    /// Perform a dry run. Files will be identified and listed, but no changes will be made.
    #[arg(short, long)]
    dry_run: bool,
}

fn main() -> Result<(), Box<dyn Error>> {
    let args = Args::parse();

    let now = Utc::now();
    let min_age_duration = Duration::days(args.min_age);
    let max_size_bytes = args.max_size * 1024; // Convert KB to bytes

    println!("Scanning '{}' for cosmic dust...", args.path.display());
    println!("  Max size: {} KB", args.max_size);
    println!("  Min age: {} days old", args.min_age);
    if args.dry_run {
        println!("  Mode: Dry Run (no changes will be made)");
    } else if let Some(archive_dir) = &args.archive_to {
        println!("  Mode: Archiving to '{}'", archive_dir.display());
        fs::create_dir_all(archive_dir)?;
    } else {
        println!("  Mode: Listing only (no changes will be made)");
    }
    println!("--------------------------------------------------");

    let mut dust_files = Vec::new();

    for entry in WalkDir::new(&args.path).into_iter().filter_map(|e| e.ok()) {
        if entry.file_type().is_file() {
            let metadata = entry.metadata()?;
            let file_size = metadata.len();

            // Check size
            if file_size > max_size_bytes {
                continue;
            }

            // Check age
            let modified_time: DateTime<Utc> = metadata.modified()?.into();
            if now.signed_duration_since(modified_time) < min_age_duration {
                continue;
            }

            dust_files.push(entry.path().to_path_buf());
        }
    }

    if dust_files.is_empty() {
        println!("No cosmic dust found. Your digital cosmos is pristine!");
    } else {
        println!("Found {} cosmic dust files:", dust_files.len());
        for file_path in &dust_files {
            println!("- {}", file_path.display());
        }

        if !args.dry_run {
            if let Some(archive_dir) = &args.archive_to {
                println!("\nArchiving cosmic dust...");
                for file_path in dust_files {
                    let file_name = file_path.file_name().ok_or("Could not get file name")?;
                    let dest_path = archive_dir.join(file_name);
                    match fs::rename(&file_path, &dest_path) {
                        Ok(_) => println!("  Moved '{}' to '{}'", file_path.display(), dest_path.display()),
                        Err(e) => eprintln!("  Error moving '{}': {}", file_path.display(), e),
                    }
                }
                println!("Archiving complete.");
            } else {
                println!("\nTo archive these files, specify an --archive-to directory (and remove --dry-run if present).");
            }
        }
    }

    Ok(())
}
