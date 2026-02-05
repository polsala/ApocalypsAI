use clap::Parser;
use walkdir::WalkDir;
use chrono::{Utc, Duration, DateTime};
use std::fs;
use std::path::PathBuf;
use anyhow::{Result, Context};

#[derive(Parser, Debug)]
#[clap(author, version, about = "Scans directories for long-forgotten files, identifying them as 'temporal residue' for digital decluttering.", long_about = None)]
struct Args {
    /// The path to scan for temporal residue.
    #[clap(value_parser)]
    path: PathBuf,

    /// The age threshold in days. Files older than this will be considered residue.
    #[clap(short, long, value_parser, default_value = "365")]
    age: u64,

    /// Use last access time instead of last modification time.
    #[clap(short, long)]
    access: bool,

    /// Use last modification time (default).
    #[clap(short, long, conflicts_with = "access")]
    modified: bool,
}

fn main() -> Result<()> {
    let args = Args::parse();

    let threshold_duration = Duration::days(args.age as i64);
    let now = Utc::now();
    let threshold_time = now - threshold_duration;

    println!("🌌 Initiating Temporal Residue Scan in: {}", args.path.display());
    println!("⏳ Seeking echoes older than {} days ({} time)...", args.age, if args.access { "access" } else { "modification" });
    println!("--------------------------------------------------");

    let mut found_residue = false;

    for entry in WalkDir::new(&args.path)
        .into_iter()
        .filter_map(|e| e.ok())
    {
        if entry.file_type().is_file() {
            let metadata = entry.metadata().context(format!("Failed to get metadata for {}", entry.path().display()))?;
            let file_time: Option<DateTime<Utc>> = if args.access {
                metadata.accessed().ok().map(DateTime::<Utc>::from)
            } else {
                metadata.modified().ok().map(DateTime::<Utc>::from)
            };

            if let Some(time) = file_time {
                if time < threshold_time {
                    println!("👻 Found a faint echo: {} (Last {} time: {})", entry.path().display(), if args.access { "access" } else { "modified" }, time.to_rfc2822());
                    found_residue = true;
                }
            }
        }
    }

    println!("--------------------------------------------------");
    if !found_residue {
        println!("✨ No significant temporal residue detected. Your digital realm is pristine!");
    } else {
        println!("🧹 Temporal residue scan complete. Consider tidying these echoes of the past.");
    }

    Ok(())
}
