use clap::Parser;
use walkdir::WalkDir;
use std::path::{Path, PathBuf};
use std::time::{SystemTime, UNIX_EPOCH};
use std::collections::HashMap;
use chrono::{DateTime, Utc};

#[derive(Parser, Debug)]
#[command(author, version, about = "Detects temporal anomalies in file system timestamps.", long_about = None)]
struct Args {
    /// The directory to scan for temporal anomalies.
    path: PathBuf,

    /// The maximum allowed deviation in seconds from the median timestamp of a directory's files.
    /// Files exceeding this threshold will be flagged.
    #[arg(short, long, default_value_t = 3600)]
    threshold: u64,

    /// Which timestamp to analyze. Can be 'mtime' (modification time) or 'ctime' (creation time).
    #[arg(short, long, default_value = "mtime")]
    mode: String,

    /// Show more detailed output, including median timestamps.
    #[arg(short, long)]
    verbose: bool,
}

#[derive(Debug, Clone)]
struct FileTemporalData {
    path: PathBuf,
    mtime: SystemTime,
    ctime: SystemTime,
}

fn get_timestamp_for_mode(data: &FileTemporalData, mode: &str) -> Option<SystemTime> {
    match mode {
        "mtime" => Some(data.mtime),
        "ctime" => Some(data.ctime),
        _ => None,
    }
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();

    let root_path = &args.path;
    if !root_path.is_dir() {
        eprintln!("Error: Provided path is not a directory.");
        std::process::exit(1);
    }

    // Group files by their parent directory for median calculation
    let mut files_by_parent: HashMap<PathBuf, Vec<FileTemporalData>> = HashMap::new();
    for entry in WalkDir::new(root_path).into_iter().filter_map(|e| e.ok()) {
        let path = entry.path().to_path_buf();
        if entry.file_type().is_file() {
            let metadata = entry.metadata()?;
            let mtime = metadata.modified()?;
            let ctime = metadata.created()?;
            let parent_dir = path.parent().unwrap_or(Path::new("/")).to_path_buf();

            files_by_parent.entry(parent_dir).or_default().push(FileTemporalData { path, mtime, ctime });
        }
    }

    for (dir_path, files_in_dir) in files_by_parent.iter() {
        let mut timestamps_for_median: Vec<u64> = Vec::new();
        for file_datum in files_in_dir {
            if let Some(timestamp) = get_timestamp_for_mode(file_datum, &args.mode) {
                let duration_since_epoch = timestamp.duration_since(UNIX_EPOCH)?;
                timestamps_for_median.push(duration_since_epoch.as_secs());
            }
        }
        timestamps_for_median.sort_unstable();
        let median_timestamp = if timestamps_for_median.is_empty() { 0 } else { timestamps_for_median[timestamps_for_median.len() / 2] };

        if args.verbose {
            let median_dt: DateTime<Utc> = DateTime::from_timestamp(median_timestamp as i64, 0).unwrap_or_else(|| Utc::now());
            println!("\n[Verbose] Directory: {}", dir_path.display());
            println!("          Median {}: {} UTC", args.mode, median_dt.format("%Y-%m-%d %H:%M:%S"));
        }

        for file_datum in files_in_dir {
            if let Some(file_timestamp) = get_timestamp_for_mode(file_datum, &args.mode) {
                let file_secs = file_timestamp.duration_since(UNIX_EPOCH)?.as_secs();
                let drift = file_secs as i64 - median_timestamp as i64;

                if drift.abs() as u64 > args.threshold {
                    let file_dt: DateTime<Utc> = DateTime::from_timestamp(file_secs as i64, 0).unwrap_or_else(|| Utc::now());
                    let local_median_dt: DateTime<Utc> = DateTime::from_timestamp(median_timestamp as i64, 0).unwrap_or_else(|| Utc::now());

                    println!("\n[Temporal Resonance Detected] File: {}", file_datum.path.display());
                    println!("  Timestamp Type: {}", args.mode);
                    println!("  File Time: {} UTC", file_dt.format("%Y-%m-%d %H:%M:%S"));
                    println!("  Local Median: {} UTC", local_median_dt.format("%Y-%m-%d %H:%M:%S"));
                    println!("  Chronal Drift: {} seconds ({:.2} minutes) - SIGNIFICANT!", drift, drift as f64 / 60.0);
                }
            }
        }
    }

    Ok(())
}
