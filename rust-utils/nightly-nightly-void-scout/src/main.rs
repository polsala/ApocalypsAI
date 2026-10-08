use clap::Parser;
use walkdir::WalkDir;
use regex::Regex;
use chrono::{Duration, Local, DateTime};
use humansize::{format_size, DECIMAL};
use std::path::PathBuf;
use std::fs;

#[derive(Parser, Debug)]
#[command(author, version, about = "A high-performance CLI tool to quickly locate files and directories based on name patterns, size, and modification time, reporting their 'echoes' in the digital void.", long_about = None)]
struct Args {
    /// The root directory to start scouting from.
    #[arg(default_value = ".")]
    path: PathBuf,

    /// A regular expression to match against file and directory names.
    #[arg(short, long)]
    name: Option<String>,

    /// Minimum file size (e.g., 100B, 1KB, 5MB, 1GB).
    #[arg(short = 's', long, value_parser = parse_size)]
    min_size: Option<u64>,

    /// Maximum file size (e.g., 100B, 1KB, 5MB, 1GB).
    #[arg(short = 'S', long, value_parser = parse_size)]
    max_size: Option<u64>,

    /// Only show items modified within the last duration (e.g., 7d, 24h, 30m).
    #[arg(short, long, value_parser = parse_duration)]
    modified_since: Option<Duration>,

    /// Only show directories that match the criteria.
    #[arg(short, long)]
    directories_only: bool,

    /// Only show files that match the criteria.
    #[arg(short, long)]
    files_only: bool,
}

fn parse_size(s: &str) -> Result<u64, String> {
    let s_lower = s.to_lowercase();
    let (num_str, unit_str) = s_lower.split_at(s_lower.find(|c: char| c.is_alphabetic()).unwrap_or(s_lower.len()));
    let num: f64 = num_str.parse().map_err(|_| format!("Invalid number in size: {}", num_str))?;

    let multiplier = match unit_str {
        "b" | "" => 1.0,
        "kb" => 1024.0,
        "mb" => 1024.0 * 1024.0,
        "gb" => 1024.0 * 1024.0 * 1024.0,
        "tb" => 1024.0 * 1024.0 * 1024.0 * 1024.0,
        _ => return Err(format!("Invalid size unit: {}", unit_str)),
    };
    Ok((num * multiplier) as u64)
}

fn parse_duration(s: &str) -> Result<Duration, String> {
    let s_lower = s.to_lowercase();
    let (num_str, unit_str) = s_lower.split_at(s_lower.find(|c: char| c.is_alphabetic()).unwrap_or(s_lower.len()));
    let num: i64 = num_str.parse().map_err(|_| format!("Invalid number in duration: {}", num_str))?;

    match unit_str {
        "s" => Ok(Duration::seconds(num)),
        "m" => Ok(Duration::minutes(num)),
        "h" => Ok(Duration::hours(num)),
        "d" => Ok(Duration::days(num)),
        _ => Err(format!("Invalid duration unit: {}", unit_str)),
    }
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();

    let name_regex = args.name.map(|s| Regex::new(&s)).transpose()?;
    let now = Local::now();
    let min_modified_time = args.modified_since.map(|d| now - d);

    for entry in WalkDir::new(&args.path).into_iter().filter_map(|e| e.ok()) {
        let path = entry.path();
        let file_name = path.file_name().and_then(|s| s.to_str()).unwrap_or("");

        // Filter by name regex
        if let Some(ref regex) = name_regex {
            if !regex.is_match(file_name) {
                continue;
            }
        }

        let metadata = match fs::metadata(path) {
            Ok(meta) => meta,
            Err(_) => continue, // Skip if metadata can't be read (e.g., broken symlink)
        };

        // Filter by type (file/directory)
        if args.files_only && !metadata.is_file() {
            continue;
        }
        if args.directories_only && !metadata.is_dir() {
            continue;
        }
        if args.files_only && args.directories_only { // If both are specified, nothing matches
            continue;
        }
        if !args.files_only && !args.directories_only && !metadata.is_file() && !metadata.is_dir() {
            continue; // Skip other types like symlinks if no specific type is requested
        }

        // File-specific filters
        if metadata.is_file() {
            let file_size = metadata.len();
            if let Some(min_s) = args.min_size {
                if file_size < min_s {
                    continue;
                }
            }
            if let Some(max_s) = args.max_size {
                if file_size > max_s {
                    continue;
                }
            }
        }

        // Filter by modification time
        if let Some(min_time) = min_modified_time {
            if let Ok(modified_time) = metadata.modified() {
                let modified_dt: DateTime<Local> = modified_time.into();
                if modified_dt < min_time {
                    continue;
                }
            }
        }

        // Print the 'echo'
        let type_indicator = if metadata.is_dir() { "[DIR]" } else if metadata.is_file() { "[FILE]" } else { "[OTH]" };
        let size_info = if metadata.is_file() { format!(" {}", format_size(metadata.len(), DECIMAL)) } else { String::new() };
        let modified_info = if let Ok(time) = metadata.modified() {
            let dt: DateTime<Local> = time.into();
            format!(" (Modified: {})", dt.format("%Y-%m-%d %H:%M:%S"))
        } else {
            String::new()
        };

        println!("{}{} {}{}", type_indicator, size_info, path.display(), modified_info);
    }

    Ok(())
}
