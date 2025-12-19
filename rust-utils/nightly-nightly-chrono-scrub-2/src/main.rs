use clap::Parser;
use walkdir::WalkDir;
use chrono::{Utc, DateTime, Duration};
use std::fs;
use std::path::PathBuf;

#[derive(Parser, Debug)]
#[command(author, version, about = "Detects temporal anomalies in file system timestamps.", long_about = None)]
struct Args {
    /// The root directory to start scanning from.
    #[arg(default_value = ".")]
    path: PathBuf,

    /// Detects files not modified in at least DAYS days.
    #[arg(long)]
    stale_days: Option<u64>,

    /// Detects files with creation/modification times more than SECONDS into the future.
    #[arg(long, default_value_t = 60)]
    future_tolerance: u64,

    /// Detects files where modification time is earlier than creation time.
    #[arg(long)]
    inconsistent: bool,

    /// Enable verbose output, showing more details for each anomaly.
    #[arg(short, long)]
    verbose: bool,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();
    let now = Utc::now();

    let stale_duration = args.stale_days.map(|days| Duration::days(days as i64));
    let future_tolerance_duration = Duration::seconds(args.future_tolerance as i64);

    if args.verbose {
        println!("Scanning directory: {}", args.path.display());
        if let Some(days) = args.stale_days { println!("  - Stale files: older than {} days", days); }
        println!("  - Future files: more than {} seconds into the future", args.future_tolerance);
        if args.inconsistent { println!("  - Inconsistent timestamps: mtime < ctime"); }
        println!("--------------------------------------------------");
    }

    for entry in WalkDir::new(&args.path)
        .into_iter()
        .filter_map(|e| e.ok())
    {
        let path = entry.path();
        if path.is_dir() { continue; }

        let metadata = match fs::metadata(path) {
            Ok(meta) => meta,
            Err(e) => {
                if args.verbose { eprintln!("Error reading metadata for {}: {}", path.display(), e); }
                continue;
            }
        };

        let mut anomalies_found = Vec::new();

        let modified_time: Option<DateTime<Utc>> = metadata.modified().ok().map(Into::into);
        let created_time: Option<DateTime<Utc>> = metadata.created().ok().map(Into::into);

        // Check for stale files
        if let (Some(stale_dur), Some(m_time)) = (stale_duration, modified_time) {
            if now.signed_duration_since(m_time) > stale_dur {
                anomalies_found.push(format!("Stale (last modified: {})", m_time.to_rfc3339()));
            }
        }

        // Check for future-dated files
        if let Some(m_time) = modified_time {
            if m_time > now + future_tolerance_duration {
                anomalies_found.push(format!("Future-dated (modified: {})", m_time.to_rfc3339()));
            }
        }
        if let Some(c_time) = created_time {
            if c_time > now + future_tolerance_duration {
                anomalies_found.push(format!("Future-dated (created: {})", c_time.to_rfc3339()));
            }
        }

        // Check for inconsistent timestamps (mtime < ctime)
        if args.inconsistent {
            if let (Some(m_time), Some(c_time)) = (modified_time, created_time) {
                if m_time < c_time {
                    anomalies_found.push(format!("Inconsistent (modified: {}, created: {})", m_time.to_rfc3339(), c_time.to_rfc3339()));
                }
            }
        }

        if !anomalies_found.is_empty() {
            println!("Anomaly detected in {}: {}", path.display(), anomalies_found.join(", "));
        }
    }

    Ok(())
}
