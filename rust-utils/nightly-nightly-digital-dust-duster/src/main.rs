use clap::Parser;
use walkdir::WalkDir;
use chrono::{Utc, Duration, DateTime};
use std::path::PathBuf;
use std::fs;
use std::io::{self, Write};

#[derive(Parser, Debug)]
#[clap(author, version, about = "A high-performance CLI tool to find and categorize old, forgotten files (digital dust bunnies) based on age and size, helping declutter digital spaces.", long_about = None)]
struct Args {
    /// Path to scan for digital dust bunnies
    #[clap(short, long, default_value = ".")]
    path: PathBuf,

    /// Files older than N days will be considered dust bunnies
    #[clap(short, long, default_value_t = 365)]
    age: u64,

    /// Files larger than N bytes will be considered dust bunnies (e.g., 1048576 for 1MB)
    #[clap(short, long, default_value_t = 1048576)] // Default 1MB
    size: u64,

    /// Only list files, do not suggest actions (future: archive/delete)
    #[clap(short, long)]
    dry_run: bool,

    /// Output format: 'human' (default) or 'json'
    #[clap(short, long, default_value = "human")]
    format: String,
}

#[derive(Debug, serde::Serialize)]
struct DustBunny {
    path: String,
    size_bytes: u64,
    modified_utc: String,
    age_days: i64,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::parse();

    let scan_path = args.path.canonicalize()?;
    let age_threshold = Duration::days(args.age as i64);
    let size_threshold = args.size;
    let now = Utc::now();

    let mut dust_bunnies = Vec::new();

    if args.format == "human" {
        println!("Scanning '{}' for digital dust bunnies...", scan_path.display());
        println!("Criteria: Older than {} days AND larger than {} bytes.", args.age, args.size);
        println!("----------------------------------------------------");
    }

    for entry in WalkDir::new(&scan_path) {
        let entry = match entry {
            Ok(e) => e,
            Err(e) => {
                if args.format == "human" {
                    eprintln!("Warning: Could not access entry: {}", e);
                }
                continue;
            }
        };

        let path = entry.path();
        if path.is_file() {
            let metadata = match fs::metadata(path) {
                Ok(m) => m,
                Err(e) => {
                    if args.format == "human" {
                        eprintln!("Warning: Could not get metadata for {}: {}", path.display(), e);
                    }
                    continue;
                }
            };

            let modified_time: DateTime<Utc> = metadata.modified()?.into();
            let file_age = now.signed_duration_since(modified_time);

            if file_age > age_threshold && metadata.len() > size_threshold {
                dust_bunnies.push(DustBunny {
                    path: path.to_string_lossy().into_owned(),
                    size_bytes: metadata.len(),
                    modified_utc: modified_time.to_rfc3339(),
                    age_days: file_age.num_days(),
                });
            }
        }
    }

    if args.format == "human" {
        if dust_bunnies.is_empty() {
            println!("\n✨ All clear! No digital dust bunnies found. Your digital space is sparkling! ✨");
        } else {
            println!("\nFound {} digital dust bunnies:", dust_bunnies.len());
            for bunny in &dust_bunnies {
                println!(
                    "- Path: {}\n  Size: {} bytes\n  Modified: {} ({} days ago)",
                    bunny.path, bunny.size_bytes, bunny.modified_utc, bunny.age_days
                );
                if !args.dry_run {
                    println!("  Suggestion: Consider archiving or deleting this forgotten relic!");
                }
                println!("");
            }
            if args.dry_run {
                println!("(Dry run: No actions suggested. Remove --dry-run for suggestions.)");
            }
        }
    } else if args.format == "json" {
        let json_output = serde_json::to_string_pretty(&dust_bunnies)?;
        io::stdout().write_all(json_output.as_bytes())?;
    } else {
        return Err(format!("Unsupported format: {}", args.format).into());
    }

    Ok(())
}
