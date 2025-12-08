use clap::Parser;
use std::fs;
use std::path::{Path, PathBuf};
use std::time::{SystemTime, Duration};
use walkdir::WalkDir;

#[derive(Parser, Debug)]
#[clap(author, version, about = "Sweeps for temporal dust bunnies (old, unused files).", long_about = None)]
struct Args {
    /// The root directory to start sweeping from.
    #[clap(short, long, value_parser, default_value = ".")]
    path: PathBuf,

    /// The age in days after which a file is considered a 'dust bunny' (not accessed or modified).
    #[clap(short, long, value_parser, default_value_t = 90)]
    age_days: u64,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();

    let cutoff_duration = Duration::from_days(args.age_days);
    let now = SystemTime::now();

    // Calculate cutoff time, ensuring it doesn't go before the epoch.
    let cutoff_time = now.checked_sub(cutoff_duration)
                         .ok_or("Cutoff time calculation resulted in a time before epoch. Is age_days too large?")?;

    println!("Sweeping for temporal dust bunnies older than {} days in: {}", args.age_days, args.path.display());
    println!("------------------------------------------------------------------");

    let mut found_dust_bunnies = 0;

    for entry in WalkDir::new(&args.path)
        .into_iter()
        .filter_map(|e| e.ok())
    {
        let path = entry.path();
        if path.is_file() {
            match fs::metadata(path) {
                Ok(metadata) => {
                    let mut is_old_modified = false;
                    if let Ok(modified_time) = metadata.modified() {
                        if modified_time < cutoff_time {
                            is_old_modified = true;
                        }
                    } else {
                        // If modified time is not available, assume it's old for this check.
                        // This might happen on some systems or for certain file types.
                        is_old_modified = true;
                    }

                    let mut is_old_accessed = false;
                    if let Ok(accessed_time) = metadata.accessed() {
                        if accessed_time < cutoff_time {
                            is_old_accessed = true;
                        }
                    } else {
                        // If accessed time is not available, assume it's old for this check.
                        // This is common with 'noatime' mount options.
                        is_old_accessed = true;
                    }

                    if is_old_modified && is_old_accessed {
                        println!("{}", path.display());
                        found_dust_bunnies += 1;
                    }
                }
                Err(e) => {
                    eprintln!("Error reading metadata for {}: {}", path.display(), e);
                }
            }
        }
    }

    println!("------------------------------------------------------------------");
    println!("Found {} temporal dust bunnies.", found_dust_bunnies);

    Ok(())
}

// Helper trait to add `from_days` to `std::time::Duration`
trait DurationExt {
    fn from_days(days: u64) -> Self;
}

impl DurationExt for Duration {
    fn from_days(days: u64) -> Self {
        Duration::from_secs(days * 24 * 60 * 60)
    }
}
