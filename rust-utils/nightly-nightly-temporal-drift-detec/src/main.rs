use clap::Parser;
use std::path::{Path, PathBuf};
use std::time::{SystemTime, Duration};
use walkdir::WalkDir;

/// A high-performance CLI tool to detect and report files with unusual modification time drifts,
/// indicating potential system anomalies.
#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
struct Args {
    /// The root directory to start scanning from. Defaults to the current directory if not provided.
    #[clap(name = "PATH", default_value = ".")]
    path: PathBuf,

    /// Tolerance in seconds for mtime being in the future. Files with mtime up to SECONDS in the future will be ignored.
    #[clap(short = 'f', long, default_value_t = 0)]
    future_threshold: u64,

    /// Enable verbose output, showing all files scanned (not just anomalies).
    #[clap(short = 'v', long)]
    verbose: bool,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();

    let current_time = SystemTime::now();
    let future_threshold_duration = Duration::from_secs(args.future_threshold);

    println!("Scanning for temporal drifts in: {}", args.path.display());
    if args.future_threshold > 0 {
        println!("Ignoring future mtimes up to {} seconds.", args.future_threshold);
    }

    for entry in WalkDir::new(&args.path)
        .into_iter()
        .filter_map(|e| e.ok())
    {
        let path = entry.path();
        if path.is_file() {
            if args.verbose {
                println!("Scanning file: {}", path.display());
            }

            match entry.metadata() {
                Ok(metadata) => {
                    let mtime = metadata.modified()?;
                    let ctime = metadata.created()?;

                    // Anomaly 1: mtime is in the future (beyond threshold)
                    if mtime > current_time + future_threshold_duration {
                        println!(
                            "Temporal Anomaly Detected: \"{}\" - mtime is in the future ({:?})",
                            path.display(),
                            mtime
                        );
                    }

                    // Anomaly 2: mtime is older than ctime
                    if mtime < ctime {
                        println!(
                            "Temporal Anomaly Detected: \"{}\" - mtime ({:?}) is older than ctime ({:?})",
                            path.display(),
                            mtime,
                            ctime
                        );
                    }
                }
                Err(e) => {
                    eprintln!("Error reading metadata for \"{}\": {}", path.display(), e);
                }
            }
        }
    }

    Ok(())
}
