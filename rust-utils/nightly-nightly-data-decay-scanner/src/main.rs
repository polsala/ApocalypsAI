use clap::Parser;
use std::fs;
use std::path::{Path, PathBuf};
use std::time::{SystemTime, Duration};
use walkdir::WalkDir;

#[derive(Parser, Debug)]
#[command(author, version, about = "Scans a directory to identify files with high 'data decay' and suggests archival or deletion.", long_about = None)]
struct Args {
    /// The root directory to scan for data decay.
    path: PathBuf,

    /// Sets the threshold in days for a file to be considered a 'Deletion Candidate'.
    /// Files older than DAYS will be marked for deletion. Files older than DAYS / 2
    /// (but not older than DAYS) will be marked for archival. Default is 365 days.
    #[arg(short, long, default_value_t = 365)]
    threshold: u64,

    /// Show more detailed information, including exact decay days.
    #[arg(short, long)]
    verbose: bool,
}

#[derive(Debug)]
struct FileDecayInfo {
    path: PathBuf,
    decay_days: u64,
}

fn get_decay_days(metadata: &fs::Metadata) -> Option<u64> {
    let now = SystemTime::now();

    let modified_time = metadata.modified().ok()?;
    let accessed_time = metadata.accessed().ok()?; // atime might be unreliable

    let last_activity_time = if accessed_time > modified_time {
        accessed_time
    } else {
        modified_time
    };

    let duration_since_activity = now.duration_since(last_activity_time).ok()?;
    Some(duration_since_activity.as_secs() / (24 * 60 * 60))
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();

    if !args.path.is_dir() {
        eprintln!("Error: Provided path is not a directory: {}", args.path.display());
        std::process::exit(1);
    }

    let mut decay_files: Vec<FileDecayInfo> = Vec::new();

    for entry in WalkDir::new(&args.path)
        .into_iter()
        .filter_map(|e| e.ok())
    {
        let path = entry.path();
        if path.is_file() {
            if let Ok(metadata) = fs::metadata(path) {
                if let Some(decay_days) = get_decay_days(&metadata) {
                    decay_files.push(FileDecayInfo { path: path.to_path_buf(), decay_days });
                }
            }
        }
    }

    decay_files.sort_by(|a, b| b.decay_days.cmp(&a.decay_days));

    let archival_threshold = args.threshold / 2;
    let deletion_threshold = args.threshold;

    println!("\n--- Data Decay Scan Results for '{}' ---", args.path.display());
    println!("Deletion Threshold: {} days, Archival Threshold: {} days\n", deletion_threshold, archival_threshold);

    if decay_files.is_empty() {
        println!("No files found or no decay information available.");
    } else {
        for file_info in decay_files {
            let status = if file_info.decay_days >= deletion_threshold {
                "Deletion Candidate"
            } else if file_info.decay_days >= archival_threshold {
                "Archival Candidate"
            } else {
                "Active Data"
            };

            if args.verbose {
                println!("[{: <20}] {: <4} days: {}", status, file_info.decay_days, file_info.path.display());
            } else {
                println!("[{: <20}] {}", status, file_info.path.display());
            }
        }
    }

    println!("\n--- End of Scan ---");

    Ok(())
}
