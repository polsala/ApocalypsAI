use clap::Parser;
use std::fs;
use std::path::{Path, PathBuf};
use std::time::{SystemTime, Duration};
use chrono::{DateTime, Local}; // For human-readable timestamps

#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
struct Args {
    /// The starting directory to forage
    path: PathBuf,

    /// Maximum recursion depth (0 for current directory only, 1 for current + direct children, etc.)
    #[clap(short, long, value_name = "DEPTH")]
    depth: Option<usize>,

    /// Show more details about each file/directory
    #[clap(short, long)]
    verbose: bool,
}

#[derive(Debug, PartialEq)]
pub enum TemporalStatus {
    FreshSprout,      // 0-7 days
    BloomingArchive,  // 7-30 days
    DustyTome,        // 30-180 days
    AncientRelic,     // 180-365 days
    ForgottenEcho,    // > 365 days
    Unknown,          // Error getting metadata
}

impl TemporalStatus {
    fn description(&self) -> (&str, &str) {
        match self {
            TemporalStatus::FreshSprout => ("Fresh Sprout", "Keep nurturing."),
            TemporalStatus::BloomingArchive => ("Blooming Archive", "Review periodically."),
            TemporalStatus::DustyTome => ("Dusty Tome", "Consider archiving or refactoring."),
            TemporalStatus::AncientRelic => ("Ancient Relic", "Archive or evaluate for deletion."),
            TemporalStatus::ForgottenEcho => ("Forgotten Echo", "Deep archive or purge with care."),
            TemporalStatus::Unknown => ("Unknown Temporal State", "Cannot determine age."),
        }
    }
}

pub fn classify_path(path: &Path) -> TemporalStatus {
    let metadata = match fs::metadata(path) {
        Ok(meta) => meta,
        Err(_) => return TemporalStatus::Unknown,
    };

    let modified_time = match metadata.modified() {
        Ok(time) => time,
        Err(_) => return TemporalStatus::Unknown,
    };

    let now = SystemTime::now();
    let duration_since_modified = match now.duration_since(modified_time) {
        Ok(duration) => duration,
        Err(_) => return TemporalStatus::Unknown, // Modified time is in the future
    };

    if duration_since_modified < Duration::from_days(7) {
        TemporalStatus::FreshSprout
    } else if duration_since_modified < Duration::from_days(30) {
        TemporalStatus::BloomingArchive
    } else if duration_since_modified < Duration::from_days(180) {
        TemporalStatus::DustyTome
    } else if duration_since_modified < Duration::from_days(365) {
        TemporalStatus::AncientRelic
    } else {
        TemporalStatus::ForgottenEcho
    }
}

fn format_system_time(st: SystemTime) -> String {
    let datetime: DateTime<Local> = st.into();
    datetime.format("%Y-%m-%d %H:%M:%S").to_string()
}

fn forage_directory(path: &Path, current_depth: usize, max_depth: Option<usize>, verbose: bool) {
    if let Some(max_d) = max_depth {
        if current_depth > max_d {
            return;
        }
    }

    let entries = match fs::read_dir(path) {
        Ok(entries) => entries,
        Err(e) => {
            eprintln!("Error reading directory {:?}: {}", path, e);
            return;
        }
    };

    for entry in entries {
        let entry = match entry {
            Ok(e) => e,
            Err(e) => {
                eprintln!("Error reading directory entry: {}", e);
                continue;
            }
        };

        let entry_path = entry.path();
        let status = classify_path(&entry_path);
        let (category, suggestion) = status.description();

        let prefix = "  ".repeat(current_depth);
        let path_display = entry_path.strip_prefix(path.parent().unwrap_or(Path::new(""))).unwrap_or(&entry_path);

        if verbose {
            let metadata = fs::metadata(&entry_path);
            let modified_str = if let Ok(meta) = metadata {
                if let Ok(time) = meta.modified() {
                    format_system_time(time)
                } else {
                    "N/A".to_string()
                }
            } else {
                "N/A".to_string()
            };
            println!("{}{} [{}] (Modified: {}) - {}", prefix, path_display.display(), category, modified_str, suggestion);
        } else {
            println!("{}{} [{}] - {}", prefix, path_display.display(), category, suggestion);
        }

        if entry_path.is_dir() {
            forage_directory(&entry_path, current_depth + 1, max_depth, verbose);
        }
    }
}

fn main() {
    let args = Args::parse();

    if !args.path.exists() {
        eprintln!("Error: Path '{}' does not exist.", args.path.display());
        std::process::exit(1);
    }

    println!("Foraging digital landscape at: {}", args.path.display());
    println!("----------------------------------------------------");

    forage_directory(&args.path, 0, args.depth, args.verbose);

    println!("----------------------------------------------------");
    println!("Foraging complete. Happy digital archaeology!");
}

// Helper for Duration::from_days (not stable in std::time::Duration yet)
pub trait DurationExt {
    fn from_days(days: u64) -> Self;
}

impl DurationExt for Duration {
    fn from_days(days: u64) -> Self {
        Duration::from_secs(days * 24 * 60 * 60)
    }
}
