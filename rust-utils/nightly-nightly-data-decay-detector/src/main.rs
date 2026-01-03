use clap::Parser;
use std::fs;
use std::path::{Path, PathBuf};
use std::time::{SystemTime, UNIX_EPOCH};
use walkdir::WalkDir;

#[derive(Parser, Debug)]
#[clap(author, version, about = "Detects 'decaying' or forgotten files based on access/modification times.", long_about = None)]
struct Args {
    /// The directory to scan for decaying files.
    path: PathBuf,

    /// Only show files with a decay score equal to or higher than this value.
    #[clap(short = 't', long, default_value_t = 0.0)]
    threshold: f64,

    /// Sort output by 'decay' (desc), 'mtime' (asc), or 'atime' (asc).
    #[clap(short = 's', long, default_value = "decay", possible_values = &["decay", "mtime", "atime"])]
    sort_by: String,

    /// Limit the number of results displayed. 0 for no limit.
    #[clap(short = 'l', long, default_value_t = 0)]
    limit: usize,

    /// Show more detailed timestamps (including time of day).
    #[clap(short = 'v', long)]
    verbose: bool,
}

#[derive(Debug, PartialEq, PartialOrd)]
struct FileDecayInfo {
    path: PathBuf,
    decay_score: f64,
    mtime: SystemTime,
    atime: SystemTime,
}

fn calculate_decay_score(mtime: SystemTime, atime: SystemTime) -> f64 {
    let now = SystemTime::now();

    let days_since_mtime = now
        .duration_since(mtime)
        .unwrap_or_default()
        .as_secs_f64()
        / (60.0 * 60.0 * 24.0);

    let days_since_atime = now
        .duration_since(atime)
        .unwrap_or_default()
        .as_secs_f64()
        / (60.0 * 60.0 * 24.0);

    // Whimsical decay formula: more weight on modification time
    (days_since_mtime * 0.8) + (days_since_atime * 0.2)
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();

    let mut decayed_files: Vec<FileDecayInfo> = Vec::new();

    for entry in WalkDir::new(&args.path)
        .into_iter()
        .filter_map(|e| e.ok())
    {
        let path = entry.path();
        if path.is_file() {
            let metadata = fs::metadata(path)?;
            let mtime = metadata.modified()?;
            let atime = metadata.accessed()?;

            let decay_score = calculate_decay_score(mtime, atime);

            if decay_score >= args.threshold {
                decayed_files.push(FileDecayInfo {
                    path: path.to_path_buf(),
                    decay_score,
                    mtime,
                    atime,
                });
            }
        }
    }

    match args.sort_by.as_str() {
        "decay" => decayed_files.sort_by(|a, b| b.decay_score.partial_cmp(&a.decay_score).unwrap_or(std::cmp::Ordering::Equal)),
        "mtime" => decayed_files.sort_by(|a, b| a.mtime.cmp(&b.mtime)),
        "atime" => decayed_files.sort_by(|a, b| a.atime.cmp(&b.atime)),
        _ => { /* Should not happen due to clap possible_values */ }
    }

    let limit = if args.limit == 0 { decayed_files.len() } else { args.limit };

    for file_info in decayed_files.iter().take(limit) {
        let mtime_str = format_system_time(file_info.mtime, args.verbose);
        let atime_str = format_system_time(file_info.atime, args.verbose);

        println!(
            "Decay: {:.2} | Modified: {} | Accessed: {} | Path: {}",
            file_info.decay_score,
            mtime_str,
            atime_str,
            file_info.path.display()
        );
    }

    Ok(())
}

fn format_system_time(time: SystemTime, verbose: bool) -> String {
    let datetime: chrono::DateTime<chrono::Local> = time.into();
    if verbose {
        datetime.format("%Y-%m-%d %H:%M:%S").to_string()
    } else {
        datetime.format("%Y-%m-%d").to_string()
    }
}

// To make this code runnable, add the following to your Cargo.toml:
// [dependencies]
// clap = { version = "4", features = ["derive"] }
// walkdir = "2"
// chrono = "0.4"
