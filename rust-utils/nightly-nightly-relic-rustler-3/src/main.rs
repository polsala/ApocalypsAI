use clap::Parser;
use walkdir::WalkDir;
use chrono::{Utc, Duration, DateTime};
use std::fs;
use std::path::PathBuf;
use std::io::{self, Write};
use std::time::SystemTime;

#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
struct Args {
    /// Path to the directory to scan for relics
    #[clap(value_parser)]
    path: PathBuf,

    /// Minimum age in days for a file to be considered a relic (default: 90)
    #[clap(short, long, default_value_t = 90)]
    age: i64,

    /// Output format (text or json)
    #[clap(short, long, default_value = "text")]
    output: String,
}

#[derive(Debug, serde::Serialize)]
struct Relic {
    path: String,
    size_bytes: u64,
    modified_at: String,
    age_days: i64,
    file_type: String,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();

    let cutoff_date = Utc::now() - Duration::days(args.age);
    let mut relics = Vec::new();

    for entry in WalkDir::new(&args.path).into_iter().filter_map(|e| e.ok()) {
        let path = entry.path();
        if path.is_file() {
            if let Ok(metadata) = fs::metadata(path) {
                if let Ok(modified_time) = metadata.modified() {
                    let modified_utc: DateTime<Utc> = modified_time.into();
                    if modified_utc < cutoff_date {
                        let age_duration = Utc::now() - modified_utc;
                        let file_type = path.extension()
                                            .and_then(|s| s.to_str())
                                            .unwrap_or("unknown")
                                            .to_string();

                        relics.push(Relic {
                            path: path.to_string_lossy().into_owned(),
                            size_bytes: metadata.len(),
                            modified_at: modified_utc.to_rfc3339(),
                            age_days: age_duration.num_days(),
                            file_type,
                        });
                    }
                }
            }
        }
    }

    match args.output.as_str() {
        "json" => {
            println!("{}", serde_json::to_string_pretty(&relics)?);
        }
        _ => {
            if relics.is_empty() {
                println!("No relics found older than {} days in '{}'.", args.age, args.path.display());
            } else {
                println!("--- Relic Manifest (Older than {} days) ---", args.age);
                for relic in relics {
                    println!(
                        "Path: {}\n  Size: {} bytes\n  Modified: {} ({} days ago)\n  Type: {}\n",
                        relic.path, relic.size_bytes, relic.modified_at, relic.age_days, relic.file_type
                    );
                }
                println!("------------------------------------------");
            }
        }
    }

    Ok(())
}
