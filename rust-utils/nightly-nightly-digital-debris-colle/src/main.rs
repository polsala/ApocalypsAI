use clap::Parser;
use std::fs;
use std::path::{Path, PathBuf};
use std::time::{SystemTime, UNIX_EPOCH};
use walkdir::WalkDir;
use chrono::{Utc, Duration, DateTime};
use serde::Serialize;

#[derive(Parser, Debug)]
#[clap(author, version, about = "Nightly Digital Debris Collector: Reclaim your digital wasteland!", long_about = None)]
struct Args {
    /// The root directory to start scanning from.
    #[clap(default_value = ".")]
    path: PathBuf,

    /// Files/directories older than this many days are considered debris.
    #[clap(short = 'a', long, default_value_t = 365)]
    age: u64,

    /// Files smaller than this many bytes are considered debris.
    #[clap(short = 's', long, default_value_t = 1024)]
    size: u64,

    /// Include empty directories in the debris report.
    #[clap(short = 'e', long)]
    empty_dirs: bool,

    /// Output the report in JSON format.
    #[clap(short = 'j', long)]
    json: bool,

    /// Show more detailed scanning progress.
    #[clap(short = 'v', long)]
    verbose: bool,
}

#[derive(Debug, Serialize)]
#[serde(rename_all = "snake_case")]
enum DebrisReason {
    OlderThanAge,
    SmallerThanSize,
    IsEmpty,
}

#[derive(Debug, Serialize)]
struct DebrisItem {
    path: PathBuf,
    #[serde(rename = "type")]
    item_type: String,
    reason: DebrisReason,
    #[serde(skip_serializing_if = "Option::is_none")]
    details: Option<DebrisDetails>,
}

#[derive(Debug, Serialize)]
#[serde(rename_all = "snake_case")]
enum DebrisDetails {
    File {
        last_modified: String,
        age_days: u64,
        size_bytes: u64,
        threshold_bytes: u64,
    },
    Directory {},
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();

    if args.verbose {
        eprintln!("Scanning for byte-dust in \"{}\" with criteria:", args.path.display());
        eprintln!("  - Age threshold: {} days", args.age);
        eprintln!("  - Size threshold: {} bytes", args.size);
        eprintln!("  - Include empty directories: {}", args.empty_dirs);
    }

    let mut debris_items: Vec<DebrisItem> = Vec::new();
    let now: DateTime<Utc> = Utc::now();
    let age_threshold = Duration::days(args.age as i64);

    if !args.path.exists() {
        eprintln!("Error: Path '{}' does not exist.", args.path.display());
        std::process::exit(1);
    }

    for entry in WalkDir::new(&args.path).into_iter().filter_map(|e| e.ok()) {
        let path = entry.path();
        let metadata = match fs::metadata(path) {
            Ok(m) => m,
            Err(_) => continue, // Skip if metadata can't be read
        };

        let mut is_debris = false;
        let mut reason: Option<DebrisReason> = None;
        let mut details: Option<DebrisDetails> = None;

        if metadata.is_file() {
            let file_size = metadata.len();
            if file_size < args.size {
                is_debris = true;
                reason = Some(DebrisReason::SmallerThanSize);
                details = Some(DebrisDetails::File {
                    last_modified: "N/A".to_string(), // Will be updated if also old
                    age_days: 0, // Will be updated if also old
                    size_bytes: file_size,
                    threshold_bytes: args.size,
                });
            }

            if let Ok(modified_time) = metadata.modified() {
                let modified_datetime: DateTime<Utc> = modified_time.into();
                if now - modified_datetime > age_threshold {
                    is_debris = true;
                    reason = Some(DebrisReason::OlderThanAge);
                    let age_in_days = (now - modified_datetime).num_days() as u64;
                    details = Some(DebrisDetails::File {
                        last_modified: modified_datetime.to_rfc3339(),
                        age_days: age_in_days,
                        size_bytes: file_size,
                        threshold_bytes: args.size,
                    });
                }
            }
        } else if metadata.is_dir() && args.empty_dirs {
            // Check if directory is empty
            let mut dir_entries = fs::read_dir(path)?;
            if dir_entries.next().is_none() {
                is_debris = true;
                reason = Some(DebrisReason::IsEmpty);
                details = Some(DebrisDetails::Directory {});
            }
        }

        if is_debris {
            if let Some(r) = reason {
                debris_items.push(DebrisItem {
                    path: path.to_path_buf(),
                    item_type: if metadata.is_file() { "file".to_string() } else { "directory".to_string() },
                    reason: r,
                    details,
                });
            }
        }
    }

    if args.json {
        println!("{}", serde_json::to_string_pretty(&debris_items)?);
    } else {
        if debris_items.is_empty() {
            println!("Reclamation complete. No digital debris found in \"{}\".", args.path.display());
        } else {
            println!("\nReclamation complete. Digital debris identified:");
            for item in &debris_items {
                println!("  Path: {}", item.path.display());
                println!("  Type: {}", item.item_type);
                match &item.reason {
                    DebrisReason::OlderThanAge => {
                        println!("  Reason: Older than {} days", args.age);
                        if let Some(DebrisDetails::File { last_modified, age_days, .. }) = &item.details {
                            println!("    (Last modified: {} ({} days ago))", last_modified, age_days);
                        }
                    },
                    DebrisReason::SmallerThanSize => {
                        println!("  Reason: Smaller than {} bytes", args.size);
                        if let Some(DebrisDetails::File { size_bytes, .. }) = &item.details {
                            println!("    (Size: {} bytes)", size_bytes);
                        }
                    },
                    DebrisReason::IsEmpty => {
                        println!("  Reason: Is empty");
                    },
                }
                println!();
            }
            println!("Total debris items found: {}.", debris_items.len());
        }
    }

    Ok(())
}
