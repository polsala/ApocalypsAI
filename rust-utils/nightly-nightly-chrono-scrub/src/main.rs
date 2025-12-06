use clap::Parser;
use walkdir::WalkDir;
use chrono::{Utc, Duration, DateTime};
use std::path::PathBuf;
use std::fs;
use humantime::parse_duration;

#[derive(Parser, Debug)]
#[command(author, version, about = "A high-performance Rust CLI tool to identify and report on old, unused files, helping to clear digital debris.", long_about = None)]
struct Args {
    /// The directory to scan for old files.
    #[arg(short, long, value_name = "PATH")]
    path: PathBuf,

    /// Minimum age for files to be considered "old". Examples: "90d", "1y", "3m".
    /// Defaults to 90 days if not specified.
    #[arg(short, long, value_name = "DURATION", default_value = "90d")]
    age: String,

    /// Exclude files matching a glob pattern (e.g., "*.log", "temp/*").
    /// Can be specified multiple times.
    #[arg(short, long, value_name = "PATTERN")]
    exclude: Vec<String>,

    /// Minimum file size to consider (e.g., "10MB", "1KB").
    #[arg(long, value_name = "SIZE")]
    min_size: Option<String>,

    /// Maximum file size to consider (e.g., "1GB", "500KB").
    #[arg(long, value_name = "SIZE")]
    max_size: Option<String>,
}

fn parse_size_string(s: &str) -> Option<u64> {
    let s_lower = s.to_lowercase();
    let (num_str, unit_str) = if s_lower.ends_with("kb") {
        (&s_lower[0..s_lower.len()-2], "kb")
    } else if s_lower.ends_with("mb") {
        (&s_lower[0..s_lower.len()-2], "mb")
    } else if s_lower.ends_with("gb") {
        (&s_lower[0..s_lower.len()-2], "gb")
    } else if s_lower.ends_with("b") {
        (&s_lower[0..s_lower.len()-1], "b")
    } else {
        (s_lower.as_str(), "")
    };

    let num: u64 = num_str.trim().parse().ok()?;
    match unit_str {
        "kb" => Some(num * 1024),
        "mb" => Some(num * 1024 * 1024),
        "gb" => Some(num * 1024 * 1024 * 1024),
        "b" | "" => Some(num),
        _ => None,
    }
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();

    if !args.path.exists() {
        eprintln!("Error: Path '{}' does not exist.", args.path.display());
        std::process::exit(1);
    }
    if !args.path.is_dir() {
        eprintln!("Error: Path '{}' is not a directory.", args.path.display());
        std::process::exit(1);
    }

    let min_age_duration = parse_duration(&args.age)
        .map_err(|e| format!("Invalid age duration format: {}. Example: 90d, 1y, 3m. Error: {}", args.age, e))?;

    let cutoff_time = Utc::now() - Duration::from_std(min_age_duration)?;

    let min_size_bytes = args.min_size.as_ref().and_then(|s| parse_size_string(s));
    let max_size_bytes = args.max_size.as_ref().and_then(|s| parse_size_string(s));

    println!("Scanning '{}' for files older than {} (cutoff: {})...",
             args.path.display(), args.age, cutoff_time.to_rfc2822());
    println!("------------------------------------------------------------------");

    let mut found_files = 0;

    for entry in WalkDir::new(&args.path)
        .into_iter()
        .filter_map(|e| e.ok())
    {
        let path = entry.path();
        if path.is_file() {
            let metadata = match fs::metadata(path) {
                Ok(meta) => meta,
                Err(_) => {
                    // println!("Warning: Could not get metadata for {}", path.display());
                    continue;
                }
            };

            // Check exclusion patterns (simple contains for now)
            let path_str = path.to_string_lossy();
            if args.exclude.iter().any(|pattern| {
                path_str.contains(pattern.trim_start_matches('*').trim_end_matches('*'))
            }) {
                continue;
            }

            let modified_time: DateTime<Utc> = match metadata.modified() {
                Ok(time) => time.into(),
                Err(_) => {
                    // println!("Warning: Could not get modification time for {}", path.display());
                    continue;
                }
            };

            if modified_time < cutoff_time {
                let file_size = metadata.len();

                if let Some(min_s) = min_size_bytes {
                    if file_size < min_s {
                        continue;
                    }
                }
                if let Some(max_s) = max_size_bytes {
                    if file_size > max_s {
                        continue;
                    }
                }

                println!("  Path: {}", path.display());
                println!("    Size: {} bytes", file_size);
                println!("    Last Modified: {}", modified_time.to_rfc2822());
                println!();
                found_files += 1;
            }
        }
    }

    println!("------------------------------------------------------------------");
    println!("Scan complete. Found {} old files.", found_files);

    Ok(())
}
