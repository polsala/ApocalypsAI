use clap::Parser;
use chrono::{Utc, Duration, Local, TimeZone};
use walkdir::WalkDir;
use std::path::PathBuf;
use anyhow::{Result, anyhow};

#[derive(Parser, Debug)]
#[command(author, version, about = "Nightly Temporal Purifier: Cleanse your system of digital detritus.", long_about = None)]
struct Args {
    /// The path to the directory to scan for temporal residue.
    #[arg(value_name = "PATH")]
    path: PathBuf,

    /// The duration threshold for files to be considered temporal residue (e.g., "7d", "3h", "30m", "1M").
    #[arg(short, long, value_name = "DURATION")]
    duration: String,

    /// If present, files will actually be deleted. Otherwise, it's a dry-run.
    #[arg(short, long)]
    delete: bool,
}

/// Parses a duration string (e.g., "7d", "3h", "30m") into a chrono::Duration.
fn parse_duration(duration_str: &str) -> Result<Duration> {
    let (value_str, unit) = duration_str.split_at(
        duration_str
            .find(|c: char| !c.is_ascii_digit())
            .ok_or_else(|| anyhow!("Invalid duration format: {}", duration_str))?,
    );

    let value: i64 = value_str.parse()?;

    match unit {
        "s" => Ok(Duration::seconds(value)),
        "m" => Ok(Duration::minutes(value)),
        "h" => Ok(Duration::hours(value)),
        "d" => Ok(Duration::days(value)),
        "w" => Ok(Duration::weeks(value)),
        "M" => Ok(Duration::days(value * 30)), // Approximate month
        "y" => Ok(Duration::days(value * 365)), // Approximate year
        _ => Err(anyhow!("Unknown duration unit: {}", unit)),
    }
}

fn main() -> Result<()> {
    let args = Args::parse();

    let threshold_duration = parse_duration(&args.duration)?;
    let now = Utc::now();
    let purge_cutoff = now - threshold_duration;

    println!("Nightly Temporal Purifier initiated.");
    println!("Scanning: {}", args.path.display());
    println!("Purge cutoff: {} (files older than {})", Local.from_utc(purge_cutoff, 0).format("%Y-%m-%d %H:%M:%S"), args.duration);
    println!("Mode: {}", if args.delete { "DELETE" } else { "DRY-RUN" });
    println!("--------------------------------------------------");

    let mut purged_count = 0;
    let mut listed_count = 0;

    for entry in WalkDir::new(&args.path)
        .into_iter()
        .filter_map(|e| e.ok())
    {
        let path = entry.path();
        if path.is_file() {
            if let Ok(metadata) = path.metadata() {
                if let Ok(modified_time) = metadata.modified() {
                    let modified_utc = chrono::DateTime::<Utc>::from(modified_time);

                    if modified_utc < purge_cutoff {
                        listed_count += 1;
                        if args.delete {
                            match std::fs::remove_file(path) {
                                Ok(_) => {
                                    purged_count += 1;
                                    println!("[PURGED] {}", path.display());
                                }
                                Err(e) => {
                                    eprintln!("[ERROR] Failed to purge {}: {}", path.display(), e);
                                }
                            }
                        } else {
                            println!("[DRY-RUN] Would purge {}", path.display());
                        }
                    }
                } else {
                    eprintln!("[WARNING] Could not get modified time for {}", path.display());
                }
            } else {
                eprintln!("[WARNING] Could not get metadata for {}", path.display());
            }
        }
    }

    println!("--------------------------------------------------");
    if args.delete {
        println!("Temporal purification complete. Purged {} files.", purged_count);
    } else {
        println!("Dry-run complete. Identified {} files for potential purging.", listed_count);
        println!("Run with --delete to actually purge these files.");
    }

    Ok(())
}
