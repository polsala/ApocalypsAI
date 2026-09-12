use clap::Parser;
use std::fs;
use std::path::{Path, PathBuf};
use std::time::{Duration, SystemTime, UNIX_EPOCH};
use walkdir::WalkDir;

#[derive(Parser, Debug)]
#[command(author, version, about = "A whimsical Rust CLI tool to sweep away ephemeral files and digital dust bunnies.", long_about = None)]
struct Args {
    /// One or more directories to scan for ephemeral files.
    #[arg(required = true)]
    paths: Vec<PathBuf>,

    /// The maximum age for files to be considered ephemeral. Files older than this duration will be targeted.
    /// Format: "<N>d" for days, "<N>h" for hours, "<N>m" for minutes. E.g., "7d", "24h", "30m".
    #[arg(short = 'a', long, default_value = "7d", value_parser = parse_duration)]
    age: Duration,

    /// Perform a dry run. List files that would be deleted without actually removing them.
    #[arg(short = 'd', long)]
    dry_run: bool,

    /// Enable verbose output, showing more details about scanned files.
    #[arg(short = 'v', long)]
    verbose: bool,
}

fn parse_duration(s: &str) -> Result<Duration, String> {
    let s = s.trim();
    let (value_str, unit_str) = s.split_at(s.len() - 1);

    let value = value_str.parse::<u64>().map_err(|_| format!("Invalid duration value: {}", value_str))?;

    match unit_str {
        "d" => Ok(Duration::from_secs(value * 24 * 60 * 60)),
        "h" => Ok(Duration::from_secs(value * 60 * 60)),
        "m" => Ok(Duration::from_secs(value * 60)),
        _ => Err(format!("Invalid duration unit: {}. Use 'd', 'h', or 'm'.", unit_str)),
    }
}

fn main() {
    let args = Args::parse();

    println!("\n✨ Initiating Ephemeral Data Janitor Protocol... ✨");
    if args.dry_run {
        println!("🧹 Dry run mode activated. No files will be actually removed. 🧹");
    }
    println!("Targeting files older than: {:?} \n", args.age);

    let now = SystemTime::now();
    let mut files_cleaned_count = 0;
    let mut bytes_reclaimed = 0;

    for path in &args.paths {
        if !path.exists() {
            eprintln!("⚠️ Path does not exist: {}. Skipping.", path.display());
            continue;
        }
        if args.verbose {
            println!("Scanning: {}", path.display());
        }

        for entry in WalkDir::new(path).into_iter().filter_map(|e| e.ok()) {
            let entry_path = entry.path();
            if entry_path.is_file() {
                match entry_path.metadata() {
                    Ok(metadata) => {
                        if let Ok(modified_time) = metadata.modified() {
                            if let Ok(age) = now.duration_since(modified_time) {
                                if age > args.age {
                                    let file_size = metadata.len();
                                    if args.dry_run {
                                        println!("  [DRY RUN] Would sweep: {} ({} bytes, age: {:?})", entry_path.display(), file_size, age);
                                    } else {
                                        match fs::remove_file(entry_path) {
                                            Ok(_) => {
                                                println!("  🧹 Swept away: {} ({} bytes, age: {:?})", entry_path.display(), file_size, age);
                                                files_cleaned_count += 1;
                                                bytes_reclaimed += file_size;
                                            }
                                            Err(e) => {
                                                eprintln!("  ❌ Failed to sweep {}: {}", entry_path.display(), e);
                                            }
                                        }
                                    }
                                } else if args.verbose {
                                    println!("  Keeping: {} ({} bytes, age: {:?}) - too fresh.", entry_path.display(), metadata.len(), age);
                                }
                            } else if args.verbose {
                                println!("  Keeping: {} - modified time is in the future. Temporal anomaly detected!", entry_path.display());
                            }
                        } else if args.verbose {
                            println!("  Keeping: {} - could not get modified time.", entry_path.display());
                        }
                    }
                    Err(e) => {
                        eprintln!("  ❌ Could not get metadata for {}: {}", entry_path.display(), e);
                    }
                }
            }
        }
    }

    if files_cleaned_count == 0 && bytes_reclaimed == 0 {
        println!("\n✨ All clear! No ancient digital echoes or dust bunnies found. Your digital space is pristine! ✨");
    } else if args.dry_run {
        println!("\n✨ Dry run complete! {} digital dust bunnies (totaling {} bytes) are ready for sweeping. ✨", files_cleaned_count, bytes_reclaimed);
    } else {
        println!("\n✨ Janitor duty complete! Swept away {} digital dust bunnies, reclaiming {} bytes of space! ✨", files_cleaned_count, bytes_reclaimed);
    }
}
