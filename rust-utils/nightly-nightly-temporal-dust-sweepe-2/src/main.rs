use clap::Parser;
use walkdir::WalkDir;
use chrono::{Utc, Duration, DateTime};
use std::path::PathBuf;
use std::time::SystemTime;
use std::error::Error;
use std::fmt;

// Custom error type for better error handling in main_logic
#[derive(Debug)]
pub enum DustSweeperError {
    PathDoesNotExist(PathBuf),
    PathIsNotDirectory(PathBuf),
    IoError(std::io::Error),
    MetadataError(std::io::Error),
}

impl fmt::Display for DustSweeperError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            DustSweeperError::PathDoesNotExist(path) => write!(f, "Error: Path '{}' does not exist.", path.display()),
            DustSweeperError::PathIsNotDirectory(path) => write!(f, "Error: Path '{}' is not a directory.", path.display()),
            DustSweeperError::IoError(err) => write!(f, "I/O Error: {}", err),
            DustSweeperError::MetadataError(err) => write!(f, "Metadata Error: {}", err),
        }
    }
}

impl Error for DustSweeperError {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        match self {
            DustSweeperError::IoError(err) => Some(err),
            DustSweeperError::MetadataError(err) => Some(err),
            _ => None,
        }
    }
}

impl From<std::io::Error> for DustSweeperError {
    fn from(err: std::io::Error) -> Self {
        DustSweeperError::IoError(err)
    }
}


#[derive(Parser, Debug)]
#[clap(author, version, about = "Scan for 'temporal dust bunnies' - files untouched for a configurable duration.", long_about = None)]
pub struct Args {
    /// The directory to scan for temporal dust bunnies.
    #[clap(value_parser)]
    pub path: PathBuf,

    /// The minimum number of days a file must be untouched to be considered a dust bunny.
    #[clap(short = 'd', long, default_value = "90")]
    pub days: u64,

    /// Use last modification time instead of last access time.
    /// (Note: Access time tracking can be disabled on some filesystems for performance,
    /// making --modified a more reliable option in those cases.)
    #[clap(short = 'm', long)]
    pub modified: bool,

    /// Show more detailed output, including the exact timestamp.
    #[clap(short = 'v', long)]
    pub verbose: bool,
}

fn main() {
    let args = Args::parse();
    if let Err(e) = main_logic(args) {
        eprintln!("{}", e);
        std::process::exit(1);
    }
}

// Refactored main logic into a public function for testing
pub fn main_logic(args: Args) -> Result<(), DustSweeperError> {
    let threshold_duration = Duration::days(args.days as i64);
    let now = Utc::now();

    if !args.path.exists() {
        return Err(DustSweeperError::PathDoesNotExist(args.path));
    }
    if !args.path.is_dir() {
        return Err(DustSweeperError::PathIsNotDirectory(args.path));
    }

    println!("Scanning '{}' for files untouched for at least {} days...", args.path.display(), args.days);
    println!("--- Temporal Dust Bunnies Found ---");

    let mut found_count = 0;

    for entry in WalkDir::new(&args.path)
        .into_iter()
        .filter_map(|e| e.ok())
    {
        if entry.file_type().is_file() {
            let metadata = entry.metadata().map_err(DustSweeperError::MetadataError)?;
            let file_time: SystemTime;

            if args.modified {
                file_time = metadata.modified().map_err(DustSweeperError::MetadataError)?;
            } else {
                // Fallback to modified time if access time is not available or fails
                file_time = metadata.accessed().unwrap_or_else(|_| {
                    eprintln!("Warning: Could not get access time for '{}'. Falling back to modification time.", entry.path().display());
                    metadata.modified().expect("Failed to get modification time") // This expect will panic if modified also fails
                });
            }

            let file_datetime: DateTime<Utc> = file_time.into();
            let age = now - file_datetime;

            if age >= threshold_duration {
                found_count += 1;
                let age_in_days = age.num_days();
                if args.verbose {
                    println!("  Path: {}", entry.path().display());
                    println!("    Last touched: {} ({} days ago)", file_datetime.to_rfc2822(), age_in_days);
                } else {
                    println!("  {} ({} days ago)", entry.path().display(), age_in_days);
                }
            }
        }
    }

    println!("-----------------------------------");
    println!("Found {} temporal dust bunnies.", found_count);

    Ok(())
}
