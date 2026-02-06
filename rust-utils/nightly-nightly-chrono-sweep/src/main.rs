use clap::Parser;
use walkdir::WalkDir;
use chrono::{Utc, Duration, DateTime};
use std::fs;
use std::path::PathBuf;
use std::io::{self, Write};

#[derive(Parser, Debug)]
#[command(author, version, about = "A high-performance Rust CLI tool to identify and optionally remove files older than a specified temporal epoch.", long_about = None)]
struct Args {
    /// The directory to sweep for temporal debris.
    #[arg(short, long, default_value = ".")]
    path: PathBuf,

    /// The temporal epoch (duration) after which files are considered debris.
    /// Examples: "30d" (30 days), "2w" (2 weeks), "1m" (1 month), "1y" (1 year).
    #[arg(short, long)]
    duration: String,

    /// Perform a dry run: list files that would be affected without deleting them.
    #[arg(short, long, default_value_t = true)]
    dry_run: bool,

    /// Actually delete the identified temporal debris. Use with caution!
    #[arg(short, long, default_value_t = false)]
    delete: bool,

    /// Skip confirmation prompt when deleting. Use with extreme caution!
    #[arg(long, default_value_t = false)]
    force: bool,
}

fn parse_duration_string(s: &str) -> Option<Duration> {
    let s = s.trim();
    if s.is_empty() { return None; }
    let (num_str, unit_char) = s.split_at(s.len() - 1);
    let num: i64 = num_str.parse().ok()?;

    match unit_char {
        "d" => Some(Duration::days(num)),
        "w" => Some(Duration::weeks(num)),
        "m" => Some(Duration::days(num * 30)), // Approximation for months
        "y" => Some(Duration::days(num * 365)), // Approximation for years
        _ => None,
    }
}

/// Core logic for identifying and optionally deleting old files.
/// Returns a vector of paths that were actually deleted.
fn chrono_sweep_core(
    path: &PathBuf,
    cutoff_time: DateTime<Utc>,
    dry_run: bool,
    delete: bool,
    force: bool,
) -> Result<Vec<PathBuf>, Box<dyn std::error::Error>> {
    let mut identified_files = Vec::new();

    for entry in WalkDir::new(path).into_iter().filter_map(|e| e.ok()) {
        if entry.file_type().is_file() {
            let metadata = match entry.metadata() {
                Ok(m) => m,
                Err(_) => {
                    eprintln!("Warning: Could not get metadata for {}", entry.path().display());
                    continue;
                }
            };

            let modified_time: DateTime<Utc> = match metadata.modified() {
                Ok(time) => time.into(),
                Err(_) => {
                    eprintln!("Warning: Could not get modification time for {}", entry.path().display());
                    continue;
                }
            };

            if modified_time < cutoff_time {
                identified_files.push((entry.path().to_path_buf(), modified_time));
            }
        }
    }

    if identified_files.is_empty() {
        println!("No temporal debris found in the specified epoch. All clear!");
        return Ok(Vec::new());
    }

    println!("Found {} pieces of temporal debris:", identified_files.len());
    for (path, mtime) in &identified_files {
        println!("  - {} (Last modified: {})", path.display(), mtime.to_rfc3339());
    }

    let mut deleted_paths = Vec::new();

    if delete {
        if !force {
            println!("\nProceeding with deletion. Are you sure? (y/N)");
            let mut confirmation = String::new();
            io::stdin().read_line(&mut confirmation)?;

            if confirmation.trim().to_lowercase() != "y" {
                println!("Deletion cancelled. Temporal debris remains.");
                return Ok(Vec::new());
            }
        }

        let mut deleted_count = 0;
        for (path, _) in identified_files {
            match fs::remove_file(&path) {
                Ok(_) => {
                    println!("  [DELETED] {}", path.display());
                    deleted_count += 1;
                    deleted_paths.push(path);
                }
                Err(e) => {
                    eprintln!("  [ERROR] Failed to delete {}: {}", path.display(), e);
                }
            }
        }
        println!("\nChrono-Sweep complete. {} files purged.", deleted_count);
    } else if dry_run {
        println!("\nThis was a dry run. To delete, run with --delete.");
        println!("Chrono-Sweep complete. No files were altered.");
    }

    Ok(deleted_paths)
}


fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();

    if args.delete && args.dry_run {
        eprintln!("Error: Cannot use --delete and --dry-run together. Choose one.");
        std::process::exit(1);
    }

    let threshold_duration = match parse_duration_string(&args.duration) {
        Some(d) => d,
        None => {
            eprintln!("Error: Invalid duration format. Use examples like '30d', '2w', '1m', '1y'.");
            std::process::exit(1);
        }
    };

    let now = Utc::now();
    let cutoff_time = now - threshold_duration;

    println!("Initiating Chrono-Sweep in: {}", args.path.display());
    println!("Identifying temporal debris older than: {} (cutoff: {})", args.duration, cutoff_time.to_rfc3339());
    println!("Mode: {}", if args.delete { "DELETION" } else { "DRY RUN" });
    println!("----------------------------------------------------");

    // Call the core logic
    let _ = chrono_sweep_core(
        &args.path,
        cutoff_time,
        args.dry_run,
        args.delete,
        args.force,
    )?;

    Ok(())
}
