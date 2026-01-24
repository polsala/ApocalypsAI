use clap::Parser;
use walkdir::WalkDir;
use chrono::{Utc, Duration, DateTime};
use std::path::{Path, PathBuf};
use std::fs;
use std::io;

#[derive(Parser, Debug)]
#[clap(author, version, about = "A high-performance Rust CLI tool to identify and scrub (archive or delete) old, unused files and directories based on age and patterns, preventing temporal clutter.", long_about = None)]
struct Args {
    /// Path to the directory to scan
    #[clap(short, long, default_value = ".")]
    path: PathBuf,

    /// Age in days. Files/directories older than this will be considered for scrubbing.
    #[clap(short, long, default_value_t = 30)]
    age: u64,

    /// Comma-separated list of patterns to match (e.g., "target/,*.log,node_modules/").
    /// Patterns ending with '/' match directories. Wildcards ('*') are supported at the beginning of file patterns.
    #[clap(short, long, use_value_delimiter = true, value_delimiter = ',')]
    patterns: Vec<String>,

    /// Perform a dry run without making any changes.
    #[clap(short, long)]
    dry_run: bool,

    /// Archive matched items to a .temporal_void directory within the scan path.
    #[clap(short, long, conflicts_with = "delete")]
    archive: bool,

    /// Delete matched items permanently.
    #[clap(short, long, conflicts_with = "archive")]
    delete: bool,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();

    if !args.dry_run && !args.archive && !args.delete {
        eprintln!("Error: No action specified. Use --dry-run, --archive, or --delete.");
        std::process::exit(1);
    }

    let now: DateTime<Utc> = Utc::now();
    let age_threshold = now - Duration::days(args.age as i64);

    println!("Scanning '{}' for temporal echoes older than {} days...", args.path.display(), args.age);
    println!("Matching patterns: {:?}", args.patterns);

    let mut scrubbed_count = 0;
    let mut skipped_count = 0;

    let archive_base_path = args.path.join(".temporal_void");
    if args.archive && !archive_base_path.exists() {
        fs::create_dir_all(&archive_base_path)?;
        println!("Created archive directory: {}", archive_base_path.display());
    }

    for entry in WalkDir::new(&args.path).into_iter().filter_map(|e| e.ok()) {
        let path = entry.path();
        let metadata = match entry.metadata() {
            Ok(m) => m,
            Err(_) => {
                eprintln!("Warning: Could not get metadata for {}", path.display());
                continue;
            }
        };

        // Skip the archive directory itself if it's within the scan path
        if args.archive && path.starts_with(&archive_base_path) {
            continue;
        }

        let modified_time: DateTime<Utc> = metadata.modified()?.into();

        let is_old = modified_time < age_threshold;
        let matches_pattern = args.patterns.is_empty() || args.patterns.iter().any(|p| {
            if p.ends_with('/') { // Directory pattern (e.g., "target/")
                path.is_dir() && path.file_name().map_or(false, |name| name == p.trim_end_matches('/'))
            } else { // File pattern or general name pattern (e.g., "*.log", "foo.txt")
                path.file_name().map_or(false, |name| {
                    let name_str = name.to_string_lossy();
                    if p.starts_with('*') && p.len() > 1 { // Wildcard prefix, e.g., *.log
                        name_str.ends_with(&p[1..])
                    } else { // Exact match or no wildcard
                        name_str == p
                    }
                })
            }
        });

        if is_old && matches_pattern {
            if args.dry_run {
                println!("[DRY RUN] Would scrub: {}", path.display());
            } else if args.archive {
                let relative_path = path.strip_prefix(&args.path)?;
                let dest_path = archive_base_path.join(relative_path);
                if path.is_dir() {
                    fs::create_dir_all(&dest_path)?;
                } else {
                    if let Some(parent) = dest_path.parent() {
                        fs::create_dir_all(parent)?;
                    }
                }
                match fs::rename(path, &dest_path) {
                    Ok(_) => println!("[ARCHIVED] {} -> {}", path.display(), dest_path.display()),
                    Err(e) => eprintln!("Error archiving {}: {}", path.display(), e),
                }
            } else if args.delete {
                if path.is_dir() {
                    match fs::remove_dir_all(path) {
                        Ok(_) => println!("[DELETED] {}", path.display()),
                        Err(e) => eprintln!("Error deleting directory {}: {}", path.display(), e),
                    }
                } else {
                    match fs::remove_file(path) {
                        Ok(_) => println!("[DELETED] {}", path.display()),
                        Err(e) => eprintln!("Error deleting file {}: {}", path.display(), e),
                    }
                }
            }
            scrubbed_count += 1;
        } else {
            skipped_count += 1;
        }
    }

    println!("\nScrubbing complete. {} temporal echoes scrubbed, {} items skipped.", scrubbed_count, skipped_count);

    Ok(())
}
