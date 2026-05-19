use clap::Parser;
use walkdir::WalkDir;
use chrono::{Utc, Duration, DateTime, Local};
use std::path::PathBuf;
use std::fs;
use std::error::Error;

#[derive(Parser, Debug)]
#[clap(author, version, about = "Unearth digital relics: large or old files.", long_about = None)]
pub struct Args {
    /// Directory to scan for relics
    #[clap(short, long, value_parser, default_value = ".")]
    pub path: PathBuf,

    /// Minimum size for a file to be considered a relic (e.g., 100M, 1G)
    #[clap(short, long, value_parser = parse_size_string, default_value = "0")]
    pub min_size: u64,

    /// Maximum age for a file to be considered a relic (e.g., 30d, 1w, 1y)
    /// Files older than this duration will be listed.
    #[clap(short, long, value_parser = parse_duration_string)]
    pub max_age: Option<Duration>,
}

/// Helper to parse size strings (e.g., "100", "100B", "10K", "10M", "10G", "10T")
pub fn parse_size_string(s: &str) -> Result<u64, String> {
    let s_lower = s.to_lowercase();
    let (num_str, unit_str) = if s_lower.ends_with("b") {
        (&s_lower[0..s_lower.len()-1], "b")
    } else if s_lower.ends_with("k") || s_lower.ends_with("kb") {
        (&s_lower[0..s_lower.len()-1], "k")
    } else if s_lower.ends_with("m") || s_lower.ends_with("mb") {
        (&s_lower[0..s_lower.len()-1], "m")
    } else if s_lower.ends_with("g") || s_lower.ends_with("gb") {
        (&s_lower[0..s_lower.len()-1], "g")
    } else if s_lower.ends_with("t") || s_lower.ends_with("tb") {
        (&s_lower[0..s_lower.len()-1], "t")
    } else {
        (s_lower.as_str(), "") // No unit, assume bytes
    };

    let num: u64 = num_str.parse().map_err(|_| format!("Invalid number in size: {}", num_str))?;

    match unit_str {
        "" | "b" => Ok(num),
        "k" => Ok(num * 1024),
        "m" => Ok(num * 1024 * 1024),
        "g" => Ok(num * 1024 * 1024 * 1024),
        "t" => Ok(num * 1024 * 1024 * 1024 * 1024),
        _ => Err(format!("Unknown size unit: {}", unit_str)),
    }
}

/// Helper to parse duration strings (e.g., "30d", "1w", "1y")
pub fn parse_duration_string(s: &str) -> Result<Duration, String> {
    let s_lower = s.to_lowercase();
    let (num_str, unit_str) = if s_lower.ends_with("d") {
        (&s_lower[0..s_lower.len()-1], "d")
    } else if s_lower.ends_with("w") {
        (&s_lower[0..s_lower.len()-1], "w")
    } else if s_lower.ends_with("y") {
        (&s_lower[0..s_lower.len()-1], "y")
    } else {
        return Err("Duration must end with 'd' (days), 'w' (weeks), or 'y' (years)".to_string());
    };

    let num: i64 = num_str.parse().map_err(|_| format!("Invalid number in duration: {}", num_str))?;

    match unit_str {
        "d" => Ok(Duration::days(num)),
        "w" => Ok(Duration::weeks(num)),
        "y" => Ok(Duration::days(num * 365)), // Approximate for simplicity
        _ => Err(format!("Unknown duration unit: {}", unit_str)),
    }
}

/// Helper to format bytes into human-readable string
pub fn format_bytes(bytes: u64) -> String {
    const KB: u64 = 1024;
    const MB: u64 = KB * 1024;
    const GB: u64 = MB * 1024;
    const TB: u64 = GB * 1024;

    if bytes < KB {
        format!("{} B", bytes)
    } else if bytes < MB {
        format!("{:.2} KB", bytes as f64 / KB as f64)
    } else if bytes < GB {
        format!("{:.2} MB", bytes as f64 / MB as f64)
    } else if bytes < TB {
        format!("{:.2} GB", bytes as f64 / GB as f64)
    } else {
        format!("{:.2} TB", bytes as f64 / TB as f64)
    }
}

/// Core logic to find relics based on criteria
pub fn find_relics_in_path(
    path: &PathBuf,
    min_size: u64,
    max_age: Option<Duration>,
    now: DateTime<Utc>,
) -> Result<Vec<(PathBuf, u64, DateTime<Utc>)>, Box<dyn Error>> {
    let mut relics = Vec::new();
    for entry in WalkDir::new(path)
        .into_iter()
        .filter_map(|e| e.ok())
    {
        if entry.file_type().is_file() {
            let metadata = entry.metadata()?;
            let file_size = metadata.len();
            let modified_time: DateTime<Utc> = metadata.modified()?.into();

            let is_large_enough = file_size >= min_size;
            let is_old_enough = if let Some(max_age_duration) = max_age {
                // Calculate age of file relative to 'now'
                now.signed_duration_since(modified_time) > max_age_duration
            } else {
                true // No age filter, so all files pass this check
            };

            if is_large_enough && is_old_enough {
                relics.push((entry.path().to_path_buf(), file_size, modified_time));
            }
        }
    }
    Ok(relics)
}

fn main() -> Result<(), Box<dyn Error>> {
    let args = Args::parse();
    let now = Utc::now();

    println!("\nUnearthing digital relics in: {}", args.path.display());
    println!("Criteria: Min Size = {}, Max Age = {}", 
             format_bytes(args.min_size), 
             args.max_age.map(|d| format!("Older than {}", format_duration(d))).unwrap_or_else(|| "None".to_string()));
    println!("--------------------------------------------------");

    let relics = find_relics_in_path(&args.path, args.min_size, args.max_age, now)?;

    if relics.is_empty() {
        println!("No digital relics found matching your criteria. Your digital realm is pristine!");
    } else {
        for (path, size, modified) in relics {
            println!(
                "Relic Found: {} ({} bytes, last modified: {})",
                path.display(),
                format_bytes(size),
                modified.with_timezone(&Local).format("%Y-%m-%d %H:%M:%S %Z")
            );
        }
    }

    println!("--------------------------------------------------");
    println!("Digital relic hunt complete. Happy cataloging!");

    Ok(())
}

// Helper to format chrono::Duration into a human-readable string
fn format_duration(duration: Duration) -> String {
    let total_seconds = duration.num_seconds();
    if total_seconds < 60 {
        format!("{} seconds", total_seconds)
    } else if total_seconds < 3600 {
        format!("{} minutes", total_seconds / 60)
    } else if total_seconds < 86400 {
        format!("{} hours", total_seconds / 3600)
    } else if total_seconds < 86400 * 30 {
        format!("{} days", total_seconds / 86400)
    } else if total_seconds < 86400 * 365 {
        format!("{} months", total_seconds / (86400 * 30))
    } else {
        format!("{} years", total_seconds / (86400 * 365))
    }
}
