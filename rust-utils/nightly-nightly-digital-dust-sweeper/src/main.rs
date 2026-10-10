use clap::Parser;
use walkdir::WalkDir;
use chrono::{Utc, Duration};
use std::fs;
use std::path::PathBuf;
use std::error::Error;
use std::fmt;

// Custom error type for better error handling in run_sweeper
#[derive(Debug)]
struct SweeperError(String);

impl fmt::Display for SweeperError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{}", self.0)
    }
}

impl Error for SweeperError {}

#[derive(Parser, Debug)]
#[command(author, version, about = "Sweeps away digital 'dust bunnies' (stale files) from your file system.", long_about = None)]
pub struct Args { // Made public for testing
    /// The directory to scan for dust bunnies.
    #[arg(short, long, value_name = "PATH")]
    pub path: PathBuf, // Made public for testing

    /// Files older than this many days (based on last modification time) are considered dust bunnies.
    #[arg(short, long, default_value_t = 30, value_name = "DAYS")]
    pub age_days: u64, // Made public for testing

    /// Perform a dry run: list files that would be deleted without actually deleting them.
    #[arg(short, long)]
    pub dry_run: bool, // Made public for testing

    /// Actually delete the identified dust bunnies. Use with caution!
    #[arg(short, long)]
    pub delete: bool, // Made public for testing
}

pub fn run_sweeper(args: Args) -> Result<(u64, u64), Box<dyn Error>> {
    if !args.path.is_dir() {
        return Err(Box::new(SweeperError(format!("Provided path '{}' is not a directory or does not exist.", args.path.display()))));
    }

    if args.delete && args.dry_run {
        return Err(Box::new(SweeperError("Cannot use --delete and --dry-run simultaneously. Choose one.".to_string())));
    }

    let cutoff_time = Utc::now() - Duration::days(args.age_days as i64);
    let mut dust_bunnies_found = 0;
    let mut bytes_to_reclaim = 0;

    println!("Scanning '{}' for files older than {} days...", args.path.display(), args.age_days);
    println!("Cutoff time: {}", cutoff_time.to_rfc2822());

    for entry in WalkDir::new(&args.path)
        .into_iter()
        .filter_map(|e| e.ok())
    {
        let path = entry.path();
        if path.is_file() {
            if let Ok(metadata) = fs::metadata(path) {
                if let Ok(modified_time) = metadata.modified() {
                    let modified_utc: chrono::DateTime<Utc> = modified_time.into();
                    if modified_utc < cutoff_time {
                        dust_bunnies_found += 1;
                        bytes_to_reclaim += metadata.len();

                        if args.dry_run {
                            println!("DRY RUN: Would delete '{}' (modified: {})", path.display(), modified_utc.to_rfc2822());
                        } else if args.delete {
                            match fs::remove_file(path) {
                                Ok(_) => println!("DELETED: '{}' (modified: {})", path.display(), modified_utc.to_rfc2822()),
                                Err(e) => eprintln!("ERROR deleting '{}': {}", path.display(), e),
                            }
                        } else {
                            println!("Found: '{}' (modified: {})", path.display(), modified_utc.to_rfc2822());
                        }
                    }
                } else {
                    eprintln!("Warning: Could not get modified time for '{}'", path.display());
                }
            } else {
                eprintln!("Warning: Could not get metadata for '{}'", path.display());
            }
        }
    }

    println!("\n--- Scan Complete ---");
    println!("Total digital dust bunnies found: {}", dust_bunnies_found);
    println!("Estimated space to reclaim: {} bytes ({} MB)", bytes_to_reclaim, bytes_to_reclaim / (1024 * 1024));

    if args.dry_run {
        println!("This was a DRY RUN. No files were actually deleted.");
    } else if args.delete {
        println!("Files were DELETED as requested. Proceed with caution next time!");
    } else {
        println!("No action taken. Use --dry-run to preview or --delete to remove files.");
    }

    Ok((dust_bunnies_found, bytes_to_reclaim))
}

fn main() {
    let args = Args::parse();
    match run_sweeper(args) {
        Ok(_) => {},
        Err(e) => {
            eprintln!("Error: {}", e);
            std::process::exit(1);
        }
    }
}
