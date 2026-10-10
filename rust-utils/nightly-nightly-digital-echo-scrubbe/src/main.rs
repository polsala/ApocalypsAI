use clap::Parser;
use std::fs;
use std::path::{Path, PathBuf};
use std::time::SystemTime;
use walkdir::WalkDir;
use chrono::{Duration, Local, DateTime};

/// A high-performance CLI tool to identify and suggest removal of stale, unused files,
/// metaphorically scrubbing digital echoes from your filesystem.
#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// The directory to scan for digital echoes.
    path: PathBuf,

    /// Files older than this many days will be considered digital echoes.
    #[arg(short, long, default_value_t = 30)]
    age: i64, // Use i64 for chrono::Duration::days

    /// Perform a dry run. Only print what *would* be scrubbed, without deleting anything.
    #[arg(short, long)]
    dry_run: bool,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();

    let target_path = &args.path;
    let age_threshold_days = args.age;
    let dry_run = args.dry_run;

    if !target_path.exists() {
        eprintln!("Error: Path '{}' does not exist.", target_path.display());
        std::process::exit(1);
    }
    if !target_path.is_dir() {
        eprintln!("Error: Path '{}' is not a directory.", target_path.display());
        std::process::exit(1);
    }

    let now: DateTime<Local> = Local::now();
    let cutoff_datetime = now - Duration::days(age_threshold_days);
    let cutoff_system_time: SystemTime = cutoff_datetime.into();


    println!(
        "Scanning '{}' for digital echoes older than {} days (last modified before {}).",
        target_path.display(),
        age_threshold_days,
        cutoff_datetime.format("%Y-%m-%d %H:%M:%S")
    );

    if dry_run {
        println!("(Dry run mode: no files will be deleted.)");
    } else {
        println!("(Live mode: files will be deleted!)");
        println!("Proceeding in 5 seconds. Press Ctrl+C to cancel.");
        std::thread::sleep(std::time::Duration::from_secs(5));
    }

    let mut echoes_found = 0;
    let mut echoes_scrubbed = 0;

    for entry in WalkDir::new(target_path)
        .into_iter()
        .filter_map(|e| e.ok())
    {
        let path = entry.path();
        if path.is_file() {
            match fs::metadata(path) {
                Ok(metadata) => {
                    if let Ok(modified_time) = metadata.modified() {
                        if modified_time < cutoff_system_time {
                            echoes_found += 1;
                            let modified_datetime: DateTime<Local> = modified_time.into();
                            println!(
                                "Found echo: '{}' (Last modified: {})",
                                path.display(),
                                modified_datetime.format("%Y-%m-%d %H:%M:%S")
                            );

                            if !dry_run {
                                match fs::remove_file(path) {
                                    Ok(_) => {
                                        println!("  -> Scrubbed!");
                                        echoes_scrubbed += 1;
                                    }
                                    Err(e) => {
                                        eprintln!("  -> Failed to scrub '{}': {}", path.display(), e);
                                    }
                                }
                            }
                        }
                    } else {
                        eprintln!("Warning: Could not get modified time for '{}'", path.display());
                    }
                }
                Err(e) => {
                    eprintln!("Warning: Could not get metadata for '{}': {}", path.display(), e);
                }
            }
        }
    }

    println!("\n--- Scrubbing Complete ---");
    println!("Total digital echoes found: {}", echoes_found);
    if !dry_run {
        println!("Total digital echoes scrubbed: {}", echoes_scrubbed);
    } else {
        println!("(In dry run mode, {} echoes would have been scrubbed.)", echoes_found);
    }

    Ok(())
}
