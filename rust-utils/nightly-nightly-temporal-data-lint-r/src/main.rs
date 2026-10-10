use clap::Parser;
use walkdir::WalkDir;
use chrono::{Duration, Utc, DateTime, Local};
use std::fs;
use std::path::PathBuf;
use std::io::{self, Write};

#[derive(Parser, Debug)]
#[clap(author, version, about = "A high-performance CLI tool to identify and clean up temporal data lint (old, unused files) across specified directories.", long_about = None)]
struct Args {
    /// The directory to scan for temporal lint.
    #[clap(short, long, default_value = ".")]
    path: PathBuf,

    /// Files older than this duration will be considered lint. Examples: "30d", "1w", "1y".
    #[clap(short, long, value_parser = parse_duration)]
    age: Duration,

    /// Perform a dry run: list files that would be deleted without actually deleting them.
    /// This is the default behavior.
    #[clap(short, long, action)]
    dry_run: bool,

    /// Actually delete the identified temporal lint. Use with caution!
    #[clap(short, long, action, conflicts_with = "dry_run")]
    delete: bool,
}

fn parse_duration(s: &str) -> Result<Duration, String> {
    let s = s.trim();
    if s.ends_with('d') {
        let days = s[..s.len() - 1].parse::<i64>().map_err(|e| e.to_string())?;
        Ok(Duration::days(days))
    } else if s.ends_with('w') {
        let weeks = s[..s.len() - 1].parse::<i64>().map_err(|e| e.to_string())?;
        Ok(Duration::weeks(weeks))
    } else if s.ends_with('y') {
        let years = s[..s.len() - 1].parse::<i64>().map_err(|e| e.to_string())?;
        // Approximate years as 365 days for simplicity
        Ok(Duration::days(years * 365))
    } else {
        Err("Invalid duration format. Use '30d', '1w', '1y' etc.".to_string())
    }
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();

    let now = Utc::now();
    let cutoff_time = now - args.age;

    println!("Scanning directory: {}", args.path.display());
    println!("Identifying files older than: {} (cutoff: {})", format_duration(&args.age), cutoff_time.with_timezone(&Local).format("%Y-%m-%d %H:%M:%S"));
    println!("Mode: {}", if args.delete { "DELETE" } else { "DRY RUN" });
    println!("---");

    let mut lint_found = 0;
    let mut lint_deleted = 0;

    for entry in WalkDir::new(&args.path)
        .into_iter()
        .filter_map(|e| e.ok())
    {
        let path = entry.path();
        if path.is_file() {
            if let Ok(metadata) = fs::metadata(path) {
                if let Ok(modified_time) = metadata.modified() {
                    let modified_utc: DateTime<Utc> = modified_time.into();
                    if modified_utc < cutoff_time {
                        lint_found += 1;
                        println!("Lint found: {} (Modified: {})", path.display(), modified_utc.with_timezone(&Local).format("%Y-%m-%d %H:%M:%S"));

                        if args.delete {
                            match fs::remove_file(path) {
                                Ok(_) => {
                                    lint_deleted += 1;
                                    println!("  -> DELETED");
                                }
                                Err(e) => {
                                    eprintln!("  -> ERROR deleting {}: {}", path.display(), e);
                                }
                            }
                        }
                    }
                } else {
                    eprintln!("Warning: Could not get modified time for {}", path.display());
                }
            } else {
                eprintln!("Warning: Could not get metadata for {}", path.display());
            }
        }
    }

    println!("---");
    println!("Scan complete.");
    println!("Total temporal lint identified: {}", lint_found);
    if args.delete {
        println!("Total temporal lint deleted: {}", lint_deleted);
    } else {
        println!("Run with --delete to remove these files.");
    }

    Ok(())
}

fn format_duration(duration: &Duration) -> String {
    let total_seconds = duration.num_seconds();
    if total_seconds % (365 * 24 * 3600) == 0 {
        format!("{} years", total_seconds / (365 * 24 * 3600))
    } else if total_seconds % (7 * 24 * 3600) == 0 {
        format!("{} weeks", total_seconds / (7 * 24 * 3600))
    } else if total_seconds % (24 * 3600) == 0 {
        format!("{} days", total_seconds / (24 * 3600))
    } else {
        format!("{} seconds", total_seconds)
    }
}
